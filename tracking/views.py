from django.shortcuts import render,redirect
from products.models import Product
from .models import ProductAlert, ProductHistory
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required
def track_product(request, product_id):
    product = Product.objects.get(id=product_id)
    if request.method == "POST":
        target_price = request.POST['target_price']
        ProductAlert.objects.create(user=request.user, product=product, target_price=target_price)
        return redirect('product_list')
    return render(request, 'tracker/track_product.html', {'product': product})

@login_required
def product_list(request):
    products = Product.objects.all()
    tracked_products = ProductAlert.objects.filter(user=request.user) if request.user.is_authenticated else []
    return render(request, 'tracker/tracked_procuducts.html', {
        'products': products,
        'tracked_products': tracked_products,
    })
