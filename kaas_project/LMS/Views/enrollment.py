from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from ..models import Course, CourseEnrollments


class Enrollment(APIView):

    def post(self, request, course_id):
        course = get_object_or_404(Course, pk=course_id)

        already_enrolled = CourseEnrollments.objects.filter(
            user=request.user, course=course
        ).exists()

        if already_enrolled:
            return Response(
                {"error": f"You have already enrolled for course {course.title}"},
                status=status.HTTP_406_NOT_ACCEPTABLE,
            )

        enrollment = CourseEnrollments.objects.create(
            user=request.user, course=course, price_at_enrollment=course.price
        )

        return Response(
            {
                "message": "User enrollment sucessfull",
                "enrollment_number": enrollment.enrollment_number,
                "enrollment_date": enrollment.date_enrolled,
            }
        )
