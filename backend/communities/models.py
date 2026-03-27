"""
Communities models for IslamouDini
Includes: Communities, Groups, Channels, Threads, Lives, Resources
"""

from django.db import models
from django.conf import settings


class Community(models.Model):
    """Main Community model."""
    
    class Visibility(models.TextChoices):
        PUBLIC = 'public', 'Public'
        PRIVATE = 'private', 'Prive'
        HIDDEN = 'hidden', 'Cache'
    
    # Basic info
    name = models.CharField(max_length=100, verbose_name='Nom')
    slug = models.SlugField(unique=True)
    description = models.TextField(max_length=2000, verbose_name='Description')
    short_description = models.CharField(max_length=200, blank=True)
    
    # Media
    avatar = models.URLField(blank=True, null=True)
    cover_image = models.URLField(blank=True, null=True)
    
    # Settings
    visibility = models.CharField(max_length=20, choices=Visibility.choices, default=Visibility.PUBLIC)
    rules = models.TextField(blank=True, null=True, verbose_name='Regles')
    
    # Requirements
    requires_approval = models.BooleanField(default=False, verbose_name='Approbation requise')
    
    # Owner
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='owned_communities'
    )
    
    # Stats
    members_count = models.PositiveIntegerField(default=0)
    posts_count = models.PositiveIntegerField(default=0)
    
    # Status
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'communities'
        verbose_name = 'Communaute'
        verbose_name_plural = 'Communautes'
        ordering = ['-members_count']
    
    def __str__(self):
        return self.name


class CommunityMember(models.Model):
    """Membership in a community."""
    
    class Role(models.TextChoices):
        MEMBER = 'member', 'Membre'
        MODERATOR = 'moderator', 'Moderateur'
        ADMIN = 'admin', 'Administrateur'
        OWNER = 'owner', 'Proprietaire'
    
    class Status(models.TextChoices):
        PENDING = 'pending', 'En attente'
        APPROVED = 'approved', 'Approuve'
        BANNED = 'banned', 'Banni'
    
    community = models.ForeignKey(
        Community,
        on_delete=models.CASCADE,
        related_name='members'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='community_memberships'
    )
    
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.MEMBER)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.APPROVED)
    
    # Notifications settings
    notifications_enabled = models.BooleanField(default=True)
    
    joined_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'community_members'
        unique_together = ('community', 'user')
        verbose_name = 'Membre'
        verbose_name_plural = 'Membres'


class Group(models.Model):
    """Groups within a community."""
    
    community = models.ForeignKey(
        Community,
        on_delete=models.CASCADE,
        related_name='groups'
    )
    
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=500, blank=True)
    icon = models.CharField(max_length=50, blank=True, null=True)
    color = models.CharField(max_length=7, default='#10B981')
    
    order = models.PositiveIntegerField(default=0)
    is_default = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'community_groups'
        ordering = ['order', 'name']
    
    def __str__(self):
        return f"{self.community.name} - {self.name}"


class Channel(models.Model):
    """Channels within a group."""
    
    class Type(models.TextChoices):
        ANNOUNCEMENTS = 'announcements', 'Annonces'
        DISCUSSION = 'discussion', 'Discussion'
        QUESTIONS = 'questions', 'Questions'
        RESOURCES = 'resources', 'Ressources'
    
    group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
        related_name='channels'
    )
    
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=300, blank=True)
    type = models.CharField(max_length=20, choices=Type.choices, default=Type.DISCUSSION)
    
    # Permissions
    is_read_only = models.BooleanField(default=False)  # Only mods can post
    members_can_create_threads = models.BooleanField(default=True)
    
    order = models.PositiveIntegerField(default=0)
    
    # Stats
    threads_count = models.PositiveIntegerField(default=0)
    messages_count = models.PositiveIntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'channels'
        ordering = ['order', 'name']
    
    def __str__(self):
        return f"#{self.name}"


class Thread(models.Model):
    """Discussion threads within a channel."""
    
    channel = models.ForeignKey(
        Channel,
        on_delete=models.CASCADE,
        related_name='threads'
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='threads'
    )
    
    title = models.CharField(max_length=200)
    content = models.TextField(max_length=10000)
    
    # Pinned threads
    is_pinned = models.BooleanField(default=False)
    is_locked = models.BooleanField(default=False)
    
    # Stats
    replies_count = models.PositiveIntegerField(default=0)
    views_count = models.PositiveIntegerField(default=0)
    likes_count = models.PositiveIntegerField(default=0)
    
    # Last activity
    last_reply_at = models.DateTimeField(null=True, blank=True)
    last_reply_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='last_replies'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'threads'
        ordering = ['-is_pinned', '-last_reply_at', '-created_at']
    
    def __str__(self):
        return self.title


