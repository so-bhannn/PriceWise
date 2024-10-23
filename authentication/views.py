"""
views.py

This module contains view functions for handling user 
registration, authentication,and other user-related actions.

Functions:
    register_view(request): Handle user registration.
"""

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.db import IntegrityError
from django.contrib import messages
from .forms import RegistrationForm
from .models import User

def register_view(request):
    """
    Handle user registration.

    If the request method is POST, validate the form data and create a new user.
    Authenticate and log in the user if registration is successful.
    If the request method is GET, display the registration form.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The HTTP response object with the rendered registration template.
    """
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            try:
                # Create the user 
                user = User.objects.create_user(
                    email=form.cleaned_data.get('email'),
                    username=form.cleaned_data.get('username'),
                    password=form.cleaned_data.get('password1')
                )
                # Authenticate the user
                user = authenticate(email=form.cleaned_data.get('email'), password=form.cleaned_data.get('password1'))
                if user is not None:
                    # Log in the user
                    login(request, user)
                    return redirect('home')
            except IntegrityError:
                form.add_error(None, 'A user with that email or username already exists.')
    else:
        form = RegistrationForm()
    return render(request, 'authentication/register.html', {'form': form})

def login_view(request):
    """
    Handle user login.

    If the request method is POST, authenticate the user with the provided email and password.
    Log in the user if authentication is successful.
    If the request method is GET, display the login form.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The HTTP response object with the rendered login template.
    """
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            # Handle invalid login
            messages.error(request, 'Invalid email or password.')
            return render(request, 'authentication/login.html')
    return render(request, 'authentication/login.html')

def logout_view(request):
    """
    Handle user logout.

    Log out the user and redirect to the home page.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The HTTP response object redirecting to the home page.
    """
    logout(request)
    return redirect('home')

def user_list_view(request):
    """
    Display a list of all users.
    """
    users = User.objects.all()
    return render(request, 'authentication/user_list.html', {'users': users})

# End-of-file (EOF)