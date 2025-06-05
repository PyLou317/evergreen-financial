from django.db import models
from django.conf import settings
from category.models import Category

# Create your models here.
class Transaction(models.Model):
    date = models.DateField(null=True, blank=True)
    description = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    notes = models.TextField(max_length=500, null=True, blank=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.date} - {self.description} - {self.category} - ${self.amount} - {self.owner}"