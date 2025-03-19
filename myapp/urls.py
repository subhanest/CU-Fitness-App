
from django.urls import path  # type: ignore

from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Home Page
    path('explore/', views.explore, name='explore'),  # Explore Page
    path('privacy-settings/', views.settings, name='settings'),  # Settings Page
    path('sign__up/', views.signup_view, name='sign__up'),  
    path('log__in/', views.login_view, name='log__in'),
    path('api/signup/', views.signup_view, name='api_signup'),
    path('api/login/', views.login_view, name='api_login'),
    path('chatbot/', views.chatbot_view, name='chatbot'),
]

