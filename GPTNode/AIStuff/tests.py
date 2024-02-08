from django.test import TestCase
from rest_framework.test import APIRequestFactory
from rest_framework import status
from .views import create_request_view, get_response_view
import random

# Create your tests here.
class RequestTesting(TestCase):
    def setUp(self):
        self.request_factory = APIRequestFactory()

    def test_create_request(self):
        obj = {
            "unique_code": 1234567891,
            "messages": [
                {"role": "system", "content": "Blablablas"},
                {"role": "user", "content": "Sheesh!1"}
            ]
        }
        request = self.request_factory.post('ai/create/', obj, format='json')
        view = create_request_view
        response = view(request)
        #print(response.data)
        self.assertTrue(response.status_code == status.HTTP_201_CREATED)
        self.assertTrue(len(response.data.get("result")) == 40)

    def test_get_response(self):

        obj = {
            "unique_code": 1234567891,
            "messages": [
                {"role": "system", "content": "Blablablas"},
                {"role": "user", "content": "Sheesh!1"}
            ]
        }
        request = self.request_factory.post('ai/create/', obj, format='json')
        view = create_request_view
        response = view(request)
        result_code = response.data.get("result")
        #print(result_code)

        obj = {
            "result_code": result_code
        }
        request = self.request_factory.get('ai/get/', obj, format='json')
        view = get_response_view
        response = view(request)
        #print(response.data)
        self.assertTrue(response.status_code == status.HTTP_200_OK)
        self.assertTrue(response.data.get("content") == "Still generating!")
