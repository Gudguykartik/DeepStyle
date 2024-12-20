from django.db import models

# Create your models here.

class CartItem(models.Model):
    product_name = models.CharField(max_length=255)
    size = models.CharField(max_length=2)  # S, M, L, XL
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    image_url = models.URLField(max_length=500)
    product_id = models.IntegerField()  # To reference the fashion dataset
    
    def get_total(self):
        return self.price * self.quantity
