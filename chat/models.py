from django.db import models
from core.models import User
from store.models import Product


class Chat(models.Model):
    buyer = models.ForeignKey(User, related_name='buyer_chats', on_delete=models.CASCADE)
    vendor = models.ForeignKey(User, related_name='vendor_chats', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Chat between {self.buyer.username} and {self.vendor.username}"


class Message(models.Model):
    chat = models.ForeignKey(Chat, related_name='messages', on_delete=models.CASCADE)
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    text = models.TextField()
    product = models.ForeignKey(Product, related_name='chat_messages', null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.sender.username} in Chat({self.chat.id})"