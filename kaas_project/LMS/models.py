from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth import get_user_model


class Category(models.Model):
    category_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


# Create your models here.
class Course(models.Model):
    from django.contrib.auth import get_user_model

    user_model = get_user_model()

    course_id = models.AutoField(primary_key=True)
    title = models.TextField(max_length=100)
    start_date = models.DateField(auto_created=True)
    reference_num = models.IntegerField(null=True)
    instructor = models.ForeignKey(to=user_model, on_delete=models.CASCADE)
    price = models.FloatField()  # INFO: The API assumes this price is in USD
    description = models.TextField()
    categories = models.ManyToManyField(Category)

    trailer = models.TextField(null=True)
    cover_img = models.TextField(null=True)

    # duration_days = models.IntegerField

    def __str__(self):
        return self.title


class Material(models.Model):
    file_types = ["pdf", "docx", "ppt", "mp4"]
    file_type_map = list(zip(file_types, file_types))

    max_len = max(map(lambda x: len(x[0]), file_type_map))

    material_id = models.AutoField(primary_key=True)
    file_name = models.TextField()
    file_type = models.CharField(choices=file_type_map, max_length=max_len)
    upload_date = models.DateTimeField(auto_now_add=True)
    course = models.ForeignKey(Course, null=True, on_delete=models.SET_NULL)
    data = models.TextField()


class CourseEnrollments(models.Model):
    from django.contrib.auth import get_user_model

    enrollment_number = models.AutoField(primary_key=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True)
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True)
    date_enrolled = models.DateTimeField(auto_now=True)
    price_at_enrollment = models.FloatField(default=0)


class ViewRecord(models.Model):
    from django.contrib.auth import get_user_model

    user_model = get_user_model()

    user = models.ForeignKey(to=user_model, on_delete=models.SET_NULL, null=True)
    material = models.ForeignKey(to=Material, on_delete=models.SET_NULL, null=True)
    course = models.IntegerField(null=False)
    view_date = models.DateTimeField(auto_now=True)


class CourseReviews(models.Model):
    from django.contrib.auth import get_user_model

    user_model = get_user_model()

    review_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(to=user_model, on_delete=models.SET_NULL, null=True)
    course = models.ForeignKey(to=Course, on_delete=models.SET_NULL, null=True)
    review = models.TextField(max_length=255)
    rating = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(5)]
    )
    created_at = models.DateTimeField(auto_created=True, auto_now_add=True)


# Adding the Wishlist model
class Wishlist(models.Model):
    user_model = get_user_model()

    user = models.ForeignKey(user_model, on_delete=models.CASCADE)  # The student adding to wishlist
    course = models.ForeignKey(Course, on_delete=models.CASCADE)  # The course being added to wishlist
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'course')  # A user can only add a course once to the wishlist

    def __str__(self):
        return f"{self.user} added {self.course} to wishlist"