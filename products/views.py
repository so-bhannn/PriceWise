from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Product
from watchlist.models import WatchList
from django.db.models import Q
from django.contrib import messages
from django.views.generic import View, ListView


def add_product(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        url = request.POST.get('url')

        if not name or not description or not price or not url:
            messages.error(request, 'All fields are required.')
            return render(request, 'products/add_product.html')

        try:
            price = float(price)
        except ValueError:
            messages.error(request, 'Invalid price format.')
            return render(request, 'products/add_product.html')

        try:
            product = Product(name=name, description=description, current_price=price, url=url)
            product.save()
            messages.success(request, 'Product added successfully!')
            return redirect('home')
        except Exception as e:
            messages.error(request, 'An error occurred while adding the product.')
            return render(request, 'products/add_product.html')
    return render(request, 'products/add_product.html')

def view_product(request, product_id):
    product = get_object_or_404(Product, product_id=product_id)
    return render(request, 'products/view_product.html', {'product': product})

def search_products(request):
    query = request.GET.get('q')
    products = Product.objects.filter(
        Q(name__icontains=query) | Q(description__icontains=query) | Q(price__icontains=query) | Q(url__icontains=query)
    ) if query else Product.objects.none()
    return render(request, 'products/search_results.html', {'products': products})

def all_products(request):
    products = Product.objects.all()
    watchlists=WatchList.objects.all()
    return render(request, 'products/all_products.html', {'products': products, 'watchlists':watchlists})

def tracked_items(request):
    pass