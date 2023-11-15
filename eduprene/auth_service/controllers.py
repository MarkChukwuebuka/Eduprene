import logging
from auth_service.serializers import RegisterSerializer, RegisterSerializerResponse
from auth_service.services import add_registration_log
from response import bad_request_with_message, server_error, with_data, bad_request_with_data, with_message_and_data
from constants.other_constants import OTP_SENT_TO_EMAIL


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
