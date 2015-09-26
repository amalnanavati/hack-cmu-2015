from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def index(request):
    return HttpResponse("Food For Grabs!")

def detail(request, event_id):
    return HttpResponse("You're looking at event %s." % event_id)

