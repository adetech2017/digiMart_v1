from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model
#from .models import User

User = get_user_model()

class EmailBackend(ModelBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        try:
            user = User.objects.filter(email=email).first()
            print("Attempting authentication for email:", email)
            print("Stored hashed password:", user.password)
            if user.check_password(password):
                print("Authentication successful:", user)
                return user
            else:
                print("Incorrect password")
        except User.DoesNotExist:
            print("User not found")
            return None

        return None



