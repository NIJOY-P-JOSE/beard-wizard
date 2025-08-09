from django.shortcuts import render

# Create your views here.

def home(request):
    return render(request, 'home.html')

def trimm(request):
    return render(request, 'trimming_guide.html')