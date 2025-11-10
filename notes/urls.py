# notes/urls.py
from django.urls import path
from . import views

app_name = "notes"

urlpatterns = [
    path("", views.home, name="home"),
    path("creditos/", views.creditos, name="creditos"),
    path("public/notes/", views.public_list, name="public_list"),
    path("public/notes/<uuid:token>/", views.public_detail, name="public_detail"),
    path("notes/add/", views.note_add, name="note_add") if hasattr(views, 'note_add') else path("notes/add/", views.home, name="note_add"),
    path("notes/<int:pk>/", views.note_edit, name="note_edit"),
    path("notes/<int:pk>/delete/", views.note_delete, name="note_delete"),
    path("notes/<int:pk>/reminder/add/", views.add_reminder, name="add_reminder") if hasattr(views, 'add_reminder') else path("notes/<int:pk>/reminder/add/", views.home, name="add_reminder"),
    path("accounts/signup/", views.signup, name="signup"),
    # Nova rota para marcar lembrete in-app como lido
    path("reminders/<int:pk>/mark_read/", views.mark_reminder_read, name="mark_reminder_read"),
]
