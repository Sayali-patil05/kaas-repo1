from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from ..serializers import ForgotPasswordSerializer, PasswordResetSerializer
from ..models import User
from .otp_util import send_otp, validate_otp, delete_otp
from django.conf import settings
from django.utils import timezone

from threading import Timer  # OTP Delete delay

otp_delete_timer: Timer = None


class ForgotPasswordView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        request_body=ForgotPasswordSerializer,
        responses={400: "Serializer Errors"},
    )
    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)

        if serializer.is_valid():
            req_email = serializer.validated_data["email"]
            user = get_object_or_404(User, email=req_email)

            otp_sent = send_otp(user)

            otp_ttl = getattr(settings, "OTP_TTL_MIN", 10)

            delay = otp_ttl * 60.0

            global otp_delete_timer
            otp_delete_timer = Timer(delay, delete_otp, args=[user])
            otp_delete_timer.start()

            otp_sent_time = timezone.now()

            if not otp_sent:
                return Response(
                    {"message": "OTP couldn't be sent"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            return Response(
                {
                    "message": f"OTP has been sent to email {user.email}",
                    "OTP_sent": otp_sent_time,  # Used for timer in the frontend
                    "OTP_duration": otp_ttl,
                }
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        request_body=PasswordResetSerializer,
        responses={400: "Serializer Errors"},
    )
    def patch(self, request):
        serializer = PasswordResetSerializer(data=request.data)
        if serializer.is_valid():
            req_email = serializer.validated_data["email"]
            req_otp = serializer.validated_data["otp"]
            new_pass = serializer.validated_data["new_password"]
            user = get_object_or_404(User, email=req_email)

            if validate_otp(user, req_otp):
                user.password = new_pass
                user.save()
                user.refresh_from_db()

                global otp_delete_timer
                otp_delete_timer.cancel()

                return Response(
                    {"message": "Password has been changed"}, status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {
                        "message": "OTP verification failed OTP has expired or is incorrect"
                    },
                    status=status.HTTP_401_UNAUTHORIZED,
                )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
