"""Children admin configuration."""
from django.contrib import admin
from .models import Child


@admin.register(Child)
class ChildAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'language', 'level', 'total_points', 'created_at']
    list_filter = ['language', 'level', 'created_at']
    search_fields = ['name', 'user__email']
    ordering = ['-created_at']
    readonly_fields = ['total_points', 'created_at', 'updated_at']
