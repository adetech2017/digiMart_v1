from django.db import models
from vendor.models import Vendor
from buyer.models import Buyer




class Product(models.Model):
    vendor = models.ForeignKey(Vendor, related_name='products', on_delete=models.CASCADE)
    product_name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=0)
    stock = models.PositiveIntegerField()
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    product_image = models.ImageField(upload_to='product_images/')
    location = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product_name


class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product_images/', blank=True, null=True)

    def __str__(self):
        return f"Image for {self.product.product_name}"


class Order(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )

    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    tax = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_method = models.CharField(max_length=200, null=True, blank=True)
    shipping_price = models.DecimalField(max_digits=9, decimal_places=2, null=True, blank=True)
    is_paid = models.BooleanField(default=True)
    delivered_at = models.DateTimeField(auto_now_add=False, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order #{self.id} - Buyer: {self.buyer}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='order_items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    bargain_price = models.DecimalField(
        max_digits=9, decimal_places=2, null=True, blank=True, default=0.00)
    vourcher_code = models.CharField(max_length=254, null=True, blank=True)

    def __str__(self):
        return f"{self.product.product_name} - {self.quantity}"

class ShippingInformation(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    shipping_address = models.CharField(max_length=200)
    shipping_city = models.CharField(max_length=100)
    shipping_zip_code = models.CharField(max_length=10)
    country = models.CharField(max_length=100)

    def __str__(self):
        return f"Shipping Information for Order #{self.order.id}"
    

class BargainPrice(models.Model):
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    price = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    bargain_price = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    discount = models.DecimalField(
        max_digits=9, decimal_places=2, null=True, blank=True)
    discounted_price = models.DecimalField(
        max_digits=9, decimal_places=2, null=True, blank=True)
    vourcher_code = models.CharField(max_length=10, unique=True)
    isRedeemed = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.buyer} - {self.vendor} - {self.product} - {self.vourcher_code}"