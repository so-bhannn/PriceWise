from django.shortcuts import render,redirect, get_object_or_404
from django.urls import reverse
from .models import WatchList, WatchListItem
from products.models import Product
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def create_watchlist(request):
    if request.method=='POST':
        name=request.POST.get('name')
        watchlist = WatchList(user=request.user, name=name)
        watchlist.save()
        messages.success(request, 'Watchlist created successfully!')
        return redirect(reverse('home'))
    return render(request, 'watchlist/create_watchlist.html')

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
            return redirect('watchlist:view_watchlist', watchlist_id=watchlist_id)
    return redirect('products:view_product', product=product)

@login_required
def all_watchlists(request):
    watchlists= WatchList.objects.all()
    return render(request, 'watchlist/all_watchlists.html', {'watchlists': watchlists})

@login_required
def view_watchlist(request,watchlist_id):
    watchlist=get_object_or_404(WatchList, watchlist_id=watchlist_id)
    watchlist_items=watchlist.items.all()
    watchlists= WatchList.objects.all()
    return render(request, 'watchlist/view_watchlist.html', {'watchlist': watchlist, 'watchlist_items':watchlist_items, 'watchlists':watchlists})

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
    return redirect('watchlist:view_watchlist', watchlist_id=watchlist_id)

@login_required
def remove_watchlist(request):
    watchlist_id=request.POST.get('watchlist_id')
    watchlist = get_object_or_404(WatchList, watchlist_id=watchlist_id)
    try:
        watchlist.delete()
        messages.success(request, 'Watchlist removed from watchlist successfully.')
    except Exception as e:
        messages.error(request, f"Failed to remove watchlist. {e}")
    return redirect('watchlist:all_watchlists')