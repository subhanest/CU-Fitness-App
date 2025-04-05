from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)
from django.db import models
from django.utils import timezone


class CustomUserManager(BaseUserManager):
    """Custom user manager to handle email-based authentication instead of username."""
    
    def create_user(self, email, username, password=None, **extra_fields):
        """Create and save a regular user with the given email, username and password."""
        if not email:
            raise ValueError('The Email field must be set')
        if not username:
            raise ValueError('The Username field must be set')
        
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, username, password=None, **extra_fields):
        """Create and save a superuser with the given email, username and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        
        return self.create_user(email, username, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """Custom user model that supports using email instead of username for authentication."""
    
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=True)
    phone = models.CharField(max_length=15, blank=True, null=True)  # Optional phone number
    age = models.PositiveIntegerField(blank=True, null=True)  # Optional age
    gender = models.CharField(max_length=10, blank=True, null=True)  # Optional gender
    
    # Additional fields from the sign-up form
    receive_updates = models.BooleanField(default=False)
    
    # Required fields for Django's admin
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    
    objects = CustomUserManager()
    
    USERNAME_FIELD = 'email'  # Use email as the unique identifier
    REQUIRED_FIELDS = ['username']  # Required in addition to the email field when creating a superuser
    
    def __str__(self):
        return self.email


class UserSession(models.Model):
    """Model to track user sessions for the 'Remember Me' functionality."""
    
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    session_token = models.CharField(max_length=255)
    expires_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.email} - {self.created_at}"
    
    class Meta:
        verbose_name = "User Session"
        verbose_name_plural = "User Sessions"


class UserQuestionnaire(models.Model):
    """Model to store user responses to the fitness questionnaire."""
    
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='questionnaire')
    fitness_goals = models.CharField(max_length=255, default="General health")  # Required with default
    body_type = models.CharField(max_length=255, default="Average")  # Required with default
    daily_caloric_need = models.IntegerField(default=2000)  # Required with default
    workout_frequency = models.CharField(max_length=255, default="3 days/week, Moderate")  # Required with default
    macronutrient_ratio = models.CharField(max_length=255, default="Balanced")  # Required with default
    dietary_restrictions = models.CharField(max_length=255, default="None")  # Required with default
    sleep_hours = models.IntegerField(default=7)  # Required with default
    work_schedule = models.CharField(max_length=255, default="9-5 Job")  # Required with default
    supplements = models.CharField(max_length=255, default="None")  # Required with default
    water_intake = models.CharField(max_length=255, default="2 liters")  # Required with default
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Questionnaire for {self.user.username}"