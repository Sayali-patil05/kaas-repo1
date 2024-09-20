from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models import CourseEnrollments, Course
from ..serializers import EnrollmentSerializer

class CourseStudentsView(APIView):
    def get(self, request, course_id):
        try:
            course = Course.objects.get(course_id=course_id)
        except Course.DoesNotExist:
            return Response({"detail": "Course not found"}, status=status.HTTP_404_NOT_FOUND)
    
        enrollments = CourseEnrollments.objects.filter(course=course)

        if not enrollments.exists():
            return Response({"students": []}, status=status.HTTP_200_OK)
        
        serializer = EnrollmentSerializer(enrollments, many=True)
        return Response({"students": serializer.data}, status=status.HTTP_200_OK)
