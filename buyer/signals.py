# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from django.contrib.auth.signals import user_logged_in
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from django.utils import timezone





# @receiver(user_logged_in)
# def update_last_login(sender, request, user, **kwargs):
#     if user.buyer:
#         user.buyer.last_login = user.last_login
#         user.buyer.save()
@receiver(user_logged_in)
def update_last_login(sender, request, user, **kwargs):
    if user.buyer:
        buyer = user.buyer
        buyer.last_login = timezone.now()
        buyer.save()