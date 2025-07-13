import random
from django.core.mail import send_mail
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .elasticsearch_helpers import save_otp_to_elasticsearch
from .models import EmailOTP
from rest_framework import viewsets, permissions
from .models import Post
from .serializers import PostSerializer
from .elasticsearch_helpers import log_post_action

class SendOTPView(APIView):
    def post(self, request):
        email = request.data.get("email")

        if not email:
            return Response({"error": "Email is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        otp_code = str(random.randint(100000, 999999))

        EmailOTP.objects.update_or_create(
            user=user,
            defaults={"otp_code": otp_code}
        )

        send_mail(
            "Your Verification Code",
            f"Your verification code is: {otp_code}",
            "youremail@gmail.com",
            [email],
            fail_silently=False,
        )
        
        save_otp_to_elasticsearch(email, otp_code)

        return Response({"message": "OTP sent successfully."}, status=status.HTTP_200_OK)


class VerifyOTPView(APIView):
 
    def post(self, request):
        email = request.data.get("email")
        otp_code = request.data.get("otp_code")

        if not email or not otp_code:
            return Response({"error": "Email and OTP code are required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=email)
            email_otp = EmailOTP.objects.get(user=user)
        except (User.DoesNotExist, EmailOTP.DoesNotExist):
            return Response({"error": "Invalid email or OTP."}, status=status.HTTP_400_BAD_REQUEST)

        if email_otp.otp_code == otp_code:

            refresh = RefreshToken.for_user(user)
            return Response({
                "message": "OTP verified successfully.",
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            })

        return Response({"error": "Invalid OTP."}, status=status.HTTP_400_BAD_REQUEST)

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Only owner can edit or delete. Others can only read.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request
        if request.method in permissions.SAFE_METHODS:
            return True
        # Write permissions only for owner
        return obj.owner == request.user
    
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        post = serializer.save(owner=self.request.user)
        log_post_action(self.request.user, post, "create")

    def perform_update(self, serializer):
        post = serializer.save()
        log_post_action(self.request.user, post, "update")

    def perform_destroy(self, instance):
        log_post_action(self.request.user, instance, "delete")
        instance.delete()

    def retrieve(self, request, *args, **kwargs):
        post = self.get_object()
        log_post_action(request.user, post, "retrieve")
        return super().retrieve(request, *args, **kwargs)