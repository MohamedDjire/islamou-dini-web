"""
Serializers for Communities API
"""

from rest_framework import serializers
from .models import (
    Community, CommunityMember, Group, Channel, Thread, ThreadReply,
    CommunityResource, Live, LiveQuestion, LiveChatMessage
)
from users.serializers import UserMinimalSerializer


class CommunityMemberSerializer(serializers.ModelSerializer):
    user = UserMinimalSerializer(read_only=True)
    
    class Meta:
        model = CommunityMember
        fields = ['id', 'user', 'role', 'status', 'notifications_enabled', 'joined_at']


class ChannelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Channel
        fields = [
            'id', 'name', 'description', 'type', 'is_read_only',
            'members_can_create_threads', 'order', 'threads_count', 'messages_count'
        ]


class GroupSerializer(serializers.ModelSerializer):
    channels = ChannelSerializer(many=True, read_only=True)
    
    class Meta:
        model = Group
        fields = ['id', 'name', 'description', 'icon', 'color', 'order', 'is_default', 'channels']


class CommunityListSerializer(serializers.ModelSerializer):
    owner = UserMinimalSerializer(read_only=True)
    is_member = serializers.SerializerMethodField()
    
    class Meta:
        model = Community
        fields = [
            'id', 'name', 'slug', 'short_description', 'avatar', 'cover_image',
            'visibility', 'owner', 'members_count', 'posts_count',
            'is_verified', 'is_member', 'created_at'
        ]
    
    def get_is_member(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return CommunityMember.objects.filter(
                community=obj, user=request.user, status='approved'
            ).exists()
        return False


class CommunityDetailSerializer(serializers.ModelSerializer):
    owner = UserMinimalSerializer(read_only=True)
    groups = GroupSerializer(many=True, read_only=True)
    is_member = serializers.SerializerMethodField()
    user_membership = serializers.SerializerMethodField()
    
    class Meta:
        model = Community
        fields = [
            'id', 'name', 'slug', 'description', 'short_description',
            'avatar', 'cover_image', 'visibility', 'rules', 'requires_approval',
            'owner', 'members_count', 'posts_count', 'is_verified',
            'is_member', 'user_membership', 'groups', 'created_at', 'updated_at'
        ]
    
    def get_is_member(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return CommunityMember.objects.filter(
                community=obj, user=request.user, status='approved'
            ).exists()
        return False
    
    def get_user_membership(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            membership = CommunityMember.objects.filter(
                community=obj, user=request.user
            ).first()
            if membership:
                return {
                    'role': membership.role,
                    'status': membership.status,
                    'notifications_enabled': membership.notifications_enabled
                }
        return None


class CommunityCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Community
        fields = [
            'name', 'slug', 'description', 'short_description',
            'avatar', 'cover_image', 'visibility', 'rules', 'requires_approval'
        ]
    
    def create(self, validated_data):
        validated_data['owner'] = self.context['request'].user
        community = super().create(validated_data)
        
        # Add owner as member
        CommunityMember.objects.create(
            community=community,
            user=community.owner,
            role='owner',
            status='approved'
        )
        
        # Create default group and channels
        default_group = Group.objects.create(
            community=community,
            name='General',
            description='Discussions generales',
            is_default=True
        )
        
        Channel.objects.create(
            group=default_group,
            name='annonces',
            description='Annonces officielles',
            type='announcements',
            is_read_only=True,
            order=0
        )
        Channel.objects.create(
            group=default_group,
            name='discussions',
            description='Discussions libres',
            type='discussion',
            order=1
        )
        Channel.objects.create(
            group=default_group,
            name='questions',
            description='Posez vos questions',
            type='questions',
            order=2
        )
        
        return community


class ThreadReplySerializer(serializers.ModelSerializer):
    author = UserMinimalSerializer(read_only=True)
    
    class Meta:
        model = ThreadReply
        fields = [
            'id', 'author', 'content', 'parent', 'likes_count',
            'is_edited', 'created_at', 'updated_at'
        ]
        read_only_fields = ['author', 'likes_count', 'is_edited']


class ThreadListSerializer(serializers.ModelSerializer):
    author = UserMinimalSerializer(read_only=True)
    last_reply_by = UserMinimalSerializer(read_only=True)
    
    class Meta:
        model = Thread
        fields = [
            'id', 'title', 'author', 'is_pinned', 'is_locked',
            'replies_count', 'views_count', 'likes_count',
            'last_reply_at', 'last_reply_by', 'created_at'
        ]


class ThreadDetailSerializer(serializers.ModelSerializer):
    author = UserMinimalSerializer(read_only=True)
    replies = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    
    class Meta:
        model = Thread
        fields = [
            'id', 'channel', 'title', 'content', 'author',
            'is_pinned', 'is_locked', 'replies_count', 'views_count',
            'likes_count', 'is_liked', 'replies', 'created_at', 'updated_at'
        ]
    
    def get_replies(self, obj):
        replies = obj.replies.filter(is_hidden=False, parent=None)[:50]
        return ThreadReplySerializer(replies, many=True, context=self.context).data
    
    def get_is_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            from social.models import Like
            # Note: We'd need to add thread support to Like model
            return False
        return False


class ThreadCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Thread
        fields = ['channel', 'title', 'content']
    
    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user
        thread = super().create(validated_data)
        
        # Update channel stats
        Channel.objects.filter(pk=thread.channel.pk).update(
            threads_count=thread.channel.threads_count + 1
        )
        
        return thread


class CommunityResourceSerializer(serializers.ModelSerializer):
    uploaded_by = UserMinimalSerializer(read_only=True)
    
    class Meta:
        model = CommunityResource
        fields = [
            'id', 'title', 'description', 'type', 'url', 'file_size',
            'is_pinned', 'download_count', 'uploaded_by', 'created_at'
        ]


class LiveQuestionSerializer(serializers.ModelSerializer):
    author = UserMinimalSerializer(read_only=True)
    has_voted = serializers.SerializerMethodField()
    
    class Meta:
        model = LiveQuestion
        fields = [
            'id', 'author', 'content', 'votes_count', 'has_voted',
            'is_answered', 'is_selected', 'answered_at', 'created_at'
        ]
    
    def get_has_voted(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            from .models import LiveQuestionVote
            return LiveQuestionVote.objects.filter(
                question=obj, user=request.user
            ).exists()
        return False


class LiveChatMessageSerializer(serializers.ModelSerializer):
    author = UserMinimalSerializer(read_only=True)
    
    class Meta:
        model = LiveChatMessage
        fields = ['id', 'author', 'content', 'is_pinned', 'created_at']


class LiveListSerializer(serializers.ModelSerializer):
    host = UserMinimalSerializer(read_only=True)
    community_name = serializers.CharField(source='community.name', read_only=True)
    
    class Meta:
        model = Live
        fields = [
            'id', 'title', 'description', 'thumbnail', 'status',
            'host', 'community_name', 'scheduled_at', 'started_at',
            'viewers_count', 'replay_enabled', 'created_at'
        ]


class LiveDetailSerializer(serializers.ModelSerializer):
    host = UserMinimalSerializer(read_only=True)
    questions = serializers.SerializerMethodField()
    
    class Meta:
        model = Live
        fields = [
            'id', 'title', 'description', 'thumbnail', 'status',
            'host', 'community', 'scheduled_at', 'started_at', 'ended_at',
            'stream_url', 'replay_url', 'replay_enabled',
            'chat_enabled', 'slow_mode_seconds',
            'viewers_count', 'peak_viewers', 'questions', 'created_at'
        ]
    
    def get_questions(self, obj):
        questions = obj.questions.filter(is_answered=False)[:20]
        return LiveQuestionSerializer(questions, many=True, context=self.context).data


class LiveCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Live
        fields = [
            'community', 'title', 'description', 'thumbnail',
            'scheduled_at', 'replay_enabled', 'chat_enabled', 'slow_mode_seconds'
        ]
    
    def create(self, validated_data):
        validated_data['host'] = self.context['request'].user
        return super().create(validated_data)
