"""
Admin configuration for social app.
"""

from django.contrib import admin
from .models import Post, PostMedia, Reel, Comment, Like, Bookmark, Hashtag


class PostMediaInline(admin.TabularInline):
    model = PostMedia
    extra = 0


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'author', 'status', 'visibility', 'likes_count', 'comments_count', 'created_at']
    list_filter = ['status', 'visibility', 'created_at']
    search_fields = ['content', 'author__email', 'author__full_name']
    raw_id_fields = ['author']
    inlines = [PostMediaInline]
    readonly_fields = ['likes_count', 'comments_count', 'shares_count', 'views_count']
    date_hierarchy = 'created_at'


@admin.register(Reel)
class ReelAdmin(admin.ModelAdmin):
    list_display = ['id', 'author', 'status', 'duration_seconds', 'likes_count', 'views_count', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['caption', 'author__email', 'author__full_name']
    raw_id_fields = ['author']
    readonly_fields = ['likes_count', 'comments_count', 'shares_count', 'views_count']
    date_hierarchy = 'created_at'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'author', 'content_preview', 'post', 'reel', 'is_hidden', 'created_at']
    list_filter = ['is_hidden', 'created_at']
    search_fields = ['content', 'author__email']
    raw_id_fields = ['author', 'post', 'reel', 'parent']
    
    def content_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'Contenu'


@admin.register(Hashtag)
class HashtagAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'posts_count', 'reels_count']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}
