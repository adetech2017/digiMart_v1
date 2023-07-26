from django.db import models
from django.contrib.auth.models import AbstractUser, Group
from django.conf import settings
from core.models import User





class Vendor(models.Model):
    USER_TYPE_CHOICES = (
        ('vendor', 'Vendor'),
    )
    
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='vendor')
    digi_number = models.CharField(max_length=100, null=True, blank=True)
    company_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    alt_phone = models.CharField(max_length=20, null=True, blank=True)
    bank_name = models.CharField(max_length=100, null=True, blank=True)
    account_name = models.CharField(max_length=100, null=True, blank=True)
    account_number = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=225, null=True, blank=True)
    state = models.CharField(max_length=225, null=True, blank=True)
    city = models.CharField(max_length=225, null=True, blank=True)
    vendor_photo = models.ImageField(null=True, blank=True,
                            default='placeholder.png')
    vend_logo = models.ImageField(null=True, blank=True,
                            default='placeholder.png')
    website = models.URLField(null=True, blank=True)
    last_login = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    groups = models.ManyToManyField(Group, blank=True, related_name='vendor_users')
    
    class Meta:
        permissions = (
            ("create_vendor", "Can create vendor"),
            ("read_vendor", "Can read vendor details"),
            ("update", "Can update vendor details"),
        )

    def __str__(self):
        return self.username


