from django.shortcuts import render  # type: ignore
from django.utils.timezone import now  # type: ignore


# Create your views here.
def home(request):
    return render(request, 'myapp/index.html', {'timestamp': now().timestamp()})

def explore(request):
    return render(request, 'myApp/explore.html')  # Explore Page

def fitness(request):
    return render(request, 'myApp/fitness.html')  # Fitness Page

def nutrition(request):
    return render(request, 'myApp/nutrition.html')# Nutrition Page

def settings(request):
    return render(request, 'myApp/settings.html') # Settings Page