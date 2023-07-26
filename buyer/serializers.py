from rest_framework import serializers
from .models import Buyer
#from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'is_active', 'is_buyer', 'first_name', 'last_name', 'username', 'email', 'created_at', 'last_login','date_joined')
        #fields = '__all__'
        ref_name = 'BuyerUser'
        
        

    # Include the created_at field in the response
    created_at = serializers.DateTimeField(source='date_joined', read_only=True)


class BuyerSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    
    class Meta:
        model = Buyer
        #fields = '__all__'
        fields = ('id','user_type', 'gender', 'phone_number', 'address', 'created_at', 'updated_at', 'user')


class BuyerTokenObtainPairSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(max_length=128, write_only=True)

    def validate(self, attrs):
        data = super().validate(attrs)

        # Authenticate the user
        user = authenticate(
            username=data['username'], 
            password=data['password']
        )

        if user and user.buyer:
            refresh = RefreshToken.for_user(user)

            # Include buyer information in the response
            data['refresh'] = str(refresh)
            data['access'] = str(refresh.access_token)
            data['buyer'] = BuyerSerializer(user.buyer).data  # Serialize buyer information

            # Remove the username and password fields from the response
            data.pop('username', None)
            data.pop('password', None)
            return data

        raise serializers.ValidationError("Invalid credentials")


class BuyerForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

class BuyerResetPasswordSerializer(serializers.Serializer):
    password = serializers.CharField()
    confirm_password = serializers.CharField()