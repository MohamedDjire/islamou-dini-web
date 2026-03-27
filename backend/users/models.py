"""
Custom User model for IslamouDini
"""

from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class UserManager(BaseUserManager):
    """Custom user manager for email-based authentication."""
    
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('L\'email est obligatoire')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'admin')
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    """
    Custom User model for IslamouDini.
    Uses email as primary identifier.
    """
    
    class Role(models.TextChoices):
        USER = 'user', 'Utilisateur'
        FORMATEUR = 'formateur', 'Formateur'
        MODERATEUR = 'moderateur', 'Moderateur'
        ADMIN = 'admin', 'Administrateur'
    
    class Gender(models.TextChoices):
        MALE = 'male', 'Homme'
        FEMALE = 'female', 'Femme'
        NOT_SPECIFIED = 'not_specified', 'Non specifie'
    
    # Override email to be unique and required
    email = models.EmailField(unique=True, verbose_name='Email')
    username = models.CharField(max_length=150, unique=True, blank=True)
    
    # Profile information
    full_name = models.CharField(max_length=255, blank=True, verbose_name='Nom complet')
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name='Telephone')
    bio = models.TextField(blank=True, null=True, max_length=500, verbose_name='Biographie')
    avatar = models.URLField(blank=True, null=True, verbose_name='Photo de profil')
    cover_image = models.URLField(blank=True, null=True, verbose_name='Image de couverture')
    gender = models.CharField(max_length=20, choices=Gender.choices, default=Gender.NOT_SPECIFIED)
    date_of_birth = models.DateField(null=True, blank=True, verbose_name='Date de naissance')
    location = models.CharField(max_length=255, blank=True, null=True, verbose_name='Localisation')
    
    # Role and permissions
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.USER)
    is_verified = models.BooleanField(default=False, verbose_name='Verifie')
    is_formateur_approved = models.BooleanField(default=False, verbose_name='Formateur approuve')
    
    # Privacy settings
    is_profile_public = models.BooleanField(default=True, verbose_name='Profil public')
    show_email = models.BooleanField(default=False, verbose_name='Afficher email')
    allow_messages = models.BooleanField(default=True, verbose_name='Autoriser messages')
    
    # Notification preferences
    email_notifications = models.BooleanField(default=True, verbose_name='Notifications email')
    push_notifications = models.BooleanField(default=True, verbose_name='Notifications push')
    
    # Stats
    followers_count = models.PositiveIntegerField(default=0)
    following_count = models.PositiveIntegerField(default=0)
    formations_count = models.PositiveIntegerField(default=0)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_active = models.DateTimeField(null=True, blank=True)
    
    # Use email as the username field for authentication
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    objects = UserManager()
    
    class Meta:
        db_table = 'users'
        verbose_name = 'Utilisateur'
        verbose_name_plural = 'Utilisateurs'
        ordering = ['-created_at']
    
    def save(self, *args, **kwargs):
        if not self.username:
            # Generate username from email
            base_username = self.email.split('@')[0]
            username = base_username
            counter = 1
            while User.objects.filter(username=username).exclude(pk=self.pk).exists():
                username = f"{base_username}{counter}"
                counter += 1
            self.username = username
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.full_name or self.email
    
    @property
    def is_formateur(self):
        return self.role in [self.Role.FORMATEUR, self.Role.ADMIN]
    
    @property
    def is_moderateur(self):
        return self.role in [self.Role.MODERATEUR, self.Role.ADMIN]


class UserFollow(models.Model):
    """Model for user follow relationships."""
    follower = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='following'
    )
    following = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='followers'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'user_follows'
        unique_together = ('follower', 'following')
        verbose_name = 'Abonnement'
        verbose_name_plural = 'Abonnements'
    
    def __str__(self):
        return f"{self.follower} suit {self.following}"


class UserBlock(models.Model):
    """Model for blocking users."""
    blocker = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='blocking'
    )
    blocked = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='blocked_by'
    )
    reason = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'user_blocks'
        unique_together = ('blocker', 'blocked')
        verbose_name = 'Blocage'
        verbose_name_plural = 'Blocages'
