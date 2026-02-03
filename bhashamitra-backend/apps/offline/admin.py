"""Admin configuration for offline models."""
from django.contrib import admin
from .models import OfflinePackage, ChildOfflineContent


@admin.register(OfflinePackage)
class OfflinePackageAdmin(admin.ModelAdmin):
    list_display = ['name', 'package_type', 'language', 'version', 'size_mb', 'is_active']
    list_filter = ['package_type', 'language', 'is_active']
    search_fields = ['name']
    readonly_fields = ['id', 'created_at', 'updated_at']


@admin.register(ChildOfflineContent)
class ChildOfflineContentAdmin(admin.ModelAdmin):
    list_display = ['child', 'package', 'sync_status', 'downloaded_at', 'last_sync_at']
    list_filter = ['sync_status']
    search_fields = ['child__name', 'package__name']
    readonly_fields = ['id', 'created_at', 'updated_at']
