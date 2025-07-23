from django.urls import path
from emailapp.consumers import EmailStatusConsumer

websocket_urlpatterns = [
    path('ws/email/<str:email_id>/', EmailStatusConsumer.as_asgi()),
]
