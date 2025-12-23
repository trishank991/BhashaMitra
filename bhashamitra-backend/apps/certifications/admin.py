"""Admin configuration for certification models."""
from django.contrib import admin
from .models import CertificateTemplate, PrintableCertificate, AnnualProgressReport


@admin.register(CertificateTemplate)
class CertificateTemplateAdmin(admin.ModelAdmin):
    list_display = ['name', 'certificate_type', 'language', 'is_active']
    list_filter = ['certificate_type', 'is_active']
    search_fields = ['name']
    readonly_fields = ['id', 'created_at', 'updated_at']


@admin.register(PrintableCertificate)
class PrintableCertificateAdmin(admin.ModelAdmin):
    list_display = ['certificate_id', 'child', 'title', 'issued_date', 'is_shared']
    list_filter = ['issued_date', 'is_shared']
    search_fields = ['certificate_id', 'child__name', 'title']
    readonly_fields = ['id', 'created_at', 'updated_at', 'certificate_id']


@admin.register(AnnualProgressReport)
class AnnualProgressReportAdmin(admin.ModelAdmin):
    list_display = ['child', 'year', 'starting_level', 'ending_level', 'total_stories_read', 'generated_at']
    list_filter = ['year']
    search_fields = ['child__name']
    readonly_fields = ['id', 'created_at', 'updated_at']
