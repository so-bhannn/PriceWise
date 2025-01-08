from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Product, WatchList, WatchListItem
from django.db.models import Q
from django.contrib import messages
from django.urls import reverse


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
def create_watchlist(request):
    if request.method=='POST':
        name=request.POST.get('name')
        watchlist = WatchList(user=request.user, name=name)
        watchlist.save()
        messages.success(request, 'Watchlist created successfully!')
        return redirect(reverse('home'))
    return render(request, 'products/create_watchlist.html')

@login_required
def add_to_watchlist(request):
    if request.method=='POST':
        product_id=request.POST.get('product_id')
        product=get_object_or_404(Product, product_id=product_id)
        watchlist_id=request.POST.get('watchlist_id')
        watchlist=get_object_or_404(WatchList, watchlist_id=watchlist_id)
        try:
            if product:
                watchlist_item=WatchListItem(watchlist=watchlist, product=product)
                watchlist_item.save()
                messages.success(request, 'Product added to watchlist successfully.')
        except Exception as e:
            messages.error(request, f'{e} An error occured while adding the product.')
            return redirect('products:view_watchlist', watchlist_id=watchlist_id)
    return redirect('products:view_product', product=product)

@login_required
def all_watchlists(request):
    watchlists= WatchList.objects.all()
    return render(request, 'products/all_watchlists.html', {'watchlists': watchlists})

@login_required
def view_watchlist(request,watchlist_id):
    watchlist=get_object_or_404(WatchList, watchlist_id=watchlist_id)
    watchlist_items=watchlist.items.all()
    watchlists= WatchList.objects.all()
    return render(request, 'products/view_watchlist.html', {'watchlist': watchlist, 'watchlist_items':watchlist_items, 'watchlists':watchlists})

@login_required
def remove_item(request):
    product_id=request.POST.get('item_id')
    watchlist_item = get_object_or_404(WatchListItem, product_id=product_id)
    watchlist_id = watchlist_item.watchlist_id
    try:
        watchlist_item.delete()
        messages.success(request, 'Item removed from watchlist successfully.')
    except Exception as e:
        messages.error(request, f"Failed to remove item. {e}")
    return redirect('products:view_watchlist', watchlist_id=watchlist_id)

@login_required
def remove_watchlist(request):
    watchlist_id=request.POST.get('watchlist_id')
    watchlist = get_object_or_404(WatchList, watchlist_id=watchlist_id)
    try:
        watchlist.delete()
        messages.success(request, 'Watchlist removed from watchlist successfully.')
    except Exception as e:
        messages.error(request, f"Failed to remove watchlist. {e}")
    return redirect('products:all_watchlists')


def all_products(request):
    products = Product.objects.all()
    watchlists=WatchList.objects.all()
    return render(request, 'products/all_products.html', {'products': products, 'watchlists':watchlists})

def tracked_items(request):
    pass