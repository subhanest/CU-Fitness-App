from django.shortcuts import render

# Create your views here.
def nutrition_index (request):
    return render(request, 'meals/nutrition_index.html')