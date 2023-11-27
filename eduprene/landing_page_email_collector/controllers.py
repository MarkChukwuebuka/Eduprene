import logging
from response import bad_request_with_message, server_error, bad_request_with_data, with_message_and_data
from .serializers import EmailCollectorSerializer
from .services import add_email_collected
from constants.other_constants import CONFIRMATION_EMAIL_SENT


def email_collector_handler(request):
    try:
        print('request')
        email_collector_serializer = EmailCollectorSerializer(data=request.data)

        if email_collector_serializer.is_valid():
            data = email_collector_serializer.data

            new_email_collected, status = add_email_collected(data)

            collected_email_serializer = EmailCollectorSerializer(new_email_collected)

            if not status:
                # Returns bad request if something happens
                return bad_request_with_message(message="Something went wrong.")

            # Returns the newly created email data
            return with_message_and_data(message=CONFIRMATION_EMAIL_SENT, data=collected_email_serializer.data, code=201)

        return bad_request_with_data(data=email_collector_serializer.errors)

    except Exception as e:
        logging.error(msg=e)
        return server_error()