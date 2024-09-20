from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Course, Material, CourseReviews, Category, CourseEnrollments, ViewRecord, Wishlist
from django.apps import apps
from .Views.student_progress import calculate_progress

User = get_user_model()


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["category_id", "name"]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["user_id", "first_name", "last_name", "email"]

class EnrollmentSerializer(serializers.ModelSerializer):
    user = UserSerializer()  # Nested UserSerializer to include user details
    progress = serializers.SerializerMethodField()  # Declare progress here

    class Meta:
        model = CourseEnrollments
        fields = ["user", "date_enrolled", "progress"]  # Include 'progress' in fields

    def get_progress(self, obj):
        course, user = obj.course, obj.user
        progress = calculate_progress(user, course)

        return round(progress * 100, 2)

class CourseSerializer(serializers.ModelSerializer):
    categories = serializers.StringRelatedField(many=True)

    class Meta:
        model = Course
        fields = [
            "course_id",
            "title",
            "start_date",
            "reference_num",
            "price",
            "description",
            "categories",
            "trailer",
            "cover_img",
        ]

class CourseWithEnrollmentsSerializer(serializers.ModelSerializer):
    categories = serializers.StringRelatedField(many=True)
    students = EnrollmentSerializer(source="courseenrollments_set", many=True)

    class Meta:
        model = Course
        fields = [
            "course_id",
            "title",
            "start_date",
            "reference_num",
            "price",
            "description",
            "categories",
            "trailer",
            "cover_img",
            "students",  # Include the student enrollment data
        ]

class CourseWriteSerializer(serializers.ModelSerializer):
    categories = serializers.ListField()

    class Meta:
        model = Course
        fields = [
            "course_id",
            "title",
            "start_date",
            "reference_num",
            "price",
            "description",
            "categories",
            "trailer",
            "cover_img",
        ]

class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = ["material_id", "file_name", "file_type", "upload_date", "data"]

class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    course = serializers.StringRelatedField()
    class Meta:
        model = CourseReviews
        fields = ["review_id", "user", "course", "review", "rating", "created_at"]
        read_only_fields = ["review_id", "created_at"]

    def create(self, validated_data):
        # Ensure that the user is the one making the request
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            validated_data["user"] = request.user
        return super().create(validated_data)

class ReviewCreateSerializer(serializers.Serializer):
    review = serializers.CharField()
    rating = serializers.IntegerField(min_value=0, max_value=5)

class SocialLinksSerializer(serializers.ModelSerializer):
    class Meta:
        model = apps.get_model("login", "SocialLinks")
        fields = ["site_name", "url"]

class UserRetrieveSerializer(serializers.ModelSerializer):
    social_links = SocialLinksSerializer(
        many=True, read_only=True, source="sociallinks_set"
    )

    class Meta:
        model = User
        fields = [
            "user_id",
            "first_name",
            "last_name",
            "email",
            "mobile_number",
            "tagline",
            "bio",
            "role_id",
            "profile_pic",
            "social_links",
        ]

class UserUpdateSerializer(serializers.ModelSerializer):
    social_links = SocialLinksSerializer(many=True, write_only=True)

    class Meta:
        model = User
        fields = ["tagline", "bio", "profile_pic", "social_links"]

    def update(self, instance, validated_data):
        social_links_data = validated_data.pop("social_links", [])

        instance = super().update(instance, validated_data)

        SocialLinks = apps.get_model("login", "SocialLinks")

        # Update social links
        for link_data in social_links_data:
            SocialLinks.objects.create(user=instance, **link_data)

        return instance


class WishlistSerializer(serializers.ModelSerializer):
    course = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all())
    course_details = CourseSerializer(source='course', read_only=True)

    class Meta:
        model = Wishlist
        fields = ['course', 'course_details']  # Added course_details for nested representation

    def create(self, validated_data):
        # Extract the user from the context
        request = self.context.get('request')
        user = request.user
        validated_data['user'] = user  # Set the user on the wishlist instance
        
        # Ensure that the course exists and the user is not adding it again
        course = validated_data['course']
        if Wishlist.objects.filter(user=user, course=course).exists():
            raise serializers.ValidationError("Course is already in the wishlist.")

        return Wishlist.objects.create(**validated_data)

    def update(self, instance, validated_data):
        # This function can be implemented if you want to update wishlist items
        instance.save()  # Add any updates as necessary
        return instance
