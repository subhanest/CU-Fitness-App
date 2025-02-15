
from django.urls import path  # type: ignore

from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Home Page
    path('explore/', views.explore, name='explore'),  # Explore Page
    path('fitness/', views.fitness, name='fitness'),  # Fitness Page
    path('privacy-settings/', views.settings, name='settings'),  # Settings Page
    path('sign__up/', views.signup_view, name='sign__up'),  
    path('log__in/', views.login_view, name='log__in')
]

