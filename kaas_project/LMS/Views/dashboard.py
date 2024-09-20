from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .streak import calculate_streak
from ..models import Course, CourseEnrollments

from django.apps import apps
from django.db.models import Sum, Count


class DasboardView(APIView):
    def get(self, request):
        user_role = request.user.role_id.role

        if user_role == "Student":
            n_courses = len(request.user.courses_enrolled.all())

            Login = apps.get_model("login.Login")
            history = Login.objects.filter(user=request.user)

            logins = sorted(list(set((map(lambda x: x.login_date.date(), history)))))

            curr_streak, longest = calculate_streak(logins)

            return Response(
                {
                    "metrics": [
                        {
                            "label": "Number of Courses enrolled",
                            "value": f"{n_courses} Courses",
                        },
                        {"label": "Current Streak", "value": f"{curr_streak} Days"},
                        {"label": "Longest streak", "value": f"{longest} Days"},
                    ]
                }
            )
        elif user_role == "Instructor":
            courses = Course.objects.filter(instructor=request.user).all()

            res = CourseEnrollments.objects.filter(course__in=courses).aggregate(
                total_students=Count("user", distinct=False),
                total_revenue=Sum("price_at_enrollment"),
            )

            students = (
                res.get("total_students") if res.get("total_students") == 0 else "No"
            )
            revenue = (
                res.get("total_revenue") if res.get("total_revenue") is not None else 0
            )

            return Response(
                {
                    "metrics": [
                        {
                            "label": "Courses created",
                            "value": f"{len(courses)} Courses",
                        },
                        {
                            "label": "Total Number of student",
                            "value": f"{students} Students",
                        },
                        {
                            "label": "Total Revenue Earned",
                            "value": f"USD {revenue:.2f}",
                        },
                    ]
                }
            )
