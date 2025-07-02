# yourapp/urls.py

from django.urls import path
from .views import send_otp

urlpatterns = [
    path('send-otp/', send_otp, name='send_otp'),
]
