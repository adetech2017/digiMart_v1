from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Vendor
from .serializers import VendorSerializer, UserSerializer, VendorTokenObtainPairSerializer, VendorForgotPasswordSerializer, VendorResetPasswordSerializer
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
import logging
from rest_framework.exceptions import ValidationError
from django.contrib.auth.hashers import make_password
from django.db import transaction
from core.models import User
from rest_framework_simplejwt.views import TokenObtainPairView
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.utils.translation import gettext_lazy as _
from django.utils.encoding import force_str
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.urls import reverse
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from rest_framework.views import APIView




class VendorCreateView(generics.CreateAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
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
                    'is_vendor': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                    # Add other user fields you want to include in the documentation
                }),
                'digi_number': openapi.Schema(type=openapi.TYPE_STRING),
                'phone_number': openapi.Schema(type=openapi.TYPE_STRING),
                'company_name': openapi.Schema(type=openapi.TYPE_STRING),
                # Add other vendor fields you want to include in the documentation
            },
            required=['user', 'gender', 'phone_number', 'address'],
        ),
    )
    def post(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            # Encrypt the password before saving the User
            user_data = serializer.validated_data['user']
            user_data['password'] = make_password(user_data['password'])

            # Save the User and Vendor objects in a transaction
            with transaction.atomic():
                user = User.objects.create(**user_data)
                vendor_data = serializer.validated_data
                vendor_data.pop('user')  # Remove the nested user data
                vendor_data['user'] = user
                vendor = Vendor.objects.create(**vendor_data)

            response_data = {
                #"user": serializer.data['user'],
                "vendor": serializer.data,
            }

            return Response(response_data, status=status.HTTP_201_CREATED)
        except ValidationError as ve:
            errors = ve.detail
            return Response({"errors": errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class VendorDetailView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    
    def retrieve(self, request, *args, **kwargs):
        vendor_instance = self.get_object()
        user_instance = vendor_instance.user

        vendor_serializer = self.get_serializer(vendor_instance)
        user_serializer = UserSerializer(user_instance)

        response_data = {
            "vendor": vendor_serializer.data,
            #"user": user_serializer.data,
        }

        return Response(response_data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary="update vendor record"
    )
    def update(self, request, *args, **kwargs):
        vendor_instance = self.get_object()
        user_instance = vendor_instance.user

        user_serializer = UserSerializer(user_instance, data=request.data, partial=True)
        user_serializer.is_valid(raise_exception=True)  # Raise an exception for invalid data
        user_serializer.save()

        vendor_serializer = self.get_serializer(vendor_instance, data=request.data, partial=True)
        vendor_serializer.is_valid(raise_exception=True)  # Raise an exception for invalid data
        vendor_serializer.save()

        response_data = {
            "vendor": vendor_serializer.data,
            #"user": user_serializer.data,
        }

        return Response(response_data, status=status.HTTP_200_OK)

class VendorTokenObtainPairView(TokenObtainPairView):
    serializer_class = VendorTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            vendor_data = response.data.get('user')
            if vendor_data:
                # Add any additional data you want to include in the response
                response.data['vendor_id'] = vendor_data.get('id')
                response.data['vendor_username'] = vendor_data.get('user').get('username')
        return response
    
class VendorForgotPasswordView(APIView):
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
        serializer = VendorForgotPasswordSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return Response({'error': _('Vendor with this email does not exist.')}, status=status.HTTP_400_BAD_REQUEST)

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
        return request.build_absolute_uri(reverse('vendor_reset_password', args=[uidb64, token]))
    
class VendorResetPasswordView(APIView):
    authentication_classes = []  # Remove all authentication classes for this view
    permission_classes = [AllowAny]  # Allow anonymous access
    
    def post(self, request, uidb64, token, *args, **kwargs):
        serializer = VendorResetPasswordSerializer(data=request.data)
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


class VendorListView(generics.ListAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer