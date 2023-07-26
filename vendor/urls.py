from django.urls import path
from .views import VendorCreateView, VendorDetailView, VendorTokenObtainPairView, VendorForgotPasswordView, VendorResetPasswordView, VendorListView



urlpatterns = [
    path('vendor/', VendorCreateView.as_view(), name='vendor-create'),
    path('vendor/<int:pk>/', VendorDetailView.as_view(), name='vendor-detail'),
    path('vendor/auth', VendorTokenObtainPairView.as_view(), name='vendor_token_obtain_pair'),
    path('vendor/forgot-password/', VendorForgotPasswordView.as_view(), name='buyer_forgot_password'),
    path('vendor/reset-password/<uidb64>/<token>/', VendorResetPasswordView.as_view(), name='buyer_reset_password'),
    path('vendors/', VendorListView.as_view(), name='vendor-list'),
]
