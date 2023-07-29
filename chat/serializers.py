from rest_framework import serializers
from .models import Chat, Message
from store.serializers import ProductSerializer



class MessageSerializer(serializers.ModelSerializer):
    product = ProductSerializer(required=False)
    
    class Meta:
        model = Message
        fields = '__all__'


class ChatSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Chat
        fields = '__all__'