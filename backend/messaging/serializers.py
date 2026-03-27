"""
Serializers for Messaging and Notifications API
"""

from rest_framework import serializers
from .models import Conversation, Message, MessageReaction, Notification, NotificationSetting
from users.serializers import UserMinimalSerializer


class MessageReactionSerializer(serializers.ModelSerializer):
    user = UserMinimalSerializer(read_only=True)
    
    class Meta:
        model = MessageReaction
        fields = ['id', 'user', 'emoji', 'created_at']


class MessageSerializer(serializers.ModelSerializer):
    sender = UserMinimalSerializer(read_only=True)
    reactions = MessageReactionSerializer(many=True, read_only=True)
    reply_to_preview = serializers.SerializerMethodField()
    
    class Meta:
        model = Message
        fields = [
            'id', 'sender', 'type', 'content', 
            'media_url', 'media_thumbnail', 'media_filename', 'media_size',
            'reply_to', 'reply_to_preview', 'reactions',
            'is_read', 'read_at', 'is_edited', 'is_deleted',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['sender', 'is_read', 'read_at', 'is_edited']
    
    def get_reply_to_preview(self, obj):
        if obj.reply_to and not obj.reply_to.is_deleted:
            return {
                'id': obj.reply_to.id,
                'sender': UserMinimalSerializer(obj.reply_to.sender).data,
                'content': obj.reply_to.content[:100] if obj.reply_to.content else None,
                'type': obj.reply_to.type
            }
        return None


class MessageCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['type', 'content', 'media_url', 'media_thumbnail', 
                  'media_filename', 'media_size', 'reply_to']
    
    def validate(self, data):
        if not data.get('content') and not data.get('media_url'):
            raise serializers.ValidationError("Contenu ou media requis")
        return data


class ConversationSerializer(serializers.ModelSerializer):
    other_user = serializers.SerializerMethodField()
    unread_count = serializers.SerializerMethodField()
    last_message_preview = serializers.SerializerMethodField()
    
    class Meta:
        model = Conversation
        fields = [
            'id', 'other_user', 'unread_count', 
            'last_message_preview', 'last_message_at',
            'created_at', 'updated_at'
        ]
    
    def get_other_user(self, obj):
        request = self.context.get('request')
        if request:
            other = obj.get_other_participant(request.user)
            return UserMinimalSerializer(other).data
        return None
    
    def get_unread_count(self, obj):
        request = self.context.get('request')
        if request:
            return obj.get_unread_count(request.user)
        return 0
    
    def get_last_message_preview(self, obj):
        if obj.last_message:
            return {
                'content': obj.last_message.content[:100] if obj.last_message.content else None,
                'type': obj.last_message.type,
                'sender_id': obj.last_message.sender_id,
                'is_deleted': obj.last_message.is_deleted
            }
        return None


class ConversationDetailSerializer(ConversationSerializer):
    messages = serializers.SerializerMethodField()
    
    class Meta(ConversationSerializer.Meta):
        fields = ConversationSerializer.Meta.fields + ['messages']
    
    def get_messages(self, obj):
        messages = obj.messages.filter(is_deleted=False).order_by('-created_at')[:50]
        return MessageSerializer(messages, many=True, context=self.context).data


class NotificationSerializer(serializers.ModelSerializer):
    actor = UserMinimalSerializer(read_only=True)
    
    class Meta:
        model = Notification
        fields = [
            'id', 'type', 'title', 'body', 'actor',
            'target_type', 'target_id', 'action_url', 'image_url',
            'is_read', 'read_at', 'created_at'
        ]


class NotificationSettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationSetting
        fields = [
            'email_likes', 'email_comments', 'email_follows', 'email_messages',
            'email_formations', 'email_communities', 'email_lives',
            'push_likes', 'push_comments', 'push_follows', 'push_messages',
            'push_formations', 'push_communities', 'push_lives',
            'quiet_hours_enabled', 'quiet_hours_start', 'quiet_hours_end'
        ]
