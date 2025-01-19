from django.contrib import admin
from django.urls import path
from . import views

app_name='tracking'

urlpatterns = [
    path('track-product/<str:id>', views.track_product, name='track_product'),
    path('product-list/', views.product_list, name='product_list'),
]
