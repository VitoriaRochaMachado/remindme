# notes/context_processors.py
from django.utils import timezone
from .models import Reminder

def in_app_notifications(request):
    """
    Fornece 'in_app_reminders' em templates: lembretes com notify_in_app=True,
    notificados_in_app=False e due_date <= agora (vencidos/presentes).
    """
    if not request.user.is_authenticated:
        return {}
    now = timezone.now()
    reminders = Reminder.objects.filter(
        note__owner=request.user,
        notify_in_app=True,
        notified_in_app=False,
        due_date__lte=now
    ).select_related('note').order_by('due_date')
    return {'in_app_reminders': reminders}
