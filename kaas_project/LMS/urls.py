from django.urls import path
from .Views import (
    course,
    enrollment,
    materials,
    record_views,
    user,
    user_course,
    reviews,
    wishlist_view,
    course_student,
    dashboard,
    get_cataegories,
)

urlpatterns = [
    path("courses/", course.Courses.as_view()),
    path("courses/<int:pk>/", course.Courses.as_view()),
    path("courses/<int:pk_course>/materials/", materials.CourseMaterials.as_view()),
    path("courses/material/<int:pk>/", materials.MaterialRetrieveAPIView.as_view()),
    path("enroll/<int:course_id>/", enrollment.Enrollment.as_view()),
    path("view/<int:course_id>/<int:material_id>/", record_views.RecordView.as_view()),
    path("user/", user.UserDetailView.as_view(), name="user-detail"),
    path("user/courses/", user_course.view_courses, name="user-courses"),
    path("review/<int:course_id>/", reviews.ReviewsView.as_view()),
    path("review/<int:course_id>/<int:review_id>/", reviews.ReviewsView.as_view()),
    path('user/wishlist/', wishlist_view.WishlistView.as_view(), name='wishlist-list'),
    path('user/wishlist/<int:course_id>/', wishlist_view.WishlistView.as_view() , name='wishlist-detail'),
    path(
        "courses/<int:course_id>/students/",
        course_student.CourseStudentsView.as_view(),
        name="course-students",
    ),
    path("dashboard/", dashboard.DasboardView.as_view()),
    path(
        "categories/",
        get_cataegories.CategoryRetrieveAPIView.as_view(),
        name="get-categories",
    ),
]
