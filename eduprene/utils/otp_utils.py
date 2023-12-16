import random
from django.utils import timezone
from django.contrib.auth.hashers import make_password, check_password


def generate_otp():
    otp = str(random.randint(100000, 999999))
    hashed_otp = make_password(otp)
    return otp, hashed_otp


def check_otp_time_expired(otp_requested_at):
    created_at = otp_requested_at
    current_time = timezone.now()

    time_difference = current_time - created_at
    time_difference_minutes = time_difference.seconds / 60

    if time_difference_minutes > 5:
        return True

    return False


def verify_otp(otp, hashed_otp):
    return check_password(otp, hashed_otp)