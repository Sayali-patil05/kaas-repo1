from rest_framework import generics
from ..serializers import UserRetrieveSerializer, UserUpdateSerializer
from drf_yasg.utils import swagger_auto_schema


class UserDetailView(generics.RetrieveUpdateAPIView):
    def get_object(self):
        return self.request.user

    def get_serializer_class(self):
        if self.request.method in ["PUT", "PATCH"]:
            return UserUpdateSerializer
        return UserRetrieveSerializer

    @swagger_auto_schema(responses={200: UserRetrieveSerializer})
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        request_body=UserUpdateSerializer,
        responses={200: UserRetrieveSerializer, 400: "Invalid input"},
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(
        request_body=UserUpdateSerializer,
        responses={200: UserRetrieveSerializer, 400: "Invalid input"},
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)
