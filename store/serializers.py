from rest_framework import serializers
from .models import Product, ProductImage, Order, OrderItem, ShippingInformation, BargainPrice, ProductReview
from rest_framework import generics, permissions
from buyer.serializers import BuyerSerializer



class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ('image',)


class ProductReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductReview
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, required=False)
    reviews = ProductReviewSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ('id', 'vendor', 'product_name', 'description', 'price', 'quantity', 'stock', 'discount', 'product_image', 'location', 'created_at', 'updated_at', 'images', 'reviews')
        extra_kwargs = {
            'product_image': {'required': True}  # Set product_image as required
        }


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'quantity', 'price', 'bargain_price']


class ShippingInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingInformation
        fields = ['id', 'shipping_address', 'shipping_city', 'shipping_zip_code']


class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True)  # Nested serializer for OrderItem
    shipping_info = ShippingInformationSerializer()  # Nested serializer for ShippingInformation

    class Meta:
        model = Order
        fields = ['id', 'buyer', 'order_items', 'shipping_info', 'total_amount', 'created_at', 'updated_at']
        # Add any other fields as needed


class BargainPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = BargainPrice
        fields = '__all__'


class BargainPriceSerializer(serializers.ModelSerializer):
    #buyer = BuyerSerializer()
    #vendor = ProductSerializer()
    product = ProductSerializer()
    class Meta:
        model = BargainPrice
        fields = '__all__'