from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Product, PriceAlert
from django.db.models import Q
from django.contrib import messages


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
            product = Product(name=name, description=description, price=price, url=url)
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

@login_required
def add_to_watchlist(request, product_id):
    product = get_object_or_404(Product, product_id=product_id)
    request.user.watchlist.add(product)
    return render()

@login_required
def set_price_alert(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    price_threshold = request.POST.get('price_threshold')
    if price_threshold is not None and price_threshold.isdigit():
        price_threshold = float(price_threshold)
        PriceAlert.objects.create(
            user=request.user,
            product=product,
            price_threshold=price_threshold
            )
    else:
        return redirect('watchlist')
    
    return redirect('watchlist')

def all_products(request):
    products = Product.objects.all()
    return render(request, 'products/all_products.html', {'products': products})