class ThreadReply(models.Model):
    """Replies to threads."""
    
    thread = models.ForeignKey(
        Thread,
        on_delete=models.CASCADE,
        related_name='replies'
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='thread_replies'
    )
    
    content = models.TextField(max_length=5000)
    
    # Reply to another reply
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children'
    )
    
    likes_count = models.PositiveIntegerField(default=0)
    is_edited = models.BooleanField(default=False)
    is_hidden = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'thread_replies'
        ordering = ['created_at']


class CommunityResource(models.Model):
    """Resources/files shared in a community."""
    
    class Type(models.TextChoices):
        PDF = 'pdf', 'PDF'
        DOCUMENT = 'document', 'Document'
        LINK = 'link', 'Lien'
        VIDEO = 'video', 'Video'
        AUDIO = 'audio', 'Audio'
    
    community = models.ForeignKey(
        Community,
        on_delete=models.CASCADE,
        related_name='resources'
    )
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='community_resources'
    )
    
    title = models.CharField(max_length=200)
    description = models.TextField(max_length=500, blank=True)
    type = models.CharField(max_length=20, choices=Type.choices)
    url = models.URLField()
    file_size = models.PositiveIntegerField(default=0)
    
    # Pinned resources
    is_pinned = models.BooleanField(default=False)
    
    download_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'community_resources'
        ordering = ['-is_pinned', '-created_at']


class Live(models.Model):
    """Live sessions within a community."""
    
    class Status(models.TextChoices):
        SCHEDULED = 'scheduled', 'Programme'
        LIVE = 'live', 'En direct'
        ENDED = 'ended', 'Termine'
        CANCELLED = 'cancelled', 'Annule'
    
    community = models.ForeignKey(
        Community,
        on_delete=models.CASCADE,
        related_name='lives'
    )
    host = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='hosted_lives'
    )
    
    title = models.CharField(max_length=200)
    description = models.TextField(max_length=2000, blank=True)
    thumbnail = models.URLField(blank=True, null=True)
    
    # Status
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.SCHEDULED)
    
    # Scheduling
    scheduled_at = models.DateTimeField()
    started_at = models.DateTimeField(null=True, blank=True)
    ended_at = models.DateTimeField(null=True, blank=True)
    
    # Stream
    stream_url = models.URLField(blank=True, null=True)
    stream_key = models.CharField(max_length=100, blank=True, null=True)
    
    # Replay
    replay_enabled = models.BooleanField(default=True)
    replay_url = models.URLField(blank=True, null=True)
    
    # Chat settings
    chat_enabled = models.BooleanField(default=True)
    slow_mode_seconds = models.PositiveIntegerField(default=0)
    
    # Stats
    viewers_count = models.PositiveIntegerField(default=0)
    peak_viewers = models.PositiveIntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'lives'
        ordering = ['-scheduled_at']
    
    def __str__(self):
        return f"{self.title} - {self.host}"


class LiveQuestion(models.Model):
    """Questions submitted during a live session."""
    
    live = models.ForeignKey(
        Live,
        on_delete=models.CASCADE,
        related_name='questions'
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='live_questions'
    )
    
    content = models.TextField(max_length=500)
    
    # Voting
    votes_count = models.PositiveIntegerField(default=0)
    
    # Status
    is_answered = models.BooleanField(default=False)
    is_selected = models.BooleanField(default=False)
    answered_at = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'live_questions'
        ordering = ['-votes_count', 'created_at']


class LiveQuestionVote(models.Model):
    """Votes on live questions."""
    
    question = models.ForeignKey(
        LiveQuestion,
        on_delete=models.CASCADE,
        related_name='votes'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'live_question_votes'
        unique_together = ('question', 'user')


class LiveChatMessage(models.Model):
    """Chat messages during a live session."""
    
    live = models.ForeignKey(
        Live,
        on_delete=models.CASCADE,
        related_name='chat_messages'
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    
    content = models.TextField(max_length=500)
    
    is_pinned = models.BooleanField(default=False)
    is_hidden = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'live_chat_messages'
        ordering = ['created_at']
