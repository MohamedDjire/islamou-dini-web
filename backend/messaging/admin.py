"""
Admin configuration for messaging app.
"""

from django.contrib import admin
from .models import Conversation, Message, Notification, NotificationSetting, PushToken


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ['id', 'participant_one', 'participant_two', 'last_message_at', 'created_at']
    search_fields = ['participant_one__email', 'participant_two__email']
    raw_id_fields = ['participant_one', 'participant_two', 'last_message']
    readonly_fields = ['unread_count_one', 'unread_count_two']


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['id', 'conversation', 'sender', 'type', 'content_preview', 'is_read', 'created_at']
    list_filter = ['type', 'is_read', 'is_deleted']
    search_fields = ['content', 'sender__email']
    raw_id_fields = ['conversation', 'sender', 'reply_to']
    
    def content_preview(self, obj):
        if obj.is_deleted:
            return '[Supprime]'
        return obj.content[:50] + '...' if obj.content and len(obj.content) > 50 else obj.content


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'type', 'title', 'is_read', 'created_at']
    list_filter = ['type', 'is_read', 'created_at']
    search_fields = ['title', 'body', 'user__email']
    raw_id_fields = ['user', 'actor']
    date_hierarchy = 'created_at'


@admin.register(NotificationSetting)
class NotificationSettingAdmin(admin.ModelAdmin):
    list_display = ['user', 'email_messages', 'push_messages', 'quiet_hours_enabled']
    search_fields = ['user__email']
    raw_id_fields = ['user']


@admin.register(PushToken)
class PushTokenAdmin(admin.ModelAdmin):
    list_display = ['user', 'device_type', 'device_name', 'is_active', 'last_used']
    list_filter = ['device_type', 'is_active']
    search_fields = ['user__email']
    raw_id_fields = ['user']
