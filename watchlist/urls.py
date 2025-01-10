from django.contrib import admin
from django.urls import path
from . import views

app_name='watchlist'

urlpatterns = [
    path('create/', views.create_watchlist, name='create_watchlist'),
    path('all/', views.all_watchlists, name='all_watchlists'),
    path('add/', views.add_to_watchlist, name='add_to_watchlist'),
    path('view/<str:watchlist_id>/', views.view_watchlist, name='view_watchlist'),
    path('remove_item/', views.remove_item, name='remove_item'),
    path('remove/', views.remove_watchlist, name='remove_watchlist'),
]
