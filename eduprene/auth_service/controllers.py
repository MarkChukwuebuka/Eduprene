import logging
from auth_service.serializers import RegisterSerializer, RegisterSerializerResponse, ResendRegisterOtpSerializer, VerifyRegistrationOtpSerializer, TokenResponseSerializer
from auth_service.services import add_registration_log, resend_registration_otp, verify_registration_otp
from response import bad_request_with_message, server_error, with_data, bad_request_with_data, with_message_and_data
from constants.other_constants import OTP_SENT_TO_EMAIL, REGISTERED_SUCCESSFULLY


def register_handler(request):
    try:
        register_serializer = RegisterSerializer(data=request.data)

        if register_serializer.is_valid():

            data = register_serializer.data

            new_user_log, status = add_registration_log(data)
            log_serializer = RegisterSerializerResponse(new_user_log)

            if not status:
                # Returns bad request if user exists and has been verified
                return bad_request_with_message(message="User already exists.")

            # Returns the log if it is newly created
            return with_message_and_data(message=OTP_SENT_TO_EMAIL, data=log_serializer.data, code=201)

        return bad_request_with_data(data=register_serializer.errors)

    except Exception as e:
        logging.error(msg=e)
        return server_error()

def resend_register_otp_handler(request):
    try:
        resend_register_otp_serializer = ResendRegisterOtpSerializer(data=request.data)

        if resend_register_otp_serializer.is_valid():
            data = resend_register_otp_serializer.data
            message, status = resend_registration_otp(data)

            if not status:
                return bad_request_with_message(message)

            return with_message_and_data(message=OTP_SENT_TO_EMAIL, data=resend_register_otp_serializer.data)

        return bad_request_with_data(data=resend_register_otp_serializer.errors)
        
    except Exception as e:
        logging.error(msg=e)
        return server_error()

def verify_registration_otp_handler(request):
    try:
        verify_registration_otp_serializer = VerifyRegistrationOtpSerializer(data=request.data)
        if verify_registration_otp_serializer.is_valid():
            data = verify_registration_otp_serializer.data
            message, status = verify_registration_otp(data)

            if not status:
                return bad_request_with_message(message)
            
            verify_token_serializer = TokenResponseSerializer(data=message)
            
            if verify_token_serializer.is_valid():
                return with_message_and_data(message=REGISTERED_SUCCESSFULLY, data=verify_token_serializer.data)
            else:
                logging.error(verify_token_serializer.errors)
                return server_error()
        
        return bad_request_with_data(data=verify_registration_otp_serializer.errors)

    except Exception as e:
        logging.error(msg=e)
        return server_error()