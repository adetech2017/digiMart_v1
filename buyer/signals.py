from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in
from django.utils import timezone
from .models import Buyer


@receiver(user_logged_in)
def update_last_login(sender, request, user, **kwargs):
    try:
        buyer = user.buyer
        buyer.last_login = timezone.now()
        buyer.save()
    except Buyer.DoesNotExist:
        pass