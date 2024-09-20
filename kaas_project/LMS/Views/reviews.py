from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from ..models import Course, CourseReviews, CourseEnrollments
from ..serializers import ReviewSerializer, ReviewCreateSerializer
from drf_yasg.utils import swagger_auto_schema

class ReviewsView(APIView):
    def get(self, request, course_id):
        # Get the course or return 404 if not found
        course = get_object_or_404(Course, pk=course_id)
        # Fetch all reviews for the course
        reviews = CourseReviews.objects.filter(course=course)
        # Serialize the reviews
        serializer = ReviewSerializer(reviews, many=True)
        # Return the serialized data
        return Response({"reviews": serializer.data}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=ReviewCreateSerializer,
        responses={
            400: "Invalid input",
            403: "Forbidden",
        },
    )
    def post(self, request, course_id):
        # Get the course or return 404 if not found
        course = get_object_or_404(Course, pk=course_id)

        if CourseReviews.objects.filter(user=request.user, course=course).exists():
            return Response(
                {"error": "Cannot post multiple reviews"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Get the data from the request
        create_serializer = ReviewCreateSerializer(data=request.data)
        if create_serializer.is_valid():
            data = create_serializer.validated_data
            data["course"] = course
            data["user"] = request.user

        is_enrolled = CourseEnrollments.objects.filter(
            user=request.user, course=course
        ).exists()

        if not is_enrolled:
            return Response(
                {"error": "Cannot review course you have not enrolled for"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        # Create a new review instance
        serializer = ReviewSerializer(data=data)

        # Validate and save the review
        if serializer.is_valid():
            created_review = CourseReviews.objects.create(
                user=request.user,
                course=course,
                review=serializer.data["review"],
                rating=serializer.data["rating"],
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        request_body=ReviewCreateSerializer,
        responses={
            400: "Invalid input",
            403: "Forbidden",
        },
    )
    def put(self, request, course_id, review_id):
        # Get the course or return 404 if not found
        course = get_object_or_404(Course, pk=course_id)
        # Get the review or return 404 if not found
        review = get_object_or_404(CourseReviews, pk=review_id, course=course)

        if review.user != request.user:
            return Response(
                {"error": "User is not the author of the review"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        # Update the review with the request data
        serializer = ReviewSerializer(review, data=request.data)
        # Validate and save the review
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, course_id, review_id):
        # Get the course or return 404 if not found
        course = get_object_or_404(Course, pk=course_id)
        # Get the review or return 404 if not found
        review = get_object_or_404(CourseReviews, pk=review_id, course=course)
        # Delete the review
        review.delete()
        # Return a success response
        return Response(status=status.HTTP_204_NO_CONTENT)
