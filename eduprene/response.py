from rest_framework.response import Response

from constants.other_constants import ERROR_MESSAGES


def with_data(data, code=200):
    return Response(data, code)


def with_message(message, code=200):
    data = {
        "message": message
    }
    return Response(data, code)


def with_message_and_data(message, data, code=200):
    data = {
        "message": message,
        "data": data
    }
    return Response(data, code)


def bad_request_with_message(message, code=400):
    return with_message(message, code)


def bad_request_with_data(data, code=400):
    return with_data(data, code)


def server_error(message=ERROR_MESSAGES['INTERNAL_SERVER_ERROR'], code=500):
    return with_message(message, code)
