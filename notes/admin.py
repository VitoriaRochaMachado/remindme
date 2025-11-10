from django.contrib import admin
from .models import Note, Reminder

@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'created_at', 'is_public')
    search_fields = ('title', 'content', 'owner__username')
    readonly_fields = ('public_token',)

@admin.register(Reminder)
class ReminderAdmin(admin.ModelAdmin):
    list_display = ('note', 'due_date', 'notified',)
    list_filter = ('notified',)
