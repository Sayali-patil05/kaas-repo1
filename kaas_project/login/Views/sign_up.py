from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from ..serializers import SignUpSerializer
from ..models import User, Role
from rest_framework.permissions import AllowAny
from drf_yasg.utils import swagger_auto_schema

class SignUpView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        request_body=SignUpSerializer,
        responses={400: "Invalid input"},
    )
    def post(self, request):
        # print(request.data)
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get("email")
            password = serializer.validated_data.get("password")
            first_name = serializer.validated_data.get("first_name")
            last_name = serializer.validated_data.get("last_name")
            mobile_number = serializer.validated_data.get("mobile_number")
            reference_num = serializer.validated_data.get("reference_number")

            # print("Serialized")

            created_user = User.objects.create(
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
                mobile_number=mobile_number,
            )

            if created_user:
                return Response(
                    {"message": "User Created sucessfully"},
                    status=status.HTTP_201_CREATED,
                )
            else:
                return Response(
                    {"error": "Something beyond my knowledge is gone wrong"}
                )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Uses same request as Sign up just sets an additional role field
class SignUpInstructorView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        request_body=SignUpSerializer,
        responses={400: "Invalid input"},
    )
    def post(self, request):
        # print(request.data)
        serializer = SignUpSerializer(data=request.data)

        instructor_role = Role.objects.get(pk=3)

        if serializer.is_valid():
            email = serializer.validated_data.get("email")
            password = serializer.validated_data.get("password")
            first_name = serializer.validated_data.get("first_name")
            last_name = serializer.validated_data.get("last_name")
            mobile_number = serializer.validated_data.get("mobile_number")
            reference_num = serializer.validated_data.get("reference_number")

            # print("Serialized")

            created_user = User.objects.create(
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
                mobile_number=mobile_number,
                role_id=instructor_role,
            )

            if created_user:
                return Response(
                    {"message": "User Created sucessfully"},
                    status=status.HTTP_201_CREATED,
                )
            else:
                return Response(
                    {"error": "Something beyond my knowledge is gone wrong"}
                )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
