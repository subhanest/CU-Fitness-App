from django.shortcuts import render  # type: ignore
from django.utils.timezone import now  # type: ignore


# Create your views here.
def home(request):
    return render(request, 'myapp/index.html', {'timestamp': now().timestamp()})

def explore(request):
    return render(request, 'myApp/ER.html')  # Explore Page

def settings(request):
    return render(request, 'myApp/settings.html') # Settings Page
    
def signup_view(request):
    return render(request, 'myapp/sign__up.html')  # Sign up Page

def login_view(request):
    return render(request, 'myApp/log__in.html') # Login Page
