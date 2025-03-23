"""
URL configuration for cufitness project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
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
