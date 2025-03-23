from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from exercise import views  # Import views from exercise app

# Create a router for the viewsets
router = DefaultRouter()
router.register(r'workout-plans', views.WorkoutPlanViewSet)
router.register(r'nutrition-plans', views.NutritionPlanViewSet)
router.register(r'progress-trackers', views.ProgressTrackerViewSet)
router.register(r'user-profiles', views.UserProfileViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),  # ✅ Keep this ONLY here
    path('api/', include(router.urls)),  # ✅ API endpoints
    path('', include('exercise.urls')),  # ✅ Includes workout & meal routes
]
