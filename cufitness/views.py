from django.http import HttpResponse
from django.shortcuts import render

def home(request):
    return HttpResponse("Hello, this is CUFitness!")
def explore(request):
    return render(request, 'ER.html')
