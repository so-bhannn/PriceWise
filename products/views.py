from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Product,PriceAlert
from django.db.models import Q

def view_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'product.html', {'product': product})

def search_products(request):
    query = request.GET.get('q')
    products = Product.objects.filter(
        Q(name__icontains=query) | Q(description__icontains=query) | Q(price__icontains=query) | Q(url__icontains=query)
    ) if query else Product.objects.none()
    return render(request, 'search_results.html', {'products': products})

@login_required
def add_to_watchlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    request.user.watchlist.add(product)
    return redirect('watchlist')

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