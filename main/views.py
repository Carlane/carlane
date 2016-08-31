from django.shortcuts import render

# Create your views here.

def home(request):
	return render(request, 'home.html')

def home_new(request):
	return render(request, 'home_new.html')
