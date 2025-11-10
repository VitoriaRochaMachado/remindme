# notes/management/commands/send_reminders.py
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from notes.models import Reminder

class Command(BaseCommand):
    help = "Envia lembretes por e-mail apenas uma vez"

    def handle(self, *args, **options):
        now = timezone.now()
        due = Reminder.objects.filter(due_date__lte=now, notified=False)
        self.stdout.write(f"Verificando {due.count()} lembretes pendentes...")

        for r in due:
            user = r.note.owner
            subject = f"Lembrete: {r.note.title}"
            message = (
                f"Olá {user.get_full_name() or user.username},\n\n"
                f"Lembrete: {r.note.title}\n\n"
                f"{r.note.content}\n\n"
                f"Data: {r.due_date.strftime('%d/%m/%Y %H:%M')}\n\n"
                f"(Enviado automaticamente pelo sistema de lembretes)"
            )

            try:
                if r.notify_email and user.email:
                    send_mail(
                        subject,
                        message,
                        settings.DEFAULT_FROM_EMAIL,
                        [user.email],
                        fail_silently=False,
                    )
                    self.stdout.write(self.style.SUCCESS(f"E-mail enviado para {user.email}"))

                # Marca como notificado por email — NÃO altera notified_in_app
                r.notified = True
                r.save(update_fields=['notified'])
            except Exception as e:
                self.stderr.write(self.style.ERROR(f"Erro ao enviar e-mail: {e}"))

        self.stdout.write(self.style.SUCCESS("Processo finalizado."))
