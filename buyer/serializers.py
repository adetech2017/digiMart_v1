from rest_framework import serializers
from .models import Buyer
#from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    #password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        #fields = '__all__'
        fields = ('id', 'is_active', 'is_buyer', 'first_name', 'last_name', 'username', 'email', 'created_at', 'last_login','date_joined')

        ref_name = 'BuyerUserSerializer'
    # Include the created_at field in the response
    created_at = serializers.DateTimeField(source='date_joined', read_only=True)


class BuyerSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Buyer
        fields = ['user', 'user_type', 'gender', 'phone_number', 'last_login', 'address', 'created_at', 'updated_at']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create_user(**user_data)
        buyer = Buyer.objects.create(user=user, **validated_data)
        return buyer



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