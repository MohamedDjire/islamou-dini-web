"""
Serializers for Social API (Posts, Reels, Comments)
"""

from rest_framework import serializers
from .models import Post, PostMedia, Reel, Comment, Like, Bookmark, Hashtag
from users.serializers import UserMinimalSerializer


class PostMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostMedia
        fields = ['id', 'type', 'url', 'thumbnail_url', 'order', 
                  'duration_seconds', 'width', 'height']


class HashtagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hashtag
        fields = ['id', 'name', 'slug', 'posts_count', 'reels_count']


class CommentSerializer(serializers.ModelSerializer):
    author = UserMinimalSerializer(read_only=True)
    replies = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    
    class Meta:
        model = Comment
        fields = [
            'id', 'author', 'content', 'likes_count', 'replies_count',
            'is_edited', 'parent', 'replies', 'is_liked', 
            'created_at', 'updated_at'
        ]
        read_only_fields = ['author', 'likes_count', 'replies_count', 'is_edited']
    
    def get_replies(self, obj):
        if obj.replies.exists():
            # Limit replies to first 3
            replies = obj.replies.filter(is_hidden=False)[:3]
            return CommentSerializer(replies, many=True, context=self.context).data
        return []
    
    def get_is_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return Like.objects.filter(user=request.user, comment=obj).exists()
        return False


class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['content', 'parent', 'post', 'reel']
    
    def validate(self, data):
        if not data.get('post') and not data.get('reel'):
            raise serializers.ValidationError("Un post ou reel est requis")
        if data.get('post') and data.get('reel'):
            raise serializers.ValidationError("Specifiez uniquement post ou reel")
        return data
    
    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)


class PostListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for post lists."""
    author = UserMinimalSerializer(read_only=True)
    media = PostMediaSerializer(many=True, read_only=True)
    is_liked = serializers.SerializerMethodField()
    is_bookmarked = serializers.SerializerMethodField()
    
    class Meta:
        model = Post
        fields = [
            'id', 'author', 'content', 'media', 'visibility',
            'likes_count', 'comments_count', 'shares_count', 'views_count',
            'allow_comments', 'is_liked', 'is_bookmarked',
            'created_at', 'updated_at'
        ]
    
    def get_is_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return Like.objects.filter(user=request.user, post=obj).exists()
        return False
    
    def get_is_bookmarked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return Bookmark.objects.filter(user=request.user, post=obj).exists()
        return False


class PostDetailSerializer(PostListSerializer):
    """Full serializer with comments."""
    comments = serializers.SerializerMethodField()
    
    class Meta(PostListSerializer.Meta):
        fields = PostListSerializer.Meta.fields + ['comments']
    
    def get_comments(self, obj):
        # Get top-level comments only
        comments = obj.comments.filter(parent=None, is_hidden=False)[:20]
        return CommentSerializer(comments, many=True, context=self.context).data


class PostCreateSerializer(serializers.ModelSerializer):
    media_urls = serializers.ListField(
        child=serializers.DictField(),
        write_only=True,
        required=False
    )
    
    class Meta:
        model = Post
        fields = ['content', 'visibility', 'allow_comments', 'media_urls']
    
    def create(self, validated_data):
        media_urls = validated_data.pop('media_urls', [])
        validated_data['author'] = self.context['request'].user
        post = super().create(validated_data)
        
        # Create media attachments
        for i, media_data in enumerate(media_urls):
            PostMedia.objects.create(
                post=post,
                type=media_data.get('type', 'image'),
                url=media_data.get('url'),
                thumbnail_url=media_data.get('thumbnail_url'),
                order=i,
                duration_seconds=media_data.get('duration_seconds', 0),
                width=media_data.get('width', 0),
                height=media_data.get('height', 0)
            )
        
        return post


class ReelListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for reel lists."""
    author = UserMinimalSerializer(read_only=True)
    is_liked = serializers.SerializerMethodField()
    is_bookmarked = serializers.SerializerMethodField()
    duration_formatted = serializers.SerializerMethodField()
    
    class Meta:
        model = Reel
        fields = [
            'id', 'author', 'caption', 'video_url', 'video_hls_url',
            'thumbnail_url', 'duration_seconds', 'duration_formatted',
            'audio_name', 'audio_author',
            'likes_count', 'comments_count', 'shares_count', 'views_count',
            'allow_comments', 'is_liked', 'is_bookmarked',
            'created_at'
        ]
    
    def get_is_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return Like.objects.filter(user=request.user, reel=obj).exists()
        return False
    
    def get_is_bookmarked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return Bookmark.objects.filter(user=request.user, reel=obj).exists()
        return False
    
    def get_duration_formatted(self, obj):
        minutes, seconds = divmod(obj.duration_seconds, 60)
        return f"{minutes}:{seconds:02d}"


class ReelDetailSerializer(ReelListSerializer):
    """Full serializer with comments."""
    comments = serializers.SerializerMethodField()
    
    class Meta(ReelListSerializer.Meta):
        fields = ReelListSerializer.Meta.fields + ['comments']
    
    def get_comments(self, obj):
        comments = obj.comments.filter(parent=None, is_hidden=False)[:20]
        return CommentSerializer(comments, many=True, context=self.context).data


class ReelCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reel
        fields = [
            'caption', 'video_url', 'thumbnail_url', 'duration_seconds',
            'audio_name', 'audio_author', 'allow_comments', 'allow_duet'
        ]
    
    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user
        validated_data['status'] = 'pending'  # Needs moderation
        return super().create(validated_data)


class FeedItemSerializer(serializers.Serializer):
    """Generic serializer for feed items (posts + reels)."""
    type = serializers.CharField()
    data = serializers.SerializerMethodField()
    
    def get_data(self, obj):
        if isinstance(obj, Post):
            return PostListSerializer(obj, context=self.context).data
        elif isinstance(obj, Reel):
            return ReelListSerializer(obj, context=self.context).data
        return None
