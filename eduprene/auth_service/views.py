from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import RegisterSerializer
from ..response import bad_request_with_data


# Create your views here.
@api_view(['POST'])
def register(request):
    register_serializer = RegisterSerializer(data=request.data)

    if register_serializer.is_valid():
        pass

    return bad_request_with_data(data=register_serializer.errors)
