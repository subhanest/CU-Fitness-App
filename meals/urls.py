from django.urls import path
from . import views  # Import views from the same app

urlpatterns = [
     path('', views.nutrition_index, name='nutrition_index'),
     path('chatbot/', views.chatbot_response, name='chatbot'),
     path('generate-meal-plan/', views.generate_meal_plan, name='generate_meal_plan'),
     path('edit-meal/<int:meal_id>/', views.edit_meal, name='edit_meal'),
]