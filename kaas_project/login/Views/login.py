from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from ..serializers import LoginSerializer
from ..models import User, Login, Role
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate
from drf_yasg.utils import swagger_auto_schema


# POST /auth/login
# {
#     "email": "jane.doe@example.com",
#     "password": "SecurePass!2024"
# }

# URL -> /auth/login
class LoginView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        request_body=LoginSerializer,
        responses={400: "Invalid Credentials"},
    )
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            try:
                request_email = serializer.validated_data["email"]
                request_passw = serializer.validated_data["password"]

                user = authenticate(
                    request=request, email=request_email, password=request_passw
                )

                if user:
                    refresh = RefreshToken.for_user(user)
                    Login.objects.create(user=user)

                    role = user.role_id.role

                    return Response(
                        {
                            "refresh": str(refresh),
                            "access": str(refresh.access_token),
                            "role": role,
                        }
                    )
                else:
                    return Response(
                        {"error": "Invalid Credentials"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
            except User.DoesNotExist:
                return Response(
                    {"error": "Invalid Credentials"}, status=status.HTTP_400_BAD_REQUEST
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
