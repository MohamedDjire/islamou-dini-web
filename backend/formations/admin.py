"""
Admin configuration for formations.
"""

from django.contrib import admin
from .models import (
    Category, Formation, Module, ModuleChapter,
    Resource, Enrollment, ModuleProgress, FormationRating, FormationBookmark
)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'parent', 'order', 'is_active']
    list_filter = ['is_active', 'parent']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    ordering = ['order', 'name']


class ModuleInline(admin.TabularInline):
    model = Module
    extra = 0
    fields = ['title', 'order', 'duration_seconds', 'is_free_preview', 'is_published']


class ResourceInline(admin.TabularInline):
    model = Resource
    extra = 0
    fk_name = 'formation'


@admin.register(Formation)
class FormationAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category', 'level', 'status', 'is_featured', 'students_count']
    list_filter = ['status', 'level', 'is_featured', 'is_free', 'category']
    search_fields = ['title', 'description', 'author__email', 'author__full_name']
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ['author', 'category']
    inlines = [ModuleInline, ResourceInline]
    readonly_fields = ['students_count', 'views_count', 'rating_average', 'rating_count']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Informations de base', {
            'fields': ('title', 'slug', 'description', 'short_description', 'author')
        }),
        ('Medias', {
            'fields': ('thumbnail', 'preview_video')
        }),
        ('Classification', {
            'fields': ('category', 'level', 'tags')
        }),
        ('Tarification', {
            'fields': ('is_free', 'price', 'duration_minutes')
        }),
        ('Status', {
            'fields': ('status', 'is_featured', 'published_at')
        }),
        ('Statistiques', {
            'fields': ('students_count', 'views_count', 'rating_average', 'rating_count'),
            'classes': ('collapse',)
        }),
    )


class ModuleChapterInline(admin.TabularInline):
    model = ModuleChapter
    extra = 0


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ['title', 'formation', 'order', 'duration_seconds', 'is_free_preview', 'is_published']
    list_filter = ['is_published', 'is_free_preview', 'formation']
    search_fields = ['title', 'formation__title']
    raw_id_fields = ['formation']
    inlines = [ModuleChapterInline]


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ['user', 'formation', 'progress_percent', 'is_completed', 'enrolled_at']
    list_filter = ['is_completed', 'enrolled_at']
    search_fields = ['user__email', 'formation__title']
    raw_id_fields = ['user', 'formation', 'last_module']
    readonly_fields = ['enrolled_at', 'last_accessed']


@admin.register(FormationRating)
class FormationRatingAdmin(admin.ModelAdmin):
    list_display = ['user', 'formation', 'rating', 'is_approved', 'created_at']
    list_filter = ['rating', 'is_approved']
    search_fields = ['user__email', 'formation__title', 'review']
    raw_id_fields = ['user', 'formation']
