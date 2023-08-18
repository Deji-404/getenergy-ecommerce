from django.db import models
from shop.models import Order

# Create your models here.

class Payment(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='payment')
    email = models.EmailField()
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    paystack_ref = models.CharField(max_length=100, blank=True, null=True)
    paid = models.BooleanField(default=False)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return f"Payment {self.id}"
    
    def get_amount(self):
        return self.amount
        
