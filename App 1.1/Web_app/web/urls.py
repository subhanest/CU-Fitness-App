from django.urls import path
from .views import SignUpView, LogInView,signup_view, login_view

urlpatterns = [
    path('sign_up/', signup_view, name='sign_up'),  
    path('log_in/', login_view, name='log_in'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', LogInView.as_view(), name='login'),
]