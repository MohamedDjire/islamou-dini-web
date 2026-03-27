"""
Formations models for IslamouDini
Includes: Categories, Formations, Modules, Resources, Progress
"""

from django.db import models
from django.conf import settings


class Category(models.Model):
    """Categories for formations (e.g., Coran, Fiqh, Aqida, etc.)"""
    name = models.CharField(max_length=100, verbose_name='Nom')
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True, null=True)
    icon = models.CharField(max_length=50, blank=True, null=True)
    color = models.CharField(max_length=7, default='#10B981')  # Hex color
    parent = models.ForeignKey(
        'self', 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True,
        related_name='subcategories'
    )
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'categories'
        verbose_name = 'Categorie'
        verbose_name_plural = 'Categories'
        ordering = ['order', 'name']
    
    def __str__(self):
        return self.name


class Formation(models.Model):
    """Main Formation/Course model."""
    
    class Level(models.TextChoices):
        BEGINNER = 'beginner', 'Debutant'
        INTERMEDIATE = 'intermediate', 'Intermediaire'
        ADVANCED = 'advanced', 'Avance'
    
    class Status(models.TextChoices):
        DRAFT = 'draft', 'Brouillon'
        PENDING = 'pending', 'En attente de validation'
        PUBLISHED = 'published', 'Publie'
        ARCHIVED = 'archived', 'Archive'
    
    # Basic info
    title = models.CharField(max_length=255, verbose_name='Titre')
    slug = models.SlugField(unique=True)
    description = models.TextField(verbose_name='Description')
    short_description = models.CharField(max_length=300, blank=True)
    
    # Media
    thumbnail = models.URLField(blank=True, null=True, verbose_name='Miniature')
    preview_video = models.URLField(blank=True, null=True, verbose_name='Video de presentation')
    
    # Classification
    category = models.ForeignKey(
        Category, 
        on_delete=models.SET_NULL, 
        null=True,
        related_name='formations'
    )
    level = models.CharField(max_length=20, choices=Level.choices, default=Level.BEGINNER)
    tags = models.JSONField(default=list, blank=True)
    
    # Author
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='created_formations'
    )
    
    # Settings
    is_free = models.BooleanField(default=True, verbose_name='Gratuit')
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    duration_minutes = models.PositiveIntegerField(default=0, verbose_name='Duree (minutes)')
    
    # Status
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.DRAFT)
    is_featured = models.BooleanField(default=False, verbose_name='Mise en avant')
    
    # Stats
    students_count = models.PositiveIntegerField(default=0)
    views_count = models.PositiveIntegerField(default=0)
    rating_average = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    rating_count = models.PositiveIntegerField(default=0)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'formations'
        verbose_name = 'Formation'
        verbose_name_plural = 'Formations'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
    
    @property
    def modules_count(self):
        return self.modules.count()


class Module(models.Model):
    """Module/Chapter within a Formation."""
    
    formation = models.ForeignKey(
        Formation,
        on_delete=models.CASCADE,
        related_name='modules'
    )
    title = models.CharField(max_length=255, verbose_name='Titre')
    description = models.TextField(blank=True, null=True)
    order = models.PositiveIntegerField(default=0)
    
    # Video content
    video_url = models.URLField(blank=True, null=True, verbose_name='URL Video')
    video_hls_url = models.URLField(blank=True, null=True, verbose_name='URL HLS')
    duration_seconds = models.PositiveIntegerField(default=0)
    thumbnail = models.URLField(blank=True, null=True)
    
    # Settings
    is_free_preview = models.BooleanField(default=False, verbose_name='Apercu gratuit')
    is_published = models.BooleanField(default=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'formation_modules'
        verbose_name = 'Module'
        verbose_name_plural = 'Modules'
        ordering = ['order']
    
    def __str__(self):
        return f"{self.formation.title} - {self.title}"


class ModuleChapter(models.Model):
    """Chapters/timestamps within a Module video."""
    
    module = models.ForeignKey(
        Module,
        on_delete=models.CASCADE,
        related_name='chapters'
    )
    title = models.CharField(max_length=255)
    timestamp_seconds = models.PositiveIntegerField(default=0)
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        db_table = 'module_chapters'
        ordering = ['order', 'timestamp_seconds']


class Resource(models.Model):
    """Downloadable resources attached to formations or modules."""
    
    class Type(models.TextChoices):
        PDF = 'pdf', 'PDF'
        DOCUMENT = 'document', 'Document'
        AUDIO = 'audio', 'Audio'
        LINK = 'link', 'Lien externe'
        OTHER = 'other', 'Autre'
    
    title = models.CharField(max_length=255, verbose_name='Titre')
    description = models.TextField(blank=True, null=True)
    type = models.CharField(max_length=20, choices=Type.choices, default=Type.PDF)
    file_url = models.URLField(verbose_name='URL du fichier')
    file_size = models.PositiveIntegerField(default=0, help_text='Taille en octets')
    
    # Can be attached to formation or module
    formation = models.ForeignKey(
        Formation,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='resources'
    )
    module = models.ForeignKey(
        Module,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='resources'
    )
    
    order = models.PositiveIntegerField(default=0)
    download_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'resources'
        verbose_name = 'Ressource'
        verbose_name_plural = 'Ressources'
        ordering = ['order']


class Enrollment(models.Model):
    """User enrollment in a formation."""
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='enrollments'
    )
    formation = models.ForeignKey(
        Formation,
        on_delete=models.CASCADE,
        related_name='enrollments'
    )
    
    # Progress
    progress_percent = models.PositiveIntegerField(default=0)
    last_module = models.ForeignKey(
        Module,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    last_position_seconds = models.PositiveIntegerField(default=0)
    
    # Status
    is_completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    # Timestamps
    enrolled_at = models.DateTimeField(auto_now_add=True)
    last_accessed = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'enrollments'
        unique_together = ('user', 'formation')
        verbose_name = 'Inscription'
        verbose_name_plural = 'Inscriptions'


class ModuleProgress(models.Model):
    """Track user progress per module."""
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='module_progress'
    )
    module = models.ForeignKey(
        Module,
        on_delete=models.CASCADE,
        related_name='user_progress'
    )
    enrollment = models.ForeignKey(
        Enrollment,
        on_delete=models.CASCADE,
        related_name='module_progress'
    )
    
    # Progress tracking
    watch_time_seconds = models.PositiveIntegerField(default=0)
    last_position_seconds = models.PositiveIntegerField(default=0)
    is_completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'module_progress'
        unique_together = ('user', 'module')


class FormationRating(models.Model):
    """User ratings and reviews for formations."""
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='formation_ratings'
    )
    formation = models.ForeignKey(
        Formation,
        on_delete=models.CASCADE,
        related_name='ratings'
    )
    
    rating = models.PositiveSmallIntegerField()  # 1-5
    review = models.TextField(blank=True, null=True)
    
    is_approved = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'formation_ratings'
        unique_together = ('user', 'formation')
        verbose_name = 'Evaluation'
        verbose_name_plural = 'Evaluations'


class FormationBookmark(models.Model):
    """Bookmarked/saved formations."""
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='bookmarked_formations'
    )
    formation = models.ForeignKey(
        Formation,
        on_delete=models.CASCADE,
        related_name='bookmarks'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'formation_bookmarks'
        unique_together = ('user', 'formation')
