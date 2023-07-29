from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Chat, Message
from .serializers import ChatSerializer, MessageSerializer
from rest_framework import status
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from store.models import Product
from store.serializers import ProductSerializer




class SendMessageView(APIView):
    @swagger_auto_schema(
        request_body=MessageSerializer,
        responses={
            200: MessageSerializer(),
            400: "Bad Request: Chat not found.",
        },
        operation_summary="Send a message in a chat",
        operation_description="This API endpoint allows authenticated users to send a message in an existing chat.",
    )
    def post(self, request):
        user = request.user
        message_text = request.data.get('message')
        chat_id = request.data.get('chat_id')
        product_id = request.data.get('product_id')

        try:
            chat = Chat.objects.get(id=chat_id)
        except Chat.DoesNotExist:
            return Response({'error': 'Chat not found.'}, status=400)

        product = None
        if product_id:
            try:
                product = Product.objects.get(id=product_id)
            except Product.DoesNotExist:
                pass

        message = Message.objects.create(chat=chat, sender=user, text=message_text, product=product)
        serializer = MessageSerializer(message)

        return Response(serializer.data)


class ReceiveMessageView(APIView):
    @swagger_auto_schema(
        responses={
            200: MessageSerializer(many=True),
            403: "Forbidden: You are not authorized to view these messages.",
        },
        operation_summary="Retrieve chat messages for the authenticated user",
        operation_description="This API endpoint allows authenticated users to retrieve their chat messages. It returns all messages associated with chats where the user is either the buyer or the vendor.",
    )
    def get(self, request):
        # Check authentication is implemented for buyers and vendors
        user = request.user

        # Retrieve all chats where the authenticated user is either the buyer or the vendor
        chats = Chat.objects.filter(buyer=user) | Chat.objects.filter(vendor=user)

        # Retrieve all messages associated with the retrieved chats
        messages = Message.objects.filter(chat__in=chats).order_by('created_at')

        if not messages.exists():
            return Response({'message': 'No chat messages found for the user.'}, status=200)

        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)


class SingleMessageView(APIView):
    @swagger_auto_schema(
        responses={
            200: MessageSerializer(),
            403: "Forbidden: You are not authorized to view this message.",
            404: "Not Found: Message not found.",
        },
        operation_summary="Retrieve a single message by its ID",
        operation_description="This API endpoint allows authenticated users to retrieve a single message by providing its unique ID. The user must be the sender or receiver of the message to access it.",
    )
    def get(self, request, message_id):
        # Assuming authentication is implemented for buyers and vendors
        user = request.user

        try:
            message = Message.objects.get(id=message_id)
        except Message.DoesNotExist:
            return Response({'message': 'Message not found.'}, status=status.HTTP_404_NOT_FOUND)

        # Check if the authenticated user is the sender or receiver of the message
        if user == message.sender or user in [message.chat.buyer, message.chat.vendor]:
            serializer = MessageSerializer(message)
            return Response(serializer.data)
        else:
            return Response({'message': 'You are not authorized to view this message.'}, status=status.HTTP_403_FORBIDDEN)