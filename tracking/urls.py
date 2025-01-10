from django.contrib import admin
from django.urls import path
from . import views

app_name='tracking'

urlpatterns = [
    path('', views.track, name='tracker')
]
