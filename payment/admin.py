from django.contrib import admin
from .models import Payment

# Register your models here.


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['order', 'email', 'amount', 'created_on', 'paystack_ref', 'paid']
    list_filter = ['amount', 'created_on', 'paid']
    
