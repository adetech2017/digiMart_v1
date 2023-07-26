from django.db import models
# from django.contrib.auth.models import AbstractUser, Group
# from django.conf import settings
from core.models import User


class Buyer(models.Model):
    USER_TYPE_CHOICES = (
        ('buyer', 'Buyer'),
    )
    
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='buyer')
    gender = models.CharField(max_length=10, null=True, blank=True)
    phone_number = models.CharField(max_length=20)
    last_login = models.DateTimeField(null=True, blank=True)
    address = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    #groups = models.ManyToManyField(Group, blank=True, related_name='buyer_users')

    def __str__(self):
        return self.user.username