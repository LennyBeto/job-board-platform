# apps/applications/admin.py
from django.contrib import admin
from .models import Application

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ['applicant', 'job', 'status', 'applied_at']
    list_filter = ['status', 'applied_at']
    search_fields = ['applicant__email', 'job__title', 'applicant__first_name', 'applicant__last_name']
    readonly_fields = ['applied_at', 'updated_at']
    ordering = ['-applied_at']
    
    fieldsets = (
        ('Application Info', {
            'fields': ('job', 'applicant', 'cover_letter', 'resume')
        }),
        ('Status', {
            'fields': ('status', 'notes')
        }),
        ('Timestamps', {
            'fields': ('applied_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )