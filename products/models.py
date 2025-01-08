from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
import uuid

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    current_price = models.DecimalField(max_digits=10, decimal_places=2)
    lowest_price= models.DecimalField(default=0, max_digits=10, decimal_places=2)
    highest_price= models.DecimalField(default=0, max_digits=10, decimal_places=2)
    product_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    url = models.URLField()
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.name)
    
    def get_absolute_url(self):
        return f"/products/{self.product_id}/"
    
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
class WatchList(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name=models.CharField(max_length=255,blank= True)
    watchlist_id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    
    def save(self,*args,**kwargs):
        if not self.name:
            self.name=f"{self.user.username}'s watchlist"
        super().save(*args,**kwargs)

    def __str__(self):
        return f"{self.user.username}'s Watchlist"

class WatchListItem(models.Model):
    watchlist=models.ForeignKey(WatchList, on_delete=models.CASCADE, related_name='items')
    product=models.ForeignKey(Product, on_delete=models.CASCADE)
    class Meta:
        unique_together=('watchlist','product')

    def __str__(self):
        return f"{self.watchlist.user.username}- {self.product.name}"

# End-of-file (EOF)