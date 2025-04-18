from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)
from django.db import models
from django.utils import timezone

from django.conf import settings


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
    
    fitness_goals = models.CharField(
    max_length=50,
    choices=[
        ('lose', 'Lose Weight'),
        ('maintain', 'Maintain Weight'),
        ('gain', 'Gain Weight')
    ],
    default='maintain'
        )
    body_type = models.CharField(max_length=255, default="Average")  # Required with default
    
    workout_frequency = models.CharField(max_length=255, default="3 days/week, Moderate")  # Required with default
   
    macronutrient_ratio = models.CharField(
    max_length=50,
    choices=[
        ('balanced', 'Balanced'),
        ('high_protein', 'High Protein'),
        ('low_carb', 'Low Carb'),
        ('low_fat', 'Low Fat')
    ],
    default='balanced'
            ) 
    activity_level = models.CharField(
    max_length=50,
    choices=[
        ('sedentary', 'Sedentary'),
        ('light', 'Lightly active'),
        ('moderate', 'Moderately active'),
        ('active', 'Active'),
        ('very_active', 'Very active')
    ],
    default='moderate'
         )

    cooking_time = models.IntegerField(null=True, blank=True)

    diet = models.CharField(max_length=50, default="omnivore")
    
    intolerances = models.TextField(blank=True, default="")  # Comma-separated values

    daily_budget = models.FloatField(null=True, blank=True)

    target_calories = models.IntegerField(null=True, blank=True)
    height = models.FloatField(default=170.0, help_text="Height in cm")  # or any reasonable default
    current_weight = models.FloatField(null=True, blank=True)
    target_weight = models.FloatField(null=True, blank=True)
    dietary_restrictions = models.CharField(max_length=255, default="None")  # Required with default
    sleep_hours = models.IntegerField(default=7)  # Required with default
    work_schedule = models.CharField(max_length=255, default="9-5 Job")  # Required with default
    supplements = models.CharField(max_length=255, default="None")  # Required with default
    water_intake = models.CharField(max_length=255, default="2 liters")  # Required with default
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Questionnaire for {self.user.username}"
    
class MealLog(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    food_name = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField(default=1)
    meal_type = models.CharField(max_length=50, choices=[
        ('breakfast', 'Breakfast'),
        ('lunch', 'Lunch'),
        ('dinner', 'Dinner'),
        ('snack', 'Snack')
    ])
    time = models.TimeField()
    date = models.DateField(default=timezone.now)
    calories = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.food_name} ({self.date})"
