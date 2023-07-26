from django.contrib import admin
from store.models import Product, Order, OrderItem, ShippingInformation
from vendor.models import Vendor
from buyer.models import Buyer
from .models import User

# Register your models here.


admin.site.register(Product)
admin.site.register(Vendor)
admin.site.register(User)
admin.site.register(Buyer)
admin.site.register(ShippingInformation)