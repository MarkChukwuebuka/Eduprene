from .models import RegisterLogs


def get_registration_log(email):
    return RegisterLogs.objects.get(email=email).cache()


def add_registration_log(data):
    # Check if log exists
    log = get_registration_log(data['email'])

    if log is None:
        log = RegisterLogs.objects.create(**data).cache()
        # Send Email with OTP

        return log

