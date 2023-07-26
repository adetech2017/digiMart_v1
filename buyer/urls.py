from django.urls import path
from .views import BuyerCreateView, BuyerUpdateView,BuyerTokenObtainPairView, BuyerForgotPasswordView, BuyerResetPasswordView, BuyerListView
from rest_framework_simplejwt.views import TokenObtainPairView
#from .views import CustomTokenRefreshView


urlpatterns = [
    path('buyer/create-account', BuyerCreateView.as_view(), name='buyer-create'),
    path('buyer/<int:pk>/', BuyerUpdateView.as_view(), name='buyer-detail'),
    path('buyer/auth', BuyerTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('buyer/forgot-password/', BuyerForgotPasswordView.as_view(), name='buyer_forgot_password'),
    path('buyer/reset-password/<uidb64>/<token>/', BuyerResetPasswordView.as_view(), name='buyer_reset_password'),
    path('buyers/', BuyerListView.as_view(), name='buyer-list'),
]