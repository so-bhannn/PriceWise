from django.contrib import admin
from django.urls import path
from . import views

app_name='products'

urlpatterns = [
    path('search/', views.search_products, name='search_products'),
    path('view/<str:product_id>/', views.view_product, name='view_product'),
    path('add/', views.add_product, name='add_product'),
    path('all/', views.all_products, name='all_products'),
    path('tracked/', views.tracked_items, name='tracked_items'),
]