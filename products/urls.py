from django.contrib import admin
from django.urls import path
from . import views

app_name='products'

urlpatterns = [
    path('search/', views.search_products, name='search_products'),
    path('view/<str:product_id>', views.view_product, name='view_product'),
    path('add_to_watchlist/<str:product_id>/', views.add_to_watchlist, name='add_to_watchlist'),
    path('set_price_alert/<str:product_id>/', views.set_price_alert, name='set_price_alert'),
    path('add/', views.add_product, name='add_product'),
    path('all/', views.all_products, name='all_products'),
]