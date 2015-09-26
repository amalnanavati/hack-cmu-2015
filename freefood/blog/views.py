from django.shortcuts import render
from django.db import models
from django.shortcuts import render_to_response
from blog.models import posts
from django.http import HttpResponse

def index(request):
    # return render(request, 'blog/index.html', {})
    return HttpResponse("Hello, world. You're at the polls index.")
# Create your views here.