"""
Admin configuration for communities app.
"""

from django.contrib import admin
from .models import (
    Community, CommunityMember, Group, Channel, Thread, ThreadReply,
    CommunityResource, Live, LiveQuestion, LiveChatMessage
)


class CommunityMemberInline(admin.TabularInline):
    model = CommunityMember
    extra = 0
    raw_id_fields = ['user']


class GroupInline(admin.TabularInline):
    model = Group
    extra = 0


@admin.register(Community)
class CommunityAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'owner', 'visibility', 'members_count', 'is_verified', 'is_active']
    list_filter = ['visibility', 'is_verified', 'is_active', 'requires_approval']
    search_fields = ['name', 'description', 'owner__email']
    prepopulated_fields = {'slug': ('name',)}
    raw_id_fields = ['owner']
    inlines = [CommunityMemberInline, GroupInline]
    readonly_fields = ['members_count', 'posts_count']


class ChannelInline(admin.TabularInline):
    model = Channel
    extra = 0


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ['name', 'community', 'order', 'is_default']
    list_filter = ['community', 'is_default']
    search_fields = ['name', 'community__name']
    raw_id_fields = ['community']
    inlines = [ChannelInline]


@admin.register(Channel)
class ChannelAdmin(admin.ModelAdmin):
    list_display = ['name', 'group', 'type', 'is_read_only', 'threads_count']
    list_filter = ['type', 'is_read_only']
    search_fields = ['name', 'group__name', 'group__community__name']
    raw_id_fields = ['group']


@admin.register(Thread)
class ThreadAdmin(admin.ModelAdmin):
    list_display = ['title', 'channel', 'author', 'is_pinned', 'is_locked', 'replies_count', 'created_at']
    list_filter = ['is_pinned', 'is_locked', 'created_at']
    search_fields = ['title', 'content', 'author__email']
    raw_id_fields = ['channel', 'author', 'last_reply_by']


@admin.register(CommunityResource)
class CommunityResourceAdmin(admin.ModelAdmin):
    list_display = ['title', 'community', 'type', 'is_pinned', 'download_count', 'created_at']
    list_filter = ['type', 'is_pinned']
    search_fields = ['title', 'community__name']
    raw_id_fields = ['community', 'uploaded_by']


@admin.register(Live)
class LiveAdmin(admin.ModelAdmin):
    list_display = ['title', 'community', 'host', 'status', 'scheduled_at', 'viewers_count']
    list_filter = ['status', 'scheduled_at']
    search_fields = ['title', 'community__name', 'host__email']
    raw_id_fields = ['community', 'host']
    readonly_fields = ['viewers_count', 'peak_viewers']


@admin.register(LiveQuestion)
class LiveQuestionAdmin(admin.ModelAdmin):
    list_display = ['content_preview', 'live', 'author', 'votes_count', 'is_answered', 'is_selected']
    list_filter = ['is_answered', 'is_selected']
    search_fields = ['content', 'author__email']
    raw_id_fields = ['live', 'author']
    
    def content_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
