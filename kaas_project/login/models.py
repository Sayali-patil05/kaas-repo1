from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.contrib.auth.hashers import make_password

class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        User.objects.create(email=email, password=password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        # Admin email = john.doe@gmail.com, password = admin123
        User.objects.create(
            email=email,
            password=password,
            role_id=Role.objects.get(pk=1),
            **extra_fields,
        )


class Role(models.Model):
    ADMIN = "Admin"
    STUDENT = "Student"
    INSTRUCTOR = "Instructor"
    TRAINER = "Trainer"

    ROLE_CHOICES = [
        (ADMIN, "Admin"),
        (STUDENT, "Student"),
        (INSTRUCTOR, "Instructor"),
        (TRAINER, "Trainer"),
    ]

    max_len = max(map(lambda x: len(x[1]), ROLE_CHOICES))

    role_id = models.AutoField(primary_key=True)
    role = models.CharField(choices=ROLE_CHOICES, max_length=max_len)

class User(AbstractBaseUser):
    user_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    mobile_number = models.CharField(max_length=15)

    tagline = models.TextField(max_length=50)
    bio = models.TextField(max_length=255)

    role_id = models.ForeignKey(Role, on_delete=models.PROTECT, default=2)
    aaas_uid = models.IntegerField(null=True)
    reference_number = models.IntegerField(null=True)

    profile_pic = models.TextField()

    courses_enrolled = models.ManyToManyField(
        to="LMS.Course", through="LMS.CourseEnrollments"
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name", "mobile_number"]

    objects = UserManager()

    def __str__(self):
        return self.first_name + " " + self.last_name

    def save(self, *args, **kwargs):
        self.password = make_password(self.password)
        # print(f"called save({self}, {args}, {kwargs})")
        super().save(*args, **kwargs)


class SocialLinks(models.Model):
    link_id = models.AutoField(primary_key=True)
    site_name = models.TextField(max_length=16)
    url = models.TextField(max_length=255)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)


class Login(models.Model):
    login_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.RESTRICT)
    login_date = models.DateTimeField(auto_now_add=True)
    logout_time = models.DateTimeField(null=True)


class UserWishlist(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    course = models.ForeignKey("LMS.Course", null=True, on_delete=models.SET_NULL)


class VerificationOTP(models.Model):
    user = models.OneToOneField(User, on_delete=models.RESTRICT)
    otp = models.IntegerField()
    time_sent = models.DateTimeField(auto_now_add=True)
