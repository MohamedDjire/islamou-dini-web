"""
Moderation models for IslamouDini
Includes: Reports, Content Reviews, Bans, Audit Logs
"""

from django.db import models
from django.conf import settings


class Report(models.Model):
    """User reports on content or users."""
    
    class Type(models.TextChoices):
        SPAM = 'spam', 'Spam'
        HARASSMENT = 'harassment', 'Harcelement'
        INAPPROPRIATE = 'inappropriate', 'Contenu inapproprie'
        MISINFORMATION = 'misinformation', 'Fausse information'
        COPYRIGHT = 'copyright', 'Violation copyright'
        HATE_SPEECH = 'hate_speech', 'Discours haineux'
        VIOLENCE = 'violence', 'Violence'
        OTHER = 'other', 'Autre'
    
    class Status(models.TextChoices):
        PENDING = 'pending', 'En attente'
        REVIEWING = 'reviewing', 'En cours d\'examen'
        RESOLVED = 'resolved', 'Resolu'
        DISMISSED = 'dismissed', 'Rejete'
    
    class TargetType(models.TextChoices):
        USER = 'user', 'Utilisateur'
        POST = 'post', 'Publication'
        REEL = 'reel', 'Reel'
        COMMENT = 'comment', 'Commentaire'
        FORMATION = 'formation', 'Formation'
        COMMUNITY = 'community', 'Communaute'
        MESSAGE = 'message', 'Message'
    
    # Reporter
    reporter = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reports_made'
    )
    
    # Target
    target_type = models.CharField(max_length=20, choices=TargetType.choices)
    target_id = models.PositiveIntegerField()
    
    # Reported user (owner of content or user being reported)
    reported_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reports_received',
        null=True,
        blank=True
    )
    
    # Report details
    type = models.CharField(max_length=30, choices=Type.choices)
    description = models.TextField(max_length=1000, blank=True)
    
    # Status
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    priority = models.PositiveSmallIntegerField(default=1)  # 1-5, higher = more urgent
    
    # Review
    reviewed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='reports_reviewed'
    )
    review_notes = models.TextField(blank=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    
    # Action taken
    action_taken = models.CharField(max_length=100, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'reports'
        ordering = ['-priority', '-created_at']
        indexes = [
            models.Index(fields=['status', '-created_at']),
            models.Index(fields=['target_type', 'target_id']),
        ]


class ContentReview(models.Model):
    """Queue for content requiring moderation before publishing."""
    
    class Status(models.TextChoices):
        PENDING = 'pending', 'En attente'
        APPROVED = 'approved', 'Approuve'
        REJECTED = 'rejected', 'Rejete'
        NEEDS_EDIT = 'needs_edit', 'Necessite modification'
    
    class ContentType(models.TextChoices):
        REEL = 'reel', 'Reel'
        FORMATION = 'formation', 'Formation'
        POST = 'post', 'Publication'
        COMMUNITY = 'community', 'Communaute'
    
    content_type = models.CharField(max_length=20, choices=ContentType.choices)
    content_id = models.PositiveIntegerField()
    
    # Author
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='content_reviews'
    )
    
    # Status
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    
    # Review
    reviewed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='content_reviewed'
    )
    review_notes = models.TextField(blank=True)
    rejection_reason = models.TextField(blank=True)
    
    # Timestamps
    submitted_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'content_reviews'
        ordering = ['-submitted_at']
        indexes = [
            models.Index(fields=['status', '-submitted_at']),
        ]


