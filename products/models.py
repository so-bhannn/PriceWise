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

# End-of-file (EOF)