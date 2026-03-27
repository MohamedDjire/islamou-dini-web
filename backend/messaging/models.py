"""
Messaging and Notifications models for IslamouDini
Includes: Conversations, Messages, Notifications
"""

from django.db import models
from django.conf import settings


class Conversation(models.Model):
    """Direct message conversation between two users."""
    
    # Participants (always 2 for DM)
    participant_one = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='conversations_as_one'
    )
    participant_two = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='conversations_as_two'
    )
    
    # Last message preview
    last_message = models.ForeignKey(
        'Message',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='+'
    )
    last_message_at = models.DateTimeField(null=True, blank=True)
    
    # Unread counts
    unread_count_one = models.PositiveIntegerField(default=0)
    unread_count_two = models.PositiveIntegerField(default=0)
    
    # Status
    is_blocked_by_one = models.BooleanField(default=False)
    is_blocked_by_two = models.BooleanField(default=False)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'conversations'
        ordering = ['-last_message_at', '-created_at']
        # Ensure unique conversation between two users
        constraints = [
            models.UniqueConstraint(
                fields=['participant_one', 'participant_two'],
                name='unique_conversation'
            )
        ]
    
    def get_other_participant(self, user):
        """Get the other participant in the conversation."""
        if self.participant_one == user:
            return self.participant_two
        return self.participant_one
    
    def get_unread_count(self, user):
        """Get unread count for a user."""
        if self.participant_one == user:
            return self.unread_count_one
        return self.unread_count_two
    
    def mark_as_read(self, user):
        """Mark conversation as read for a user."""
        if self.participant_one == user:
            self.unread_count_one = 0
        else:
            self.unread_count_two = 0
        self.save()


class Message(models.Model):
    """Individual message in a conversation."""
    
    class Type(models.TextChoices):
        TEXT = 'text', 'Texte'
        IMAGE = 'image', 'Image'
        VIDEO = 'video', 'Video'
        AUDIO = 'audio', 'Audio'
        FILE = 'file', 'Fichier'
    
    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name='messages'
    )
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='sent_messages'
    )
    
    # Content
    type = models.CharField(max_length=20, choices=Type.choices, default=Type.TEXT)
    content = models.TextField(max_length=5000, blank=True)
    
    # Media (for images, videos, etc.)
    media_url = models.URLField(blank=True, null=True)
    media_thumbnail = models.URLField(blank=True, null=True)
    media_filename = models.CharField(max_length=255, blank=True, null=True)
    media_size = models.PositiveIntegerField(default=0)
    
    # Reply to another message
    reply_to = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='replies'
    )
    
    # Status
    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)
    is_edited = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'messages'
        ordering = ['created_at']
    
    def __str__(self):
        return f"Message from {self.sender} at {self.created_at}"


class MessageReaction(models.Model):
    """Emoji reactions on messages."""
    
    message = models.ForeignKey(
        Message,
        on_delete=models.CASCADE,
        related_name='reactions'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    emoji = models.CharField(max_length=10)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'message_reactions'
        unique_together = ('message', 'user', 'emoji')


class Notification(models.Model):
    """User notifications."""
    
    class Type(models.TextChoices):
        # Social
        LIKE = 'like', 'Like'
        COMMENT = 'comment', 'Commentaire'
        FOLLOW = 'follow', 'Nouvel abonne'
        MENTION = 'mention', 'Mention'
        
        # Formations
        NEW_MODULE = 'new_module', 'Nouveau module'
        COURSE_UPDATE = 'course_update', 'Mise a jour formation'
        CERTIFICATE = 'certificate', 'Certificat'
        
        # Communities
        COMMUNITY_INVITE = 'community_invite', 'Invitation communaute'
        COMMUNITY_POST = 'community_post', 'Publication communaute'
        THREAD_REPLY = 'thread_reply', 'Reponse thread'
        
        # Lives
        LIVE_STARTING = 'live_starting', 'Live commence'
        LIVE_SCHEDULED = 'live_scheduled', 'Live programme'
        
        # Messages
        NEW_MESSAGE = 'new_message', 'Nouveau message'
        
        # System
        SYSTEM = 'system', 'Systeme'
        MODERATION = 'moderation', 'Moderation'
    
    # Recipient
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notifications'
    )
    
    # Type and content
    type = models.CharField(max_length=30, choices=Type.choices)
    title = models.CharField(max_length=200)
    body = models.TextField(max_length=500, blank=True)
    
    # Actor (who triggered the notification)
    actor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='triggered_notifications'
    )
    
    # Related object (polymorphic reference)
    # We store the object type and ID to link to any model
    target_type = models.CharField(max_length=50, blank=True)  # e.g., 'post', 'reel', 'formation'
    target_id = models.PositiveIntegerField(null=True, blank=True)
    
    # Action URL
    action_url = models.CharField(max_length=500, blank=True)
    
    # Image (for preview)
    image_url = models.URLField(blank=True, null=True)
    
    # Status
    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'notifications'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'is_read', '-created_at']),
        ]
    
    def __str__(self):
        return f"{self.type} for {self.user}"


class NotificationSetting(models.Model):
    """User notification preferences."""
    
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notification_settings'
    )
    
    # Email notifications
    email_likes = models.BooleanField(default=True)
    email_comments = models.BooleanField(default=True)
    email_follows = models.BooleanField(default=True)
    email_messages = models.BooleanField(default=True)
    email_formations = models.BooleanField(default=True)
    email_communities = models.BooleanField(default=True)
    email_lives = models.BooleanField(default=True)
    
    # Push notifications
    push_likes = models.BooleanField(default=True)
    push_comments = models.BooleanField(default=True)
    push_follows = models.BooleanField(default=True)
    push_messages = models.BooleanField(default=True)
    push_formations = models.BooleanField(default=True)
    push_communities = models.BooleanField(default=True)
    push_lives = models.BooleanField(default=True)
    
    # Quiet hours
    quiet_hours_enabled = models.BooleanField(default=False)
    quiet_hours_start = models.TimeField(null=True, blank=True)  # e.g., 22:00
    quiet_hours_end = models.TimeField(null=True, blank=True)    # e.g., 07:00
    
    class Meta:
        db_table = 'notification_settings'


class PushToken(models.Model):
    """Store push notification tokens for users."""
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='push_tokens'
    )
    token = models.TextField()
    device_type = models.CharField(max_length=20)  # 'web', 'ios', 'android'
    device_name = models.CharField(max_length=100, blank=True)
    
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    last_used = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'push_tokens'
