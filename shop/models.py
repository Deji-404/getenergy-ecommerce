from django.db import models
from django.conf import settings
from django.urls import reverse
from django_countries.fields import CountryField

# Create your models here.

STATUS = (
    (0, "Draft"),
    (1, "Publish")
)

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Company(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='company')
    name = models.CharField(max_length=200)
    cover_photo = models.ImageField(upload_to='company_cover')
    about = models.TextField()

    def __str__(self):
        return self.name

class Product(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='products', null=True, blank=True)
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    price = models.DecimalField(decimal_places=2, max_digits=20)
    desc = models.TextField()
    photo = models.ImageField(upload_to='products')
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    status = models.IntegerField(default=1, choices=STATUS)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created_on']

    def get_absolute_url(self):
        return reverse("shop:product", kwargs={"id": self.id})
    
    def get_add_to_cart_url(self):
        return reverse("shop:add-to-cart", kwargs={"id": self.id})
    
    def get_remove_from_cart_url(self):
        return reverse("shop:remove-from-cart", kwargs={"id": self.id})
    
    def get_reduce_order_quantity_url(self):
        return reverse("shop:reduce-order-quantity", kwargs={"id": self.id})

class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.product.name}"
    
    def get_total_price(self):
        return self.quantity * self.product.price
    
class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    products = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)

    class Meta:
        ordering = ['-start_date']

    def __str__(self):
        return f"{self.user.username}"
    
    def get_total_price(self):
        total = 0
        for product in self.products.all():
            total += product.get_total_price()
        return total
    
class Checkout(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='checkout')
    street_address = models.CharField(max_length=100)
    apartment_address = models.CharField(blank=True, max_length=100)
    country = CountryField(multiple=False)
    zip = models.CharField(max_length=100)
    city = models.CharField(max_length=50)

    def __str__(self):
        return self.user.username
    
class ProductReview(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='product_reviews')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_reviews')
    comment = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} comment on {self.product}"
    
    class Meta:
        ordering = ['-created_on']

    
