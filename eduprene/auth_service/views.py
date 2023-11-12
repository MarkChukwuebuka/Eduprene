from rest_framework.decorators import api_view
from .controllers import register_handler


# Create your views here.
@api_view(['POST'])
def register(request):
    return register_handler(request)
