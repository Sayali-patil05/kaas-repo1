from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Sum
from .student_progress import calculate_progress
from ..serializers import CourseSerializer
from ..models import Course, CourseEnrollments


@api_view(["GET"])
def view_courses(request):
    # Gets courses from student point of view we also need to implement a get from instructor point of view
    if request.user.role_id.role == "Student":
        enrolled = request.user.courses_enrolled.all()
        enrolled_list = list()

        for course in enrolled:
            progress = calculate_progress(request.user, course)
            temp = CourseSerializer(course).data
            temp.update({"progress": progress})

            enrolled_list.append(temp)

        return Response({"courses": enrolled_list})
    else:
        users_courses = Course.objects.filter(instructor=request.user).all()
        total_students = 0
        total_revenue = 0
        course_list = list()

        for course in users_courses:
            course_dict = CourseSerializer(course).data
            n_students = course.user_set.count()

            revenue = CourseEnrollments.objects.filter(course=course).aggregate(
                total=Sum("price_at_enrollment", default=0.0)
            )["total"]

            course_dict.update({"students": n_students, "revenue": revenue})
            total_students += n_students
            total_revenue += revenue
            course_list.append(course_dict)

        return Response(
            {
                "courses": course_list,
                "students_count": total_students,
                "revenue_generated": total_revenue,
            }
        )


# @api_view(["GET"])
# def course_students(self, request, course_id):
#     if request.user.role_id.role == "Student":
#         return Response(
#             {"message": "Students are not authorized to view this"},
#             status=status.HTTP_401_UNAUTHORIZED,
#         )

#     course = get_object_or_404(Course, pk=course_id)

#     CourseEnrollments.objects.filter(course=course)

#     import pdb

#     pdb.set_trace()
