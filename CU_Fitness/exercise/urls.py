from django.urls import path, include
from rest_framework.routers import DefaultRouter
from exercise import views  
from .views import WorkoutLogAPIView
from .views import WorkoutProgressAPIView
from .views import WorkoutChartDataAPIView

# API router for ViewSets
router = DefaultRouter()
router.register(r'workout-plans', views.WorkoutPlanViewSet, basename="workoutplan")
router.register(r'nutrition-plans', views.NutritionPlanViewSet, basename="nutritionplan")
router.register(r'progress-trackers', views.ProgressTrackerViewSet, basename="progresstracker")
router.register(r'user-profiles', views.UserProfileViewSet, basename="userprofile")

urlpatterns = [
    path('', views.home, name='home'),  # ✅ Home Page
    path('api/', include(router.urls)),  # ✅ Include ViewSet API routes

    # ✅ AI Adaptive Workouts & Meal Plans
    path('workout/recommend/', views.get_workout_recommendation, name='workout-recommend'),
    path('meal/recommend/', views.get_meal_recommendation, name='meal-recommend'),

    # ✅ AI Chatbot API
    path('api/ai_chatbot/', views.ai_chatbot, name='ai-chatbot'),

    path('api/log_workout/', WorkoutLogAPIView.as_view(), name='log_workout'),
     path('api/workout_progress/', WorkoutProgressAPIView.as_view(), name='workout_progress'),
     path('api/workout_chart/', WorkoutChartDataAPIView.as_view(), name='workout_chart'),
]
