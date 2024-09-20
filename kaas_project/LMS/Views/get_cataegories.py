from rest_framework.generics import ListAPIView
from ..models import Category
from ..serializers import CategorySerializer
from drf_yasg.utils import swagger_auto_schema


class CategoryRetrieveAPIView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    @swagger_auto_schema(
        responses={
            200: CategorySerializer,
        },
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