class UserBan(models.Model):
    """User bans and restrictions."""
    
    class Type(models.TextChoices):
        TEMPORARY = 'temporary', 'Temporaire'
        PERMANENT = 'permanent', 'Permanent'
        SHADOW = 'shadow', 'Shadow ban'
    
    class Scope(models.TextChoices):
        GLOBAL = 'global', 'Global'
        POSTING = 'posting', 'Publications'
        COMMENTING = 'commenting', 'Commentaires'
        MESSAGING = 'messaging', 'Messagerie'
        COMMUNITY = 'community', 'Communaute specifique'
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='bans'
    )
    
    type = models.CharField(max_length=20, choices=Type.choices)
    scope = models.CharField(max_length=20, choices=Scope.choices, default=Scope.GLOBAL)
    
    # For community-specific bans
    community_id = models.PositiveIntegerField(null=True, blank=True)
    
    reason = models.TextField()
    
    # Duration (null for permanent)
    started_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    
    # Who issued the ban
    issued_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='bans_issued'
    )
    
    # Related report
    report = models.ForeignKey(
        Report,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    
    # Status
    is_active = models.BooleanField(default=True)
    lifted_at = models.DateTimeField(null=True, blank=True)
    lifted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='bans_lifted'
    )
    
    class Meta:
        db_table = 'user_bans'
        ordering = ['-started_at']


class AuditLog(models.Model):
    """Audit log for moderation actions."""
    
    class Action(models.TextChoices):
        # User actions
        USER_BAN = 'user_ban', 'Bannissement utilisateur'
        USER_UNBAN = 'user_unban', 'Debannissement utilisateur'
        USER_WARN = 'user_warn', 'Avertissement utilisateur'
        
        # Content actions
        CONTENT_APPROVE = 'content_approve', 'Approbation contenu'
        CONTENT_REJECT = 'content_reject', 'Rejet contenu'
        CONTENT_DELETE = 'content_delete', 'Suppression contenu'
        CONTENT_HIDE = 'content_hide', 'Masquage contenu'
        
        # Report actions
        REPORT_RESOLVE = 'report_resolve', 'Resolution signalement'
        REPORT_DISMISS = 'report_dismiss', 'Rejet signalement'
        
        # Community actions
        COMMUNITY_BAN = 'community_ban', 'Bannissement communaute'
        COMMUNITY_DELETE = 'community_delete', 'Suppression communaute'
        
        # Other
        OTHER = 'other', 'Autre'
    
    # Moderator
    moderator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='moderation_actions'
    )
    
    action = models.CharField(max_length=30, choices=Action.choices)
    
    # Target
    target_type = models.CharField(max_length=50)  # e.g., 'user', 'post', 'reel'
    target_id = models.PositiveIntegerField()
    
    # Details
    details = models.JSONField(default=dict)
    notes = models.TextField(blank=True)
    
    # IP address (for security)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'audit_logs'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['moderator', '-created_at']),
            models.Index(fields=['action', '-created_at']),
        ]


class BannedWord(models.Model):
    """Words/phrases banned from content."""
    
    word = models.CharField(max_length=100, unique=True)
    is_regex = models.BooleanField(default=False)
    
    # Severity
    severity = models.PositiveSmallIntegerField(default=1)  # 1-3
    
    # Auto-action
    auto_flag = models.BooleanField(default=True)
    auto_hide = models.BooleanField(default=False)
    auto_delete = models.BooleanField(default=False)
    
    added_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'banned_words'


class ModerationStats(models.Model):
    """Daily moderation statistics."""
    
    date = models.DateField(unique=True)
    
    # Reports
    reports_received = models.PositiveIntegerField(default=0)
    reports_resolved = models.PositiveIntegerField(default=0)
    reports_dismissed = models.PositiveIntegerField(default=0)
    
    # Content
    content_approved = models.PositiveIntegerField(default=0)
    content_rejected = models.PositiveIntegerField(default=0)
    content_deleted = models.PositiveIntegerField(default=0)
    
    # Users
    users_banned = models.PositiveIntegerField(default=0)
    users_warned = models.PositiveIntegerField(default=0)
    
    # Average response time (in minutes)
    avg_response_time = models.PositiveIntegerField(default=0)
    
    class Meta:
        db_table = 'moderation_stats'
        ordering = ['-date']
