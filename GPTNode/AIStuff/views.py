from django.shortcuts import render
from .serializers import RequestSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions
from .models import Request


# Create your views here.
@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def create_request_view(request, format=None):
    seri = RequestSerializer()
    return seri.create(request.data)

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def get_response_view(request, result_code, format=None):
    seri = RequestSerializer()
    #print(request.GET.get(res))
    return seri.get_response(result_code)
