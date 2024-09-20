from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ..models import Login
from django.utils.timezone import now


@api_view(["POST"])
def logout_user(request):
    if not request.user:
        Response(
            {"error": "User must be logged in first"},
            status=status.HTTP_401_UNAUTHORIZED,
        )
    last_login = (
        Login.objects.filter(user=request.user, logout_time__isnull=True)
        .order_by("login_date")
        .first()
    )

    if last_login:
        last_login.logout_time = now()
        last_login.save()
        return Response({"message": "User logged out sucessfully"})
    else:
        return Response(
            {"message": "User is not currently logged in"},
            status=status.HTTP_400_BAD_REQUEST,
        )
