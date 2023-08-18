from django.contrib import admin
from django.utils import timezone
from .models import Product, Category, OrderItem, Order, Checkout, Company

# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    #fields = ['name', 'category', 'price', 'desc', 'photo', 'status']
    list_display = ['user', 'name', 'category', 'price', 'created_on', 'status']
    list_filter = ['name', 'price', 'created_on']
    search_fields = ['name']

    """
    def save_model(self, request, obj, form, change):
        obj.user = request.user
        if not obj.id:
            obj.created_on = timezone.now()
        obj.updated_on = timezone.now()
        super(ProductAdmin, self).save_model(request, obj, form, change)
    """
    
@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'ordered', 'quantity']
    list_filter = ['user', 'ordered']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'start_date', 'ordered_date', 'ordered']
    list_filter = ['user', 'start_date', 'ordered_date', 'ordered']
    search_fields = ['user']


@admin.register(Checkout)
class CheckoutAdmin(admin.ModelAdmin):
    list_display = ['user', 'order', 'country', 'zip', 'street_address', 'apartment_address']
    list_filter = ['zip', 'country']


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ['user', 'name']
    search_fields = ['user', 'name']