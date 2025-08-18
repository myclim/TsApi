from django.db import models



class ProductModel(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
