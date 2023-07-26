from rest_framework import serializers
from .models import Vendor
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken



User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'is_active', 'is_vendor', 'first_name', 'last_name', 'username', 'email', 'created_at', 'last_login','date_joined')
        ref_name = 'VendorUser'
        

    # Include the created_at field in the response
    created_at = serializers.DateTimeField(source='date_joined', read_only=True)


class VendorSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    
    class Meta:
        model = Vendor
        fields = '__all__'
        # You can include other fields as needed


class VendorTokenObtainPairSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(max_length=128, write_only=True)

    def validate(self, attrs):
        data = super().validate(attrs)

        # Authenticate the user
        user = authenticate(
            username=data['username'], 
            password=data['password']
        )

        if user and user.vendor:
            refresh = RefreshToken.for_user(user)

            # Include vendor information in the response
            data['refresh'] = str(refresh)
            data['access'] = str(refresh.access_token)
            data['vendor'] = VendorSerializer(user.vendor).data  # Serialize vendor information

            # Remove the username and password fields from the response
            data.pop('username', None)
            data.pop('password', None)
            return data

        raise serializers.ValidationError("Invalid credentials")


class VendorForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()


class VendorResetPasswordSerializer(serializers.Serializer):
    password = serializers.CharField()
    confirm_password = serializers.CharField()