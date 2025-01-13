from django.contrib import admin
from django.urls import path
from . import views

app_name='tracking'

urlpatterns = [
    path('send_email/', views.send_email, name='send_email')
]
