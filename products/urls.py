from django.contrib import admin
from django.urls import path
from . import views

app_name='products'

urlpatterns = [
    path('search/', views.search_products, name='search_products'),
    path('view/<str:product_id>', views.view_product, name='view_product'),
    path('add_to_watchlist/<str:product_id>/', views.add_to_watchlist, name='add_to_watchlist'),
    path('add/', views.add_product, name='add_product'),
    path('all/', views.all_products, name='all_products'),
    path('create_watchlist/', views.create_watchlist, name='create_watchlist'),
    path('all_watchlists/', views.all_watchlists, name='all_watchlists'),
    path('add_to_watchlist/', views.add_to_watchlist, name='add_to_watchlist'),
    path('view_watchlist/<str:watchlist_id>', views.view_watchlist, name='view_watchlist'),
    path('remove_item/', views.remove_item, name='remove_item'),
    path('remove_watchlist/', views.remove_watchlist, name='remove_watchlist')
]