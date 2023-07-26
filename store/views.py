from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Product, ProductImage, Order, OrderItem, ShippingInformation, BargainPrice
from .serializers import (
    ProductSerializer, ProductImageSerializer,
    OrderSerializer, OrderItemSerializer, ShippingInformationSerializer, BargainPriceSerializer
)
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, permissions
from django.db.models import Q
from django.utils.crypto import get_random_string
import string


################ create/view product endpoint ####################
class ProductCreateView(generics.CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

################ edit/update product detail ####################
class ProductRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

################ create/view order endpoint ####################
# Order Views
class OrderListView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(buyer=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = OrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order = serializer.save(buyer=request.user)

        # Create order items and update product stock
        items = request.data.get('order_items', [])
        for item_data in items:
            product = Product.objects.get(pk=item_data['product'])
            quantity = item_data['quantity']
            bargain_price = item_data['bargain_price']
            vourcher_code = item_data['vourcher_code']

            # Calculate the price after applying the discount
            discounted_price = product.price * (1 - product.discount / 100)

            # Check if the product has enough stock to fulfill the order
            if product.stock >= quantity:
                # Create order item with the discounted price
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=quantity,
                    price=discounted_price,
                    bargain_price=bargain_price,
                    vourcher_code = vourcher_code
                )

                # Update the product's stock
                product.stock -= quantity
                product.save()
                
                bargain_price = BargainPrice.objects.get(vourcher_code=vourcher_code)

                # Update isRedeemed to True
                bargain_price.isRedeemed = True
                bargain_price.save()
            else:
                return Response({"error": f"Insufficient stock for product {product.name}"}, status=status.HTTP_400_BAD_REQUEST)

        # Create shipping information
        shipping_data = request.data.get('shipping_info', {})
        shipping_data['order'] = order.id
        shipping_serializer = ShippingInformationSerializer(data=shipping_data)
        shipping_serializer.is_valid(raise_exception=True)
        shipping_serializer.save()

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    serializer_class = OrderSerializer

################ edit/update order detail ####################
class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(buyer=self.request.user)

    serializer_class = OrderSerializer

################ create/view order item ####################
# OrderItem Views
class OrderItemListView(generics.ListCreateAPIView):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer

################ edit/update order item ####################
class OrderItemDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer

################ create/view product images endpoint ####################
# ProductImage Views
class ProductImageListView(generics.ListCreateAPIView):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer

################ edit/updaate product images ####################
class ProductImageDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer

################ create/view shipping endpoint ####################
# ShippingInformation Views
class ShippingInformationListView(generics.ListCreateAPIView):
    queryset = ShippingInformation.objects.all()
    serializer_class = ShippingInformationSerializer

################ edit/update shipping Endpoint ####################
class ShippingInformationDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ShippingInformation.objects.all()
    serializer_class = ShippingInformationSerializer

################ Auth Vendor Products Lists Endpoint ####################
class VendorProductListView(generics.ListAPIView):
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        vendor = self.request.user  # Assuming the vendor is the authenticated user
        return Product.objects.filter(vendor=vendor)

################ Auth Vendor Order Lists Endpoint ####################
class VendorOrderListView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        vendor = self.request.user  # Assuming the vendor is the authenticated user
        return Order.objects.filter(vendor=vendor)

################ Auth Buyer Order Lists Endpoint ####################
class BuyerOrderListView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        buyer = self.request.user  # Assuming the buyer is the authenticated user
        return Order.objects.filter(buyer=buyer)

################ Product search Endpoint ####################
class ProductSearchView(generics.ListAPIView):
    serializer_class = ProductSerializer
    #products/search/?product_name=shoes
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                name='product_name',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                description='Search products by name (case-insensitive)',
            ),
        ],
        responses={200: ProductSerializer(many=True)},
    )
    def get_queryset(self):
        search_query = self.request.query_params.get('product_name', '')
        return Product.objects.filter(product_name__icontains=search_query)

################ Vendor product search Endpoint ####################
#/api/products/search/?company_name=search_query
class VendorSearchView(generics.ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        search_query = self.request.query_params.get('company_name', '')
        return Product.objects.filter(vendor__name__icontains=search_query)
    

class AllProductListView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class AllOrderListView(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    

class BargainPriceListCreateView(generics.ListCreateAPIView):
    queryset = BargainPrice.objects.all()
    serializer_class = BargainPriceSerializer
    
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'buyer': openapi.Schema(type=openapi.TYPE_INTEGER),
                'vendor': openapi.Schema(type=openapi.TYPE_INTEGER),
                'product': openapi.Schema(type=openapi.TYPE_INTEGER),
                'price': openapi.Schema(type=openapi.TYPE_NUMBER, format=openapi.FORMAT_DECIMAL),
                'bargain_price': openapi.Schema(type=openapi.TYPE_NUMBER, format=openapi.FORMAT_DECIMAL),
                'discount': openapi.Schema(type=openapi.TYPE_NUMBER, format=openapi.FORMAT_DECIMAL),
                'discounted_price': openapi.Schema(type=openapi.TYPE_NUMBER, format=openapi.FORMAT_DECIMAL),
                'vourcher_code': openapi.Schema(type=openapi.TYPE_STRING),
                'isRedeemed': openapi.Schema(type=openapi.TYPE_BOOLEAN, default=False),
            },
            required=['buyer', 'vendor', 'product', 'vourcher_code'],
        ),
        responses={
            status.HTTP_201_CREATED: BargainPriceSerializer(),
            status.HTTP_400_BAD_REQUEST: "Invalid data provided.",
        },
    )
    def post(self, request, *args, **kwargs):
        # Generate random vourcher_code
        vourcher_code_length = 10
        vourcher_code = get_random_string(length=vourcher_code_length, allowed_chars=string.ascii_uppercase + string.digits)

        # Set the generated vourcher_code in the request data
        
        request.data['vourcher_code'] = vourcher_code

        return super().post(request, *args, **kwargs)
    
    def perform_create(self, serializer):
        # Calculate discounted_price and discount percentage
        price = serializer.validated_data['price']
        bargain_price = serializer.validated_data['bargain_price']

        # Calculate the discount percentage
        if price > 0:
            discount_percent = ((price - bargain_price) / price) * 100
        else:
            discount_percent = 0

        # Calculate the discounted_price
        discounted_price = bargain_price - price

        # Set discounted_price and discount percentage in the serializer's data before saving
        serializer.validated_data['discounted_price'] = discounted_price
        serializer.validated_data['discount'] = discount_percent

        # Call the default perform_create to save the BargainPrice object
        super().perform_create(serializer)


class BargainPriceDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = BargainPrice.objects.all()
    serializer_class = BargainPriceSerializer


class BargainPriceValidateView(generics.RetrieveAPIView):
    queryset = BargainPrice.objects.all()
    serializer_class = BargainPriceSerializer
    lookup_field = 'vourcher_code'

    def retrieve(self, request, *args, **kwargs):
        voucher_code = kwargs.get('vourcher_code')
        try:
            bargain_price = BargainPrice.objects.get(vourcher_code=voucher_code)
        except BargainPrice.DoesNotExist:
            return Response({'message': 'Invalid voucher code'}, status=status.HTTP_404_NOT_FOUND)

        if bargain_price.isRedeemed:
            return Response({'message': 'Voucher code already redeemed'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(bargain_price)
        return Response(serializer.data, status=status.HTTP_200_OK)