from django.db import models
from django.conf import settings
from products.models import Product
import uuid

# Create your models here.

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