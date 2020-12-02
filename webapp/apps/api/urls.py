from django.urls import path
from . import views


urlpatterns = [
    path('extract', views.ExtractObjects.as_view(), name='object-extraction')
]