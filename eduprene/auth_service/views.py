from rest_framework.decorators import api_view
from .controllers import register_handler, resend_register_otp_handler


@api_view(['POST'])
def register(request):
    return register_handler(request)


@api_view(['POST'])
def resend_register_otp(request):
    return resend_register_otp_handler(request)