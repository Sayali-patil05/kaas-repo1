from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from ..models import Material, Course, CourseEnrollments, ViewRecord
from ..serializers import CourseSerializer, MaterialSerializer


class RecordView(APIView):
    def post(self, request, course_id, material_id):
        course = get_object_or_404(Course, pk=course_id)
        material = get_object_or_404(Material, pk=material_id)

        viewed_instructor = course.instructor == request.user

        is_enrolled = (
            CourseEnrollments.objects.filter(user=request.user, course=course).exists()
            or viewed_instructor
        )

        material_valid = Material.objects.filter(pk=material_id, course=course).exists()

        if not is_enrolled:
            return Response(
                {"error": "User has not enrolled for the course"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        if not material_valid:
            return Response(
                {"error": "This Material does not belong to the given course"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if not viewed_instructor:
            print("Skipping since instructor is viewing")
            ViewRecord.objects.create(
                user=request.user, material=material, course=course.course_id
            )

        return Response({"message": "View added"})
