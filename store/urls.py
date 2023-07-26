from django.urls import path
from .views import (
    ProductCreateView, ProductRetrieveUpdateDestroyView,
    OrderListView, OrderDetailView,
    OrderItemListView, OrderItemDetailView,
    ShippingInformationListView, ShippingInformationDetailView, VendorProductListView,
    VendorOrderListView, BuyerOrderListView, ProductSearchView, VendorSearchView, AllProductListView,
    AllOrderListView, BargainPriceListCreateView, BargainPriceDetailView, BargainPriceValidateView
)


app_name = 'store'

urlpatterns = [
    # Product URLs
    #path('product/', ProductCreateView.as_view(), name='product-list'),
    path('product/create/', ProductCreateView.as_view(), name='product-create'),
    path('product/<int:pk>/', ProductRetrieveUpdateDestroyView.as_view(), name='product-detail'),

    # Order URLs
    path('orders/', OrderListView.as_view(), name='order-list'),
    path('orders/<int:pk>/', OrderDetailView.as_view(), name='order-detail'),

    # OrderItem URLs
    path('order-items/', OrderItemListView.as_view(), name='orderitem-list'),
    path('order-items/<int:pk>/', OrderItemDetailView.as_view(), name='orderitem-detail'),

    # ShippingInformation URLs
    path('shipping-info/', ShippingInformationListView.as_view(), name='shippinginformation-list'),
    path('shipping-info/<int:pk>/', ShippingInformationDetailView.as_view(), name='shippinginformation-detail'),
    
    # current auth vendor products
    path('vendor/products/', VendorProductListView.as_view(), name='vendor-product-list'),
    
    # current auth vendor orders
    path('vendor/orders/', VendorOrderListView.as_view(), name='vendor-order-list'),
    
    # current buyer orders
    path('buyer/orders/', BuyerOrderListView.as_view(), name='buyer-order-list'),
    
    # search for products
    path('product/search/', ProductSearchView.as_view(), name='product-search'),
    
    # search for vendor products
    path('vendors/products/search/<str:company_name>', VendorSearchView.as_view(), name='product-search'),
    
    path('products/', AllProductListView.as_view(), name='product-list'),
    path('orders/', AllOrderListView.as_view(), name='order-list'),
    
    path('bargain-prices/', BargainPriceListCreateView.as_view(), name='bargain-price-list-create'),
    path('bargain-prices/<int:pk>/', BargainPriceDetailView.as_view(), name='bargain-price-detail'),
    path('bargain-prices/validate/<str:vourcher_code>/', BargainPriceValidateView.as_view(), name='bargain-price-validate'),
]

