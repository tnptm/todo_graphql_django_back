from django.contrib import admin
from .models import Todo

@admin.register(Todo)
class TodoAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'completed', 'created_at', 'owner')
    list_filter = ('completed',)
    search_fields = ('text',)
