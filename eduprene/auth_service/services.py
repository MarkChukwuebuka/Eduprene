import logging
from datetime import datetime as dt

from .models import RegisterLogs

from constants.other_constants import EMAIL_SUBJECTS, NOTIFICATION_EVENTS, CACHE_PREFIXES

from utils.otp_utils import check_otp_time_expired, generate_otp
from utils.cache_utils import CacheUtil

from notifications.controllers import EmailService
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
    log, error = CacheUtil.get_cache_value_or_default(prefix=CACHE_PREFIXES['REGISTER_LOGS'], key=email,
                                                      value_callback=get_registration_log(email))

    if error:
        logging.error(error)

    if log and log.otp_verified:
        return log, False

    generated_otp, hashed_otp = generate_otp()

    # Generate OTP and add to data
    data['otp'] = hashed_otp
    data['otp_requested_at'] = dt.now()

    if not log:
        log = RegisterLogs.objects.create(**data)

    # Set the value of the old log to the new hashed otp
    log.otp = hashed_otp
    log.save()

    # Cache value for log
    CacheUtil.set_cache_value(prefix=CACHE_PREFIXES['REGISTER_LOGS'], key=email, value=log)

    # Set the raw OTP to send to the email
    log.otp = generated_otp

    # Send Email with OTP
    send_registration_otp(log, generate_otp)

    print(f"{generated_otp=}")
    return log, True


def resend_registration_otp(data):
    email = data['email']
    log, error = CacheUtil.get_cache_value_or_default(prefix=CACHE_PREFIXES['REGISTER_LOGS'], key=email,
                                                      value_callback=get_registration_log(email))
    
    if error:
        logging.error(error)

    if not log:
        return f"Invalid User", False

    if log and log.otp_verified:
        return f"User verified", False
    
    generated_otp, hashed_otp = generate_otp()

    # Set the value of the old log to the new hashed otp
    log.otp = hashed_otp
    log.save()

    # Cache value for log
    CacheUtil.set_cache_value(prefix=CACHE_PREFIXES['REGISTER_LOGS'], key=email, value=log)

    # Send email with OTP
    send_registration_otp(log, generated_otp)

    print(f"{generated_otp=}")
    return f"OTP sent to {log.email}", True
