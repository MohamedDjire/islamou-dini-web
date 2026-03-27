"""
Serializers for Formations API
"""

from rest_framework import serializers
from .models import (
    Category, Formation, Module, ModuleChapter, 
    Resource, Enrollment, ModuleProgress, FormationRating, FormationBookmark
)
from users.serializers import UserMinimalSerializer


class CategorySerializer(serializers.ModelSerializer):
    subcategories = serializers.SerializerMethodField()
    formations_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Category
        fields = [
            'id', 'name', 'slug', 'description', 'icon', 'color',
            'parent', 'order', 'subcategories', 'formations_count'
        ]
    
    def get_subcategories(self, obj):
        if obj.subcategories.exists():
            return CategorySerializer(obj.subcategories.filter(is_active=True), many=True).data
        return []
    
    def get_formations_count(self, obj):
        return obj.formations.filter(status='published').count()


class ModuleChapterSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModuleChapter
        fields = ['id', 'title', 'timestamp_seconds', 'order']


class ResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resource
        fields = [
            'id', 'title', 'description', 'type', 
            'file_url', 'file_size', 'order', 'download_count'
        ]


class ModuleListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for module lists."""
    duration_formatted = serializers.SerializerMethodField()
    
    class Meta:
        model = Module
        fields = [
            'id', 'title', 'description', 'order', 
            'duration_seconds', 'duration_formatted',
            'is_free_preview', 'thumbnail'
        ]
    
    def get_duration_formatted(self, obj):
        minutes, seconds = divmod(obj.duration_seconds, 60)
        hours, minutes = divmod(minutes, 60)
        if hours:
            return f"{hours}h {minutes}min"
        return f"{minutes}min {seconds}s"


class ModuleDetailSerializer(serializers.ModelSerializer):
    """Full serializer with video URLs and chapters."""
    chapters = ModuleChapterSerializer(many=True, read_only=True)
    resources = ResourceSerializer(many=True, read_only=True)
    duration_formatted = serializers.SerializerMethodField()
    user_progress = serializers.SerializerMethodField()
    
    class Meta:
        model = Module
        fields = [
            'id', 'title', 'description', 'order',
            'video_url', 'video_hls_url', 'duration_seconds', 
            'duration_formatted', 'thumbnail', 'is_free_preview',
            'chapters', 'resources', 'user_progress'
        ]
    
    def get_duration_formatted(self, obj):
        minutes, seconds = divmod(obj.duration_seconds, 60)
        hours, minutes = divmod(minutes, 60)
        if hours:
            return f"{hours}h {minutes}min"
        return f"{minutes}min {seconds}s"
    
    def get_user_progress(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            progress = ModuleProgress.objects.filter(
                user=request.user, module=obj
            ).first()
            if progress:
                return {
                    'watch_time_seconds': progress.watch_time_seconds,
                    'last_position_seconds': progress.last_position_seconds,
                    'is_completed': progress.is_completed
                }
        return None


class FormationListSerializer(serializers.ModelSerializer):
    """Serializer for formation lists/cards."""
    author = UserMinimalSerializer(read_only=True)
    category = serializers.StringRelatedField()
    duration_formatted = serializers.SerializerMethodField()
    is_enrolled = serializers.SerializerMethodField()
    
    class Meta:
        model = Formation
        fields = [
            'id', 'title', 'slug', 'short_description', 'thumbnail',
            'category', 'level', 'author', 'is_free', 'price',
            'duration_minutes', 'duration_formatted', 'modules_count',
            'students_count', 'rating_average', 'rating_count',
            'is_featured', 'is_enrolled', 'created_at'
        ]
    
    def get_duration_formatted(self, obj):
        hours, minutes = divmod(obj.duration_minutes, 60)
        if hours:
            return f"{hours}h {minutes}min"
        return f"{minutes}min"
    
    def get_is_enrolled(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return Enrollment.objects.filter(
                user=request.user, formation=obj
            ).exists()
        return False


class FormationDetailSerializer(serializers.ModelSerializer):
    """Full serializer for formation detail page."""
    author = UserMinimalSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    modules = ModuleListSerializer(many=True, read_only=True)
    resources = ResourceSerializer(many=True, read_only=True)
    duration_formatted = serializers.SerializerMethodField()
    is_enrolled = serializers.SerializerMethodField()
    user_progress = serializers.SerializerMethodField()
    is_bookmarked = serializers.SerializerMethodField()
    
    class Meta:
        model = Formation
        fields = [
            'id', 'title', 'slug', 'description', 'short_description',
            'thumbnail', 'preview_video', 'category', 'level', 'tags',
            'author', 'is_free', 'price', 'duration_minutes', 
            'duration_formatted', 'status', 'is_featured',
            'students_count', 'views_count', 'rating_average', 'rating_count',
            'modules', 'resources', 'is_enrolled', 'user_progress',
            'is_bookmarked', 'created_at', 'published_at'
        ]
    
    def get_duration_formatted(self, obj):
        hours, minutes = divmod(obj.duration_minutes, 60)
        if hours:
            return f"{hours}h {minutes}min"
        return f"{minutes}min"
    
    def get_is_enrolled(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return Enrollment.objects.filter(
                user=request.user, formation=obj
            ).exists()
        return False
    
    def get_user_progress(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            enrollment = Enrollment.objects.filter(
                user=request.user, formation=obj
            ).first()
            if enrollment:
                return {
                    'progress_percent': enrollment.progress_percent,
                    'last_module_id': enrollment.last_module_id,
                    'last_position_seconds': enrollment.last_position_seconds,
                    'is_completed': enrollment.is_completed
                }
        return None
    
    def get_is_bookmarked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return FormationBookmark.objects.filter(
                user=request.user, formation=obj
            ).exists()
        return False


class FormationCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating/updating formations."""
    
    class Meta:
        model = Formation
        fields = [
            'title', 'slug', 'description', 'short_description',
            'thumbnail', 'preview_video', 'category', 'level', 'tags',
            'is_free', 'price', 'duration_minutes'
        ]
    
    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)


class EnrollmentSerializer(serializers.ModelSerializer):
    formation = FormationListSerializer(read_only=True)
    
    class Meta:
        model = Enrollment
        fields = [
            'id', 'formation', 'progress_percent', 'last_module',
            'last_position_seconds', 'is_completed', 'completed_at',
            'enrolled_at', 'last_accessed'
        ]


class ModuleProgressUpdateSerializer(serializers.Serializer):
    """Serializer for updating module progress."""
    watch_time_seconds = serializers.IntegerField(min_value=0)
    last_position_seconds = serializers.IntegerField(min_value=0)
    is_completed = serializers.BooleanField(default=False)


class FormationRatingSerializer(serializers.ModelSerializer):
    user = UserMinimalSerializer(read_only=True)
    
    class Meta:
        model = FormationRating
        fields = ['id', 'user', 'rating', 'review', 'created_at']
        read_only_fields = ['user']
    
    def validate_rating(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("La note doit etre entre 1 et 5")
        return value
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
