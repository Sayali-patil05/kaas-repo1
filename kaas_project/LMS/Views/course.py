from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models import Course, CourseEnrollments, Category
from ..serializers import CourseSerializer, CourseWriteSerializer
from .average_rating import get_average_rating
from django.db.models import Prefetch
from drf_yasg.utils import swagger_auto_schema


class Courses(APIView):
    # GET /lms/courses [gets all available courses, unless an ID is specified]
    def get(self, request, *args, **kwargs):
        if course_id := kwargs.get("pk"):
            course = (
                Course.objects.filter(pk=course_id)
                .prefetch_related(
                    Prefetch("categories", queryset=Category.objects.all())
                )
                .first()
            )

            isInstructor = False
            if course.instructor == request.user:
                isInstructor = True

            isEnrolled = CourseEnrollments.objects.filter(
                user=request.user, course=course
            ).exists()

            course_dict = {
                "course_id": course.course_id,
                "title": course.title,
                "start_date": course.start_date,
                "price": course.price,
                "description": course.description,
                "categories": [category.name for category in course.categories.all()],
                "trailer": course.trailer,
                "cover_img": course.cover_img,
            }
            ins = course.instructor
            ins_details = {
                "full_name": str(ins.first_name + " " + ins.last_name).capitalize(),
            }
            course_dict.update(
                {
                    "instructor": ins_details["full_name"],
                    "rating": get_average_rating(course_id=course.course_id),
                    "display": {
                        "is_instructor": isInstructor,
                        "is_enrolled": isEnrolled,
                    },
                }
            )

            return Response(course_dict)
        else:
            courses = Course.objects.prefetch_related(
                Prefetch("categories", queryset=Category.objects.all())
            )
            course_list = []
            for course in courses:
                course_dict = {
                    "course_id": course.course_id,
                    "title": course.title,
                    "start_date": course.start_date,
                    "price": course.price,
                    "description": course.description,
                    "categories": [
                        category.name for category in course.categories.all()
                    ],
                    "cover_img": course.cover_img,
                }
                ins = course.instructor
                ins_details = {
                    "name": str(ins.first_name + " " + ins.last_name).capitalize(),
                }
                course_dict.update(
                    {
                        "instructor": ins_details,
                        "rating": get_average_rating(course_id=course.course_id),
                    }
                )
                course_list.append(course_dict)
            return Response({"courses": course_list})

    @swagger_auto_schema(
        request_body=CourseWriteSerializer,
        responses={
            400: "Invalid input",
            403: "Forbidden",
        },
    )
    def put(self, request):
        # TODO: Add Validations start_date must be in the future

        user_role = (
            request.user.role_id.role
        )  # TODO: Validate if the user is an instructor

        serializer = CourseWriteSerializer(data=request.data)

        if serializer.is_valid():
            title = serializer.validated_data["title"]
            start_date = serializer.validated_data["start_date"]
            price = serializer.validated_data["price"]
            description = serializer.validated_data["description"]
            categories = serializer.validated_data["categories"]
            trailer = serializer.validated_data["trailer"]

            db_categories = []

            for category in categories:
                obj, created = Category.objects.get_or_create(name=category)
                db_categories.append(obj)

            created_course = Course.objects.create(
                title=title,
                start_date=start_date,
                price=price,
                description=description,
                instructor=request.user,
                trailer=trailer,
            )

            created_course.categories.add(*db_categories)

            if created_course:
                return Response(
                    {"message": "Course created sucessfully"},
                    status=status.HTTP_201_CREATED,
                )
            else:
                return Response({"error": "Something horrible went wrong"})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        request_body=CourseSerializer,
        responses={
            400: "Invalid input",
            403: "Forbidden",
        },
    )
    def patch(self, request, pk):
        course = get_object_or_404(Course, pk=pk)

        # Check if the user_id of currently logged in user matches the instructor id of course
        # Only the instructor can modify or delete the course
        if course.instructor.user_id != request.user.user_id:
            return Response(
                {"error": "User is unauthorized to update this course"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        serializer = CourseSerializer(course, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # DELETE /lms/courses/<course_id>/ [Delete a course]
    def delete(self, request, pk):
        course = get_object_or_404(Course, pk=pk)

        # Check if the user_id of currently logged in user matches the instructor id of course
        # Only the instructor can modify or delete the course
        if course.instructor.user_id != request.user.user_id:
            return Response(
                {"error": "User is unauthorized to delete this course"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        course.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
