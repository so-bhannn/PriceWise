from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from tracking.models import Product, PriceHistory, UserTracking
from .utils import fetch_product_price

class Command(BaseCommand):
    help = "Update product prices and notify users if target price is met"

    def handle(self, *args, **kwargs):
        products = Product.objects.all()
        for product in products:
            new_price = fetch_product_price(product.url)
            if new_price and new_price != product.current_price:
                product.current_price = new_price
                product.save()
                PriceHistory.objects.create(product=product, price=new_price)
                
                # Notify users if target price is met
                user_trackings = UserTracking.objects.filter(product=product, target_price__gte=new_price)
                for tracking in user_trackings:
                    self.send_notification(tracking.user.email, product, new_price)

    def send_notification(self, email, product, price):
        subject = f"Price Alert: {product.name}"
        message = f"The price of {product.name} has dropped to ${price}.\nCheck it here: {product.url}"
        send_mail(subject, message, 'noreply@pricetracker.com', [email])
