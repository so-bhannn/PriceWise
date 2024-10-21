from django.urls import path
from .views import register_view, login_view, logout_view, user_list_view

urlpatterns = [
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('users/', user_list_view, name='user_list'),
]