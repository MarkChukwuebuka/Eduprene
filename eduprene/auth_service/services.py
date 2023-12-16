import logging
from datetime import datetime as dt
from django.utils import timezone

from .models import RegisterLogs, User, UserAccount
from payments.models import UserBankAccount
from rest_framework_simplejwt.tokens import RefreshToken
from constants.other_constants import EMAIL_SUBJECTS, NOTIFICATION_EVENTS, CACHE_PREFIXES

from utils.otp_utils import generate_otp, check_otp_time_expired, verify_otp
from utils.cache_utils import CacheUtil
from utils.other_utils import generate_unique_id
from notifications.tasks import email_queue


def get_registration_log(email):
    log, error = None, None
    try:
        log = RegisterLogs.objects.filter(email=email).first()
    except Exception as e:
        error = e

    return log, error


def send_registration_otp(log, otp):
    send_otp = email_queue.delay(
        email=log.email,
        subject=EMAIL_SUBJECTS['REGISTER_OTP_SENT'],
        message=f"Your One Time Password is {otp}. This will expire in 5 minutes.",
        event=NOTIFICATION_EVENTS['REGISTER_OTP']
    )

    return send_otp, True


def add_registration_log(data):
    # Check if log exists
    email = data['email']
    log, error = CacheUtil.get_cache_value_or_default(prefix=CACHE_PREFIXES['REGISTER_LOGS'], key=email, value_callback=get_registration_log(email))

    if error:
        logging.error(error)

    if log and log.otp_verified:
        return log, False

    generated_otp, hashed_otp = generate_otp()

    # Generate OTP and add to data
    data['otp'] = hashed_otp
    data['otp_requested_at'] = timezone.now()

    if not log:
        log = RegisterLogs.objects.create(**data)

    # Set the value of the old log to the new hashed otp
    log.otp = hashed_otp
    log.save()

    # Cache value for log
    CacheUtil.set_cache_value(prefix=CACHE_PREFIXES['REGISTER_LOGS'], key=email, value=log)

    # Set the raw OTP to send to the email
    log.otp = hashed_otp

    # Send Email with OTP
    send_registration_otp(log, generated_otp)

    print(f"{generated_otp=}")
    return log, True


def resend_registration_otp(data):
    email = data['email']
    log, error = CacheUtil.get_cache_value_or_default(prefix=CACHE_PREFIXES['REGISTER_LOGS'], key=email, value_callback=get_registration_log(email), require_fresh=True)
    
    if error:
        logging.error(error)

    if not log:
        return f"Invalid User", False

    if log and log.otp_verified:
        return f"User verified", False
    
    generated_otp, hashed_otp = generate_otp()

    # Set the value of the old log to the new hashed otp
    log.otp = hashed_otp
    log.otp_requested_at = timezone.now()
    log.otp_trials = 0
    log.save()

    # Cache value for log
    CacheUtil.set_cache_value(prefix=CACHE_PREFIXES['REGISTER_LOGS'], key=email, value=log)

    # Send email with OTP
    send_registration_otp(log, generated_otp)

    print(f"{generated_otp=}")
    return f"OTP sent to {log.email}", True

def verify_registration_otp(data):
    # Create user instance
    email = data['email']

    otp = data['otp']
    log, error = CacheUtil.get_cache_value_or_default(prefix=CACHE_PREFIXES['REGISTER_LOGS'], key=email, value_callback=get_registration_log(email))
    
    if error:
        logging.error(error)

    if log is None:
        return f"Invalid User", False
    
    if log.otp_trials >= 3:
        return f"Too many wrong trials. Request a new OTP", False
    
    # Increment otp_trials by 1 to avoid bruteforcing
    log.otp_trials += 1
    CacheUtil.set_cache_value(prefix=CACHE_PREFIXES['REGISTER_LOGS'], key=email, value=log)
   
    # Validate OTP
    if not verify_otp(otp, log.otp):
        return f"Invalid OTP", False

    # Check OTP time
    otp_expired = check_otp_time_expired(log.otp_requested_at)

    if otp_expired:
        return f"OTP Expired!", False

    log, error = get_registration_log(log.email)

    log.otp_verified = True
    log.save()
    
    user, error = CacheUtil.get_cache_value_or_default(prefix=CACHE_PREFIXES['USER'], key=email, value_callback=create_user(log))

    # Cache value for log
    CacheUtil.set_cache_value(prefix=CACHE_PREFIXES['REGISTER_LOGS'], key=email, value=log)

    token = generate_auth_token(user)
    response_data = {
        "token": token
    }

    return response_data, True


def create_user(log):
    uid = generate_unique_id()
    user_details = {
        "uid": uid,
        "first_name": log.first_name,
        "last_name": log.last_name,
        "username": uid,
        "email": log.email,
        "password": log.password, 
        "is_active": True
    }
    
    user = User.objects.create(**user_details)
    user.save()

    create_user_account(user)
    create_user_bank_account(user)

    return user, None


def create_user_account(user):
    user_account = UserAccount(user=user)
    user_account.save()
    return user_account


def create_user_bank_account(user):
    user_bank_account = UserBankAccount(user=user)
    user_bank_account.save()
    return user_bank_account


def generate_auth_token(user):
    # Generate JWT Token for user.
    token = str(RefreshToken.for_user(user).access_token)
    return token