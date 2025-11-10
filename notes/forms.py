from django import forms
from .models import Note, Reminder
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta


# --- FORMULÁRIO DE LEMBRETE INDIVIDUAL (CASO USE EM OUTROS CONTEXTOS) ---
class ReminderForm(forms.ModelForm):
    class Meta:
        model = Reminder
        fields = ['due_date', 'recurrence', 'notify_email', 'notify_in_app']
        widgets = {'due_date': forms.DateTimeInput(attrs={'type': 'datetime-local'})}

    def clean_due_date(self):
        due_date = self.cleaned_data['due_date']

        # Converte para timezone-aware se necessário
        if timezone.is_naive(due_date):
            due_date = timezone.make_aware(due_date, timezone.get_current_timezone())

        now = timezone.now()
        min_allowed = now + timedelta(minutes=5)

        if due_date <= min_allowed:
            raise forms.ValidationError(
                "O lembrete deve ser para pelo menos 5 minutos no futuro."
            )

        return due_date


# --- FORMULÁRIO DE CADASTRO DE USUÁRIO ---
User = get_user_model()

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text="Obrigatório. Usado para contato.")

    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name", "password1", "password2")


# --- FORMULÁRIO PRINCIPAL (Nota + Lembrete juntos) ---
class NoteWithReminderForm(forms.ModelForm):
    due_date = forms.DateTimeField(
        required=False,
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        label="Data do lembrete",
        help_text="Opcional — se quiser adicionar um lembrete para esta nota.",
    )
    recurrence = forms.CharField(
        required=False,
        label="Recorrência",
        help_text="Ex: diário, semanal, etc (opcional)",
    )
    notify_email = forms.BooleanField(required=False, initial=True, label="Notificar por e-mail")
    notify_in_app = forms.BooleanField(required=False, initial=True, label="Notificar no site")

    class Meta:
        model = Note
        fields = ['title', 'content', 'is_public']
        labels = {
            'title': 'Título',
            'content': 'Conteúdo',
            'is_public': 'É pública?',
        }

    def clean_due_date(self):
        due_date = self.cleaned_data.get('due_date')

        if due_date:
            # Garante timezone-aware
            if timezone.is_naive(due_date):
                due_date = timezone.make_aware(due_date, timezone.get_current_timezone())

            now = timezone.now()
            min_allowed = now + timedelta(minutes=5)

            if due_date <= min_allowed:
                raise forms.ValidationError(
                    "O lembrete deve ser para pelo menos 5 minutos no futuro."
                )

            # Impede lembretes no passado
            if due_date < now:
                raise forms.ValidationError("A data do lembrete não pode estar no passado.")

        return due_date
