from .models import Emails
from utils.other_utils import generate_referral_code
from notifications.tasks import email_queue
from constants.other_constants import EMAIL_SUBJECTS, NOTIFICATION_EVENTS

def send_email_collector_email(send_email_collector_email):
    message = f"""
    Hello {send_email_collector_email.first_name}, you have registered to be one of the first people to be notified when Eduprene launches 🤝🏾.\n 
    
    Your referral link is https://learn.eduprene.com/landing?code={send_email_collector_email.referral_code}.\n\n
    
    Earn big bonuses when you refer your friends and colleagues to also earn from reading articles on Eduprene. 
    """
    
    send_email = email_queue.delay(
        email=send_email_collector_email.email,
        subject=EMAIL_SUBJECTS['EMAIL_COLLECTOR_EMAIL_SAVED'],
        message=message,
        event=NOTIFICATION_EVENTS['EMAIL_COLLECTOR']
    )

    return send_email, True

def add_email_collected(data):
    referral_code = generate_referral_code(Emails)

    data["referral_code"] = referral_code

    email_collected_data = Emails.objects.create(**data)

    # Send email with Referral Code
    send_email_collector_email(email_collected_data)

    return email_collected_data, True

