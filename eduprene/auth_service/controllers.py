from utils.otp_utils import generate_otp
from datetime import datetime as dt

def register_handler(data):
    # Generate OTP and add to data
    data['otp'] = generate_otp()
    data['otp_requested_at'] = dt.utcnow()