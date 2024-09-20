from django.urls import path
from .Views import login, sign_up, logout, forgot_password

urlpatterns = [
    path("login/", login.LoginView.as_view()),
    path("signup/", sign_up.SignUpView.as_view()),
    path("signup-instructor/", sign_up.SignUpInstructorView.as_view()),
    # path("login-history/", login_history.get_login_history),
    path("logout/", logout.logout_user),
    path("forgot-password/", forgot_password.ForgotPasswordView.as_view()),
]
