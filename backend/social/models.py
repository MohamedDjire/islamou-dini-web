"""
Social models for IslamouDini
Includes: Posts, Reels, Comments, Likes, Shares
"""

from django.db import models
from django.conf import settings


class Post(models.Model):
    """Posts/Publications model."""
    
    class Status(models.TextChoices):
        DRAFT = 'draft', 'Brouillon'
        PENDING = 'pending', 'En attente'
        PUBLISHED = 'published', 'Publie'
        REJECTED = 'rejected', 'Rejete'
        ARCHIVED = 'archived', 'Archive'
    
    class Visibility(models.TextChoices):
        PUBLIC = 'public', 'Public'
        FOLLOWERS = 'followers', 'Abonnes uniquement'
        PRIVATE = 'private', 'Prive'
    
    # Author
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='posts'
    )
    
    # Content
    content = models.TextField(max_length=5000, verbose_name='Contenu')
    
    # Settings
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PUBLISHED)
    visibility = models.CharField(max_length=20, choices=Visibility.choices, default=Visibility.PUBLIC)
    
    # Allow comments
    allow_comments = models.BooleanField(default=True)
    
    # Stats
    likes_count = models.PositiveIntegerField(default=0)
    comments_count = models.PositiveIntegerField(default=0)
    shares_count = models.PositiveIntegerField(default=0)
    views_count = models.PositiveIntegerField(default=0)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'posts'
        verbose_name = 'Publication'
        verbose_name_plural = 'Publications'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Post by {self.author} - {self.created_at}"


class PostMedia(models.Model):
    """Media attachments for posts."""
    
    class Type(models.TextChoices):
        IMAGE = 'image', 'Image'
        VIDEO = 'video', 'Video'
        DOCUMENT = 'document', 'Document'
    
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='media'
    )
    type = models.CharField(max_length=20, choices=Type.choices)
    url = models.URLField(verbose_name='URL')
    thumbnail_url = models.URLField(blank=True, null=True)
    order = models.PositiveIntegerField(default=0)
    
    # For videos
    duration_seconds = models.PositiveIntegerField(default=0)
    
    # Metadata
    width = models.PositiveIntegerField(default=0)
    height = models.PositiveIntegerField(default=0)
    file_size = models.PositiveIntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'post_media'
        ordering = ['order']


class Reel(models.Model):
    """Short-form video content (Reels)."""
    
    class Status(models.TextChoices):
        PROCESSING = 'processing', 'En traitement'
        PENDING = 'pending', 'En attente de validation'
        PUBLISHED = 'published', 'Publie'
        REJECTED = 'rejected', 'Rejete'
        ARCHIVED = 'archived', 'Archive'
    
    # Author
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reels'
    )
    
    # Content
    caption = models.TextField(max_length=2000, blank=True, verbose_name='Description')
    
    # Video
    video_url = models.URLField(verbose_name='URL Video')
    video_hls_url = models.URLField(blank=True, null=True)
    thumbnail_url = models.URLField(blank=True, null=True)
    duration_seconds = models.PositiveIntegerField(default=0)
    
    # Audio (if separate)
    audio_name = models.CharField(max_length=255, blank=True, null=True)
    audio_author = models.CharField(max_length=255, blank=True, null=True)
    
    # Settings
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PROCESSING)
    allow_comments = models.BooleanField(default=True)
    allow_duet = models.BooleanField(default=True)
    
    # Stats
    likes_count = models.PositiveIntegerField(default=0)
    comments_count = models.PositiveIntegerField(default=0)
    shares_count = models.PositiveIntegerField(default=0)
    views_count = models.PositiveIntegerField(default=0)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'reels'
        verbose_name = 'Reel'
        verbose_name_plural = 'Reels'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Reel by {self.author} - {self.created_at}"


class Comment(models.Model):
    """Comments on posts and reels."""
    
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    
    # Polymorphic: can be on post or reel
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='comments'
    )
    reel = models.ForeignKey(
        Reel,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='comments'
    )
    
    # Parent comment (for replies/threads)
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='replies'
    )
    
    # Content
    content = models.TextField(max_length=1000)
    
    # Stats
    likes_count = models.PositiveIntegerField(default=0)
    replies_count = models.PositiveIntegerField(default=0)
    
    # Status
    is_edited = models.BooleanField(default=False)
    is_hidden = models.BooleanField(default=False)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'comments'
        verbose_name = 'Commentaire'
        verbose_name_plural = 'Commentaires'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Comment by {self.author} on {self.post or self.reel}"


class Like(models.Model):
    """Likes on posts, reels, and comments."""
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='likes'
    )
    
    # Polymorphic: can be on post, reel, or comment
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='likes'
    )
    reel = models.ForeignKey(
        Reel,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='likes'
    )
    comment = models.ForeignKey(
        Comment,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='likes'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'likes'
        verbose_name = 'Like'
        verbose_name_plural = 'Likes'
        # Ensure one like per user per content
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'post'],
                condition=models.Q(post__isnull=False),
                name='unique_post_like'
            ),
            models.UniqueConstraint(
                fields=['user', 'reel'],
                condition=models.Q(reel__isnull=False),
                name='unique_reel_like'
            ),
            models.UniqueConstraint(
                fields=['user', 'comment'],
                condition=models.Q(comment__isnull=False),
                name='unique_comment_like'
            ),
        ]


class Bookmark(models.Model):
    """Bookmarked/saved content."""
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='social_bookmarks'
    )
    
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='bookmarks'
    )
    reel = models.ForeignKey(
        Reel,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='bookmarks'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'social_bookmarks'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'post'],
                condition=models.Q(post__isnull=False),
                name='unique_post_bookmark'
            ),
            models.UniqueConstraint(
                fields=['user', 'reel'],
                condition=models.Q(reel__isnull=False),
                name='unique_reel_bookmark'
            ),
        ]


class Share(models.Model):
    """Track content shares."""
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='shares'
    )
    
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='shares'
    )
    reel = models.ForeignKey(
        Reel,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='shares'
    )
    
    # Where was it shared
    platform = models.CharField(max_length=50, blank=True)  # whatsapp, twitter, etc.
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'shares'


class Hashtag(models.Model):
    """Hashtags for posts and reels."""
    
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)
    posts_count = models.PositiveIntegerField(default=0)
    reels_count = models.PositiveIntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'hashtags'
        ordering = ['-posts_count', '-reels_count']
    
    def __str__(self):
        return f"#{self.name}"


class PostHashtag(models.Model):
    """Many-to-many relationship between posts and hashtags."""
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='hashtags')
    hashtag = models.ForeignKey(Hashtag, on_delete=models.CASCADE, related_name='posts')
    
    class Meta:
        db_table = 'post_hashtags'
        unique_together = ('post', 'hashtag')


class ReelHashtag(models.Model):
    """Many-to-many relationship between reels and hashtags."""
    reel = models.ForeignKey(Reel, on_delete=models.CASCADE, related_name='hashtags')
    hashtag = models.ForeignKey(Hashtag, on_delete=models.CASCADE, related_name='reels')
    
    class Meta:
        db_table = 'reel_hashtags'
        unique_together = ('reel', 'hashtag')
