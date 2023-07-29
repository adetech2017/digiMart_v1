import os
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
import chat.routing  # Replace 'your_app_name' with the name of your Django app



os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'digiMart_v1.settings')  # Replace 'your_project_name' with the actual name of your Django project

application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': URLRouter(
        chat.routing.websocket_urlpatterns  # Replace 'your_app_name' with the name of your Django app
    ),
})
