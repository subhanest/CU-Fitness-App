from django.contrib import admin
from .models import WorkoutPlan, NutritionPlan, ProgressTracker, UserProfile

# Customize admin interface for WorkoutPlan
class WorkoutPlanAdmin(admin.ModelAdmin):
    list_display = ['name', 'goal', 'created_at']
    search_fields = ['name', 'goal']
    list_filter = ['goal']  # You can filter by 'goal', e.g., 'muscle_gain', 'weight_loss'

# Customize admin interface for NutritionPlan
class NutritionPlanAdmin(admin.ModelAdmin):
    list_display = ['meal_type', 'meal_name', 'calories', 'protein', 'carbs', 'fats', 'created_at']
    search_fields = ['meal_name', 'meal_type']
    list_filter = ['meal_type']  # You can filter by meal type like breakfast, lunch, dinner

# Customize admin interface for ProgressTracker
class ProgressTrackerAdmin(admin.ModelAdmin):
    list_display = ['user', 'weight', 'body_fat_percentage', 'muscle_mass', 'created_at']
    search_fields = ['user__username']  # Allows search by user's username
    list_filter = ['user']  # You can filter progress by user

# Customize admin interface for UserProfile
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'age', 'fitness_level', 'goal', 'created_at']
    search_fields = ['user__username', 'fitness_level', 'goal']
    list_filter = ['fitness_level', 'goal']  # Filter by fitness level and goal

# Register models in admin with customizations
admin.site.register(WorkoutPlan, WorkoutPlanAdmin)
admin.site.register(NutritionPlan, NutritionPlanAdmin)
admin.site.register(ProgressTracker, ProgressTrackerAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
