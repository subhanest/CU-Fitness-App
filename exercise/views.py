
from django.shortcuts import render

def fitness(request):
    return render(request, 'exercise/index.html')
