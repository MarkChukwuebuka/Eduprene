from rest_framework.decorators import api_view
from .controllers import email_collector_handler


@api_view(['POST'])
def email(request):
    return email_collector_handler(request)