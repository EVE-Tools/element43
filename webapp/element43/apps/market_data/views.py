# Create your views here.
from django.shortcuts import render_to_response

def home(request):
    return render_to_response('home.html')

def home-test(request):
    return render_to_response('home-test.html')
