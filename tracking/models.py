from django.db import models
from products.models import Product
from django.conf import settings

# Create your models here.
class ProductHistory(models.Model):
    product=models.ForeignKey(Product, related_name="price_history", on_delete=models.CASCADE)
    price=models.DecimalField(max_digits=10, decimal_places=2)
    timestamp=models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering=['-timestamp']

class ProductAlert(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product=models.ForeignKey(Product, on_delete=models.CASCADE)
    target_price=models.DecimalField(max_digits=10, decimal_places=2)
    is_active=models.BooleanField(default=True)
    created_at=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username}-{self.product.name}-₹{self.target_price}"
