from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.generics import RetrieveAPIView
from ..models import Material, Course
from ..serializers import CourseSerializer, MaterialSerializer
from drf_yasg.utils import swagger_auto_schema


def serialize(x):
    return_dict = MaterialSerializer(x).data
    return_dict.pop("data")
    return return_dict


class CourseMaterials(APIView):

    def get(self, request, pk_course, **kwargs):
        course = get_object_or_404(Course, pk=pk_course)
        materials_list = list(
            map(serialize, Material.objects.filter(course=course).values())
        )

        return Response(
            {"materials": list(materials_list), "count": len(materials_list)},
            status=status.HTTP_200_OK,
        )

    @swagger_auto_schema(
        request_body=MaterialSerializer,
        responses={
            400: "Invalid input",
            403: "Forbidden",
        },
    )
    def put(self, request, pk_course):
        serializer = MaterialSerializer(data=request.data)
        course = get_object_or_404(Course, pk=pk_course)

        # Check if the user_id of currently logged in user matches the instructor id of course
        # Only the instructor can upload modify or delete the materials
        if course.instructor.user_id != request.user.user_id:
            return Response(
                {"error": "User is unauthorized to add material to this course"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        if serializer.is_valid():
            file_name = serializer.validated_data["file_name"]
            file_type = serializer.validated_data["file_type"]
            data = serializer.validated_data["data"]

            material = Material.objects.create(
                file_name=file_name, file_type=file_type, course=course, data=data
            )

            if material:
                return Response(
                    {"message": "Material upload sucessfully"},
                    status=status.HTTP_201_CREATED,
                )
            else:
                return Response({"error": "Something horrible went wrong"})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        request_body=MaterialSerializer,
        responses={
            400: "Invalid input",
            403: "Forbidden",
        },
    )
    def patch(self, request, material_id):
        material = get_object_or_404(Material, pk=material_id)
        course = material.course

        # Check if the user_id of currently logged in user matches the instructor id of course
        # Only the instructor can modify or delete the course
        if course.instructor.user_id != request.user.user_id:
            return Response(
                {"error": "User is unauthorized to update material for this course"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        serializer = MaterialSerializer(material, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, material_id):
        material = get_object_or_404(Material, pk=material_id)
        course = material.course

        if course.instructor.user_id != request.user.user_id:
            return Response(
                {"error": "User is unauthorized to delete material for this course"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        material.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class MaterialRetrieveAPIView(RetrieveAPIView):
    queryset = Material.objects.all()
    serializer_class = MaterialSerializer

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
