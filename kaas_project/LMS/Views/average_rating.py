from ..models import CourseReviews
from django.db.models import Avg


def get_average_rating(course_id: int) -> float:
    rating = CourseReviews.objects.filter(course=course_id).aggregate(
        avg_rating=Avg("rating")
    )["avg_rating"]

    return rating if rating is not None else 0
