from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.db import IntegrityError
from .forms import RegistrationForm
from .models import User

def register_view(request):
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
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('home',{'user':user})
        else:
            # Handle invalid login
            return render(request, 'authentication/login.html', {'error': 'Invalid email or password'})
    return render(request, 'authentication/login.html')

def logout_view(request):
    logout(request)
    return redirect('home')

def user_list_view(request):
    users = User.objects.all()
    return render(request, 'authentication/user_list.html', {'users': users})