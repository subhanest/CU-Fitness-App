from django.contrib import admin
from django.urls import path, include
from exercise import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'workout-plans', views.WorkoutPlanViewSet)
router.register(r'nutrition-plans', views.NutritionPlanViewSet)
router.register(r'progress-trackers', views.ProgressTrackerViewSet)
router.register(r'user-profiles', views.UserProfileViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('myapp.urls')),
    path('explore/', include('allapps.urls')),

    # ✅ This brings back your /fitness/ homepage
    path('fitness/', views.home, name='fitness-home'),

    # ✅ APIs (ViewSets)
    path('api/', include(router.urls)),

    # ✅ Function-based APIs (chart, log, progress, chatbot)
    path('api/', include('exercise.urls')),

    # ✅ For workout and meal recommendation
    path('workout/', include('exercise.urls')),
    path('meal/', include('exercise.urls')),
]
