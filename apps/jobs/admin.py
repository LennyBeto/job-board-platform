# apps/jobs/admin.py
from django.contrib import admin
from .models import Job, Category

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'created_at']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}
    ordering = ['name']

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ['title', 'company_name', 'category', 'location', 'job_type', 'is_active', 'created_at']
    list_filter = ['job_type', 'is_active', 'category', 'created_at']
    search_fields = ['title', 'company_name', 'location', 'description']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'company_name', 'category', 'location', 'job_type')
        }),
        ('Job Details', {
            'fields': ('description', 'requirements', 'responsibilities', 'benefits')
        }),
        ('Compensation', {
            'fields': ('salary_min', 'salary_max')
        }),
        ('Status', {
            'fields': ('is_active', 'application_deadline', 'posted_by')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )