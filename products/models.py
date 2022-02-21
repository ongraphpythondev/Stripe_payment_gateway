from django.db import models
from django.utils import timezone

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.IntegerField(default=0)

    def __str__(self) -> str: 
        return self.name

class Order(models.Model):
    product = models.ForeignKey(Product , on_delete=models.CASCADE)
    ordered_at = models.DateTimeField(default= timezone.now)

    def __str__(self):
        return str(self.product)
