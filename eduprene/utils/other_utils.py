import secrets
from datetime import datetime as dt

def generate_code(length=5):
    '''Generates *2 string length of the length passed in'''
    if type(length) != int:
        length = 5
    
    return secrets.token_hex(length)

def generate_referral_code(model):
    referral_code = generate_code(5)

    check_code_exists = model.objects.filter(referral_code=referral_code).first()

    if check_code_exists:
        generate_referral_code(model)

    return referral_code


def generate_unique_id():
    current_time = dt.now().time()

    # Convert the time to a string
    time_string = str(current_time)

    # Extract digits and concatenate them
    concatenated_digits = ''.join(filter(str.isdigit, time_string))
    token = (secrets.token_hex(3) + concatenated_digits).upper()

    return token