from ..models import User, VerificationOTP
from django.core.mail import send_mail
from datetime import datetime
from django.utils import timezone
import random
from django.conf import settings


EMAIL_TEMPLATE_STR = """
Dear {name},

We hope this message finds you well.

You have requested to reset your password. Please use the following One-Time Password (OTP) to proceed with the password reset process:

{otp}

If you did not request this change, please disregard this message, or contact our support team immediately.

Thank you for your attention to this matter.

Best regards,
The KaaS (Knowledge as a Service) Application
"""


def send_otp(user: User) -> bool:
    name = user.first_name + " " + user.last_name
    # WARNING: I am not basic random is prone to any kind of cryptographic attacks
    otp = random.randint(1000, 9999)  # 4 digit OTP is probably ok for now

    result = send_mail(
        subject="OTP to reset KaaS Password",
        message=EMAIL_TEMPLATE_STR.format(name=name, otp=otp),
        from_email="kaas10593@gmail.com",
        recipient_list=[user.email],
        fail_silently=False,
    )

    if bool(result):
        otp_obj = VerificationOTP.objects.create(user=user, otp=otp)
        if otp_obj:
            # print(f"OTP created for {user.email} -> {otp}")
            return True
        else:
            return False
    else:
        return bool(result)


def validate_otp(user: User, req_otp: int) -> bool:
    verified = VerificationOTP.objects.filter(user=user, otp=req_otp).first()

    if verified:
        curr_time = timezone.now()
        otp_sent_time = verified.time_sent

        diff = curr_time - otp_sent_time

        otp_ttl = getattr(
            settings, "OTP_TTL_MIN", 10
        )  # OTP Valid for 10 min by default

        diff_min = int(diff.total_seconds() / 60)

        # TODO: Uncomment later for expiring OTP
        if diff_min <= otp_ttl:
            verified.delete()
            return True
        else:
            return False
    else:
        return False


def delete_otp(user: User) -> None:
    users_otp = VerificationOTP.objects.filter(user=user).first()
    # print(f"Deleted OTP for {user.email} -> {users_otp.otp}")
    users_otp.delete()
