from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .models import Buyer
from core.models import User
from .serializers import BuyerSerializer, UserSerializer, BuyerTokenObtainPairSerializer, BuyerForgotPasswordSerializer, BuyerResetPasswordSerializer
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
import logging
from rest_framework.exceptions import ValidationError
from django.contrib.auth.hashers import make_password
from django.db import transaction
from django.utils import timezone
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.views import APIView
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.utils.translation import gettext_lazy as _
from django.utils.encoding import force_str
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.urls import reverse
from django.template.loader import render_to_string
from django.core.mail import EmailMessage


# Use the correct name 'buyer_login' to reverse the URL
#url = reverse('buyer_login')


logger = logging.getLogger(__name__)


class BuyerCreateView(generics.CreateAPIView):
    queryset = Buyer.objects.all()
    serializer_class = BuyerSerializer
    authentication_classes = []  # Remove all authentication classes for this view
    permission_classes = [AllowAny]  # Allow anonymous access

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'user': openapi.Schema(type=openapi.TYPE_OBJECT, properties={
                    'first_name': openapi.Schema(type=openapi.TYPE_STRING),
                    'last_name': openapi.Schema(type=openapi.TYPE_STRING),
                    'username': openapi.Schema(type=openapi.TYPE_STRING),
                    'email': openapi.Schema(type=openapi.TYPE_STRING),
                    'password': openapi.Schema(type=openapi.TYPE_STRING),
                    'is_buyer': openapi.Schema(type=openapi.TYPE_BOOLEAN, default=True),
                    # Add other user fields you want to include in the documentation
                }),
                'gender': openapi.Schema(type=openapi.TYPE_STRING),
                'phone_number': openapi.Schema(type=openapi.TYPE_STRING),
                'address': openapi.Schema(type=openapi.TYPE_STRING),
                # Add other buyer fields you want to include in the documentation
            },
            required=['user', 'gender', 'phone_number', 'address'],
        ),
    )
    def post(self, request, format=None):
        serializer = BuyerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response_data = {
                "buyer": serializer.data,
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # def post(self, request, *args, **kwargs):
    #     try:
    #         serializer = self.get_serializer(data=request.data)
    #         serializer.is_valid(raise_exception=True)

    #         # Encrypt the password before saving the User
    #         user_data = serializer.validated_data['user']
    #         user_data['password'] = make_password(user_data['password'])

    #         # Save the User and Buyer objects in a transaction
    #         with transaction.atomic():
    #             user = User.objects.create(**user_data)
    #             buyer_data = serializer.validated_data
    #             buyer_data.pop('user')  # Remove the nested user data
    #             buyer_data['user'] = user
    #             buyer = Buyer.objects.create(**buyer_data)

    #         response_data = {
    #             #"user": serializer.data['user'],
    #             "buyer": serializer.data,
    #         }

    #         return Response(response_data, status=status.HTTP_201_CREATED)
    #     except ValidationError as ve:
    #         errors = ve.detail
    #         return Response({"errors": errors}, status=status.HTTP_400_BAD_REQUEST)
    #     except Exception as e:
    #         return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class BuyerUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Buyer.objects.all()
    serializer_class = BuyerSerializer

    def retrieve(self, request, *args, **kwargs):
        buyer_instance = self.get_object()
        user_instance = buyer_instance.user

        buyer_serializer = self.get_serializer(buyer_instance)
        user_serializer = UserSerializer(user_instance)

        response_data = {
            "buyer": buyer_serializer.data,
            #"user": user_serializer.data,
        }

        return Response(response_data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary="update buyer record"
    )
    def update(self, request, *args, **kwargs):
        buyer_instance = self.get_object()
        user_instance = buyer_instance.user

        user_serializer = UserSerializer(user_instance, data=request.data, partial=True)
        user_serializer.is_valid(raise_exception=True)  # Raise an exception for invalid data
        user_serializer.save()

        buyer_serializer = self.get_serializer(buyer_instance, data=request.data, partial=True)
        buyer_serializer.is_valid(raise_exception=True)  # Raise an exception for invalid data
        buyer_serializer.save()

        response_data = {
            "buyer": buyer_serializer.data,
            #"user": user_serializer.data,
        }

        return Response(response_data, status=status.HTTP_200_OK)


class BuyerTokenObtainPairView(TokenObtainPairView):
    serializer_class = BuyerTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            buyer_data = response.data.get('user')
            if buyer_data:
                # Add any additional data you want to include in the response
                response.data['buyer_id'] = buyer_data.get('id')
                response.data['buyer_username'] = buyer_data.get('user').get('username')
        return response


class BuyerForgotPasswordView(APIView):
    authentication_classes = []  # Remove all authentication classes for this view
    permission_classes = [AllowAny]  # Allow anonymous access
    
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING),
                'email': openapi.Schema(type=openapi.TYPE_STRING),
            },
            required=['username', 'email'],
        ),
    )
    def post(self, request, *args, **kwargs):
        serializer = BuyerForgotPasswordSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return Response({'error': _('User with this email does not exist.')}, status=status.HTTP_400_BAD_REQUEST)

            # Generate the reset password token
            token_generator = default_token_generator
            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            token = token_generator.make_token(user)

            # Prepare the reset password link
            reset_password_url = self._get_reset_password_url(request, uidb64, token)

            # Render the email template
            context = {
                'user': user,
                'reset_password_url': reset_password_url,
            }
            email_message = render_to_string('reset_password_email.html', context)

            # Send the email
            mail_subject = 'Password Reset Request'
            email = EmailMessage(mail_subject, email_message, 'no-reply@example.com', [email])
            email.content_subtype = "html"
            email.send()

            return Response({'success': _('Reset password email has been sent.')}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def _get_reset_password_url(self, request, uidb64, token):
        return request.build_absolute_uri(reverse('buyer_reset_password', args=[uidb64, token]))
    
class BuyerResetPasswordView(APIView):
    authentication_classes = []  # Remove all authentication classes for this view
    permission_classes = [AllowAny]  # Allow anonymous access
    
    def post(self, request, uidb64, token, *args, **kwargs):
        serializer = BuyerResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            try:
                uid = force_str(urlsafe_base64_decode(uidb64))
                user = User.objects.get(pk=uid)
            except (TypeError, ValueError, OverflowError, User.DoesNotExist):
                return Response({'error': _('Invalid reset password link.')}, status=status.HTTP_400_BAD_REQUEST)

            token_generator = default_token_generator
            if not token_generator.check_token(user, token):
                return Response({'error': _('Invalid reset password link.')}, status=status.HTTP_400_BAD_REQUEST)

            password = serializer.validated_data['password']
            user.set_password(password)
            user.save()

            return Response({'success': _('Password has been reset successfully.')}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BuyerListView(generics.ListAPIView):
    queryset = Buyer.objects.all()
    serializer_class = BuyerSerializer