from django.shortcuts import render
# Create your views here.

def home(request):
    return render(request, 'pricewise/home.html')

def under_construction(request):
    return render(request, 'pricewise/under-construction.html')