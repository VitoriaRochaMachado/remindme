# notes/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.http import HttpResponseForbidden
from django.contrib import messages
from .models import Note, Reminder
from .forms import NoteWithReminderForm, SignUpForm

def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, "Conta criada com sucesso. Faça login.")
            return redirect("login")
    else:
        form = SignUpForm()
    return render(request, "registration/signup.html", {"form": form})

def creditos(request):
    return render(request, "creditos.html", {"meu_nome": "SEU_NOME"})

def public_list(request):
    notes = Note.objects.filter(is_public=True).order_by('-created_at')
    return render(request, "public_list.html", {"notes": notes})

def public_detail(request, token):
    note = get_object_or_404(Note, public_token=token, is_public=True)
    return render(request, "public_detail.html", {"note": note})

@login_required
def home(request):
    user = request.user
    if request.method == "POST":
        form = NoteWithReminderForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.owner = user
            note.save()

            due_date = form.cleaned_data.get("due_date")
            if due_date:
                Reminder.objects.create(
                    note=note,
                    due_date=due_date,
                    recurrence=form.cleaned_data.get("recurrence", ""),
                    notify_email=form.cleaned_data.get("notify_email", False),
                    notify_in_app=form.cleaned_data.get("notify_in_app", False),
                )

            messages.success(request, "Anotação criada com sucesso!")
            return redirect("notes:home")
        else:
            messages.error(request, "Corrija os erros antes de continuar.")
    else:
        form = NoteWithReminderForm()

    notes = Note.objects.filter(owner=user).order_by('-created_at')
    reminders = Reminder.objects.filter(
        note__owner=user, notified=False, due_date__gte=timezone.now()
    ).order_by('due_date')[:10]

    return render(request, "home.html", {"notes": notes, "form": form, "reminders": reminders})

@login_required
def note_edit(request, pk):
    note = get_object_or_404(Note, pk=pk)
    if note.owner != request.user:
        return HttpResponseForbidden("Você não pode editar esta anotação.")
    if request.method == "POST":
        form = NoteWithReminderForm(request.POST, instance=note)
        if form.is_valid():
            form.save()
            messages.success(request, "Anotação atualizada.")
            return redirect("notes:home")
        else:
            messages.error(request, "Corrija os erros antes de continuar.")
    else:
        form = NoteWithReminderForm(instance=note)
    return render(request, "note_form.html", {"form": form, "note": note})

@login_required
def note_delete(request, pk):
    note = get_object_or_404(Note, pk=pk)
    if note.owner != request.user:
        return HttpResponseForbidden("Você não pode apagar esta anotação.")
    note.delete()
    messages.info(request, "Anotação apagada.")
    return redirect("notes:home")


@login_required
def mark_reminder_read(request, pk):
    """
    Marca notified_in_app=True para o reminder (espera POST).
    Redireciona para a página anterior.
    """
    reminder = get_object_or_404(Reminder, pk=pk)
    if reminder.note.owner != request.user:
        return HttpResponseForbidden("Não autorizado.")
    if request.method == "POST":
        reminder.notified_in_app = True
        reminder.save(update_fields=['notified_in_app'])
    return redirect(request.META.get('HTTP_REFERER', 'notes:home'))

