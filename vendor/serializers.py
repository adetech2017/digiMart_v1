from rest_framework import serializers
from .models import Vendor
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from core.authentication_backends import EmailBackend




User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        #fields = '__all__'
        fields = ('id', 'is_active', 'is_vendor', 'first_name', 'last_name','username', 'email', 'created_at', 'last_login','date_joined')

        ref_name = 'VendorUserSerializer'
    # Include the created_at field in the response
    created_at = serializers.DateTimeField(source='date_joined', read_only=True)


class VendorSerializer(serializers.ModelSerializer):
    tokens = serializers.SerializerMethodField()
    user = UserSerializer()
    
    class Meta:
        model = Vendor
        #fields = '__all__'
        fields = ('user', 'user_type', 'phone_number', 'digi_number', 'vendor_type', 'company_name', 'website', 'created_at', 'updated_at', 'tokens')
        # You can include other fields as needed

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create_user(**user_data)
        vendor = Vendor.objects.create(user=user, **validated_data)
        return vendor

    # def get_tokens(self, obj):
    #     refresh = RefreshToken.for_user(obj.user)
    #     return {
    #         'refresh': str(refresh),
    #         'access': str(refresh.access_token),
    #     }
    
class VendorTokenObtainPairSerializer(TokenObtainPairSerializer):
    class Meta:
        model = Vendor

# class VendorTokenObtainPairSerializer(serializers.Serializer):
#     email = serializers.EmailField()
#     password = serializers.CharField()


#     def validate(self, attrs):
#         email = attrs.get('email')
#         password = attrs.get('password')
#         user = EmailBackend().authenticate(self.context['request'], email=email, password=password)
#         #print(user)
#         if user:
#             refresh = RefreshToken.for_user(user)
#             return {
#                 'refresh': str(refresh),
#                 'access': str(refresh.access_token),
#                 'user_id': user.id,
#             }
#         raise serializers.ValidationError("Invalid credentials")
    # email = serializers.EmailField()
    # password = serializers.CharField()

    # def validate(self, attrs):
    #     data = super().validate(attrs)

    #     # Authenticate the user
    #     user = authenticate(
    #         email=data['email'], 
    #         password=data['password']
    #     )

    #     if user and user.vendor:
    #         refresh = RefreshToken.for_user(user)

    #         # Include vendor information in the response
    #         data['refresh'] = str(refresh)
    #         data['access'] = str(refresh.access_token)
    #         data['vendor'] = VendorSerializer(user.vendor).data  # Serialize vendor information

    #         # Remove the username and password fields from the response
    #         data.pop('email', None)
    #         data.pop('password', None)
    #         return data

    #     raise serializers.ValidationError("Invalid credentials")


class VendorForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()


class VendorResetPasswordSerializer(serializers.Serializer):
    password = serializers.CharField()
    confirm_password = serializers.CharField()