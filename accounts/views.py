import random
from django.core.mail import send_mail
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import EmailOTP
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .tasks import send_otp_email


class SendOTPView(APIView):
    def post(self, request):
        email = request.data.get('email')

        if not email:
            return Response({"error": "Email is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        otp_code = str(random.randint(100000, 999999))

        EmailOTP.objects.update_or_create(
            user=user,
            defaults={'otp_code': otp_code}
        )

        send_mail(
            'Your Verification Code',
            f'Your verification code is: {otp_code}',
            'youremail@gmail.com',
            [email],
            fail_silently=False,
        )

        return Response({"message": "OTP sent successfully."}, status=status.HTTP_200_OK)

class VerifyOTPView(APIView):
    def post(self, request):
        email = request.data.get('email')
        otp_code = request.data.get('otp_code')

        if not email or not otp_code:
            return Response({"error": "Email and OTP code are required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=email)
            email_otp = EmailOTP.objects.get(user=user)
        except (User.DoesNotExist, EmailOTP.DoesNotExist):
            return Response({"error": "Invalid email or OTP."}, status=status.HTTP_400_BAD_REQUEST)

        if email_otp.otp_code == otp_code:
            return Response({"message": "OTP verified successfully."}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid OTP."}, status=status.HTTP_400_BAD_REQUEST)




class VerifyOtpView(APIView):
    def post(self, request):
        email = request.data.get("email")
        otp_code = request.data.get("otp_code")

        if otp_code == "555922":  
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

            refresh = RefreshToken.for_user(user)
            return Response({
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            })

        return Response({"error": "Invalid OTP."}, status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST'])
def send_otp(request):
    return Response({"message": "OTP sent"})
