from . import views

from django.urls import path

urlpatterns = [
    path('', views.fb_auth, 'fb-auth'),
]
