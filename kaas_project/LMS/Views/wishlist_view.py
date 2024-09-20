from rest_framework import generics, status
from rest_framework.response import Response
from ..models import Wishlist, Course
from ..serializers import WishlistSerializer, CourseSerializer

class WishlistView(generics.GenericAPIView):
    serializer_class = WishlistSerializer

    def post(self, request, course_id, *args, **kwargs):
        # Check if the user is authenticated
        if not request.user.is_authenticated:
            return Response({"error": "Authentication required."}, status=status.HTTP_401_UNAUTHORIZED)

        # Prepare data for wishlist entry
        wishlist_data = {
            "course": course_id,  # Directly use the course_id
        }

        # Ensure the course exists
        try:
            course = Course.objects.get(course_id=course_id)
        except Course.DoesNotExist:
            return Response({"error": "Course does not exist."}, status=status.HTTP_404_NOT_FOUND)

        # Check if the course is already in the wishlist
        if Wishlist.objects.filter(user=request.user, course=course).exists():
            return Response({"error": "Course is already in the wishlist."}, status=status.HTTP_400_BAD_REQUEST)

        # Use the serializer to save the wishlist entry
        serializer = self.get_serializer(data=wishlist_data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user, course=course)  # Pass user and course directly to save
        return Response({"course": CourseSerializer(course).data, "message": "Course added to wishlist successfully."}, status=status.HTTP_201_CREATED)

    def delete(self, request, course_id, *args, **kwargs):
        # Check if the user is authenticated
        if not request.user.is_authenticated:
            return Response({"error": "Authentication required."}, status=status.HTTP_401_UNAUTHORIZED)

        # Remove course from wishlist
        try:
            wishlist_item = Wishlist.objects.get(user=request.user, course__course_id=course_id)
            wishlist_item.delete()
            return Response({"message": "Course removed from wishlist successfully."}, status=status.HTTP_204_NO_CONTENT)
        except Wishlist.DoesNotExist:
            return Response({"error": "Course is not in your wishlist."}, status=status.HTTP_404_NOT_FOUND)

    def get(self, request, *args, **kwargs):
        # Check if the user is authenticated
        if not request.user.is_authenticated:
            return Response({"error": "Authentication required."}, status=status.HTTP_401_UNAUTHORIZED)

        # Retrieve all wishlist items for the user
        wishlist_items = Wishlist.objects.filter(user=request.user).select_related('course')
        serializer = WishlistSerializer(wishlist_items, many=True)
        
        # Include course details
        response_data = [
            {
                "course": CourseSerializer(item.course).data,
                "added_at": item.added_at
            } for item in wishlist_items
        ]

        return Response(response_data, status=status.HTTP_200_OK)


