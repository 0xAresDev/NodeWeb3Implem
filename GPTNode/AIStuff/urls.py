from django.urls import path
from .views import create_request_view, get_response_view


app_name = "AIStuff"

urlpatterns = [
    path('create/', create_request_view, name='create-request'),
    path('get/<str:result_code>', get_response_view, name='get-response'),
]
