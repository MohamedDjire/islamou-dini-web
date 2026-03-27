from django.contrib import admin
from .models import Report, Ban

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('id', 'reporter', 'reported_user', 'reason', 'status', 'created_at')
    list_filter = ('status', 'reason', 'created_at')
    search_fields = ('reporter__username', 'reported_user__username', 'description')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Report Info', {
            'fields': ('reporter', 'reported_user', 'reason', 'description')
        }),
        ('Status', {
            'fields': ('status',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(Ban)
class BanAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'moderator', 'reason', 'is_active', 'expires_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('user__username', 'reason')
    readonly_fields = ('created_at', 'expires_at')
    
    fieldsets = (
        ('User Info', {
            'fields': ('user', 'moderator')
        }),
        ('Ban Details', {
            'fields': ('reason', 'duration_days', 'is_active')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'expires_at'),
            'classes': ('collapse',)
        }),
    )
