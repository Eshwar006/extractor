from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse


def fb_auth(request):
    return HttpResponse('<h1>New FB Auth Blog</h1>')