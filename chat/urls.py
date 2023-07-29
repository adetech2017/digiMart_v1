from django.urls import path
from .views import SendMessageView, ReceiveMessageView, SingleMessageView




urlpatterns = [
    path('chat/send_message/', SendMessageView.as_view(), name='send-message'),
    path('chat/receive_message/', ReceiveMessageView.as_view(), name='receive-message'),
    path('chat/messages/<int:message_id>/', SingleMessageView.as_view(), name='single-message'),
]

