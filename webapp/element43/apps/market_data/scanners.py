# Create your views here.
from django.shortcuts import render_to_response
import psycopg2

def random(request):
    
    return render_to_response('market/randomscanner.haml')
