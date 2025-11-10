# notes/models.py
from django.db import models
from django.conf import settings
import uuid

class Note(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_public = models.BooleanField(default=False)
    public_token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class Reminder(models.Model):
    note = models.ForeignKey(Note, on_delete=models.CASCADE, related_name='reminders')
    due_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    # envio por email (controlado pelo comando send_reminders)
    notified = models.BooleanField(default=False)

    # notificação no site: o sistema mostrará (in-app) enquanto notified_in_app=False
    notify_in_app = models.BooleanField(default=True)

    # marca que o usuário já visualizou/marcou como lido no site
    notified_in_app = models.BooleanField(default=False)

    # controle simples de recorrência (string)
    recurrence = models.CharField(max_length=20, blank=True)

    # notificação por email (flag para escolher envio)
    notify_email = models.BooleanField(default=True)

    class Meta:
        ordering = ['-due_date']

    def __str__(self):
        return f"Reminder for {self.note.title} at {self.due_date}"
