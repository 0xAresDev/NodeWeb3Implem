from rest_framework import serializers
from .models import Request, ChatPart, AIResponse
import random, string
from rest_framework.response import Response
from rest_framework import status




class RequestSerializer():

    def validate_create_data(self, data):
        if not data.get("unique_code") or not data.get("messages"):
            return False
        if not isinstance(data.get("unique_code"), int):
            return False
        messages = data.get("messages")
        for message in messages:
            if not message.get("role") or not message.get("content"):
                return False
            if message.get("role") not in ["user", "assistant", "system"]:
                return False
            if len(message.get("content")) == 0:
                return False
        if len(Request.objects.filter(unique_code=data.get("unique_code"))) > 0:
            return False
        return True

    def create_random_code(self):
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=40))

    def create(self, data):
        if not self.validate_create_data(data):
            return Response({"Error": "Invalid formatting or duplicate unique_code!"}, status=status.HTTP_400_BAD_REQUEST)

        result_code = self.create_random_code()
        req = Request.objects.create(unique_code=data.get("unique_code"), result_code=result_code)

        messages = data.get("messages")

        for i, message in enumerate(messages):
            part = ChatPart.objects.create(role=message.get("role"), content=message.get("content"), chat_id=i, request=req)

        res = AIResponse.objects.create(result_code=result_code, response="Still generating!")

        return Response({"result": res.result_code}, status=status.HTTP_201_CREATED)


    def validate_response(self, result_code):
        if len(result_code) != 40:
            return False
        return True

    def get_response(self, result_code):
        if not self.validate_response(result_code):
            return Response({"Error": "Invalid Code"}, status=status.HTTP_400_BAD_REQUEST)
        code = result_code #data.get("result_code")
        res = AIResponse.objects.filter(result_code=code)
        if len(res) == 0:
            return Response({"Error": "No response found for result code"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            res = res.first()

        return Response({"content": res.response}, status=status.HTTP_200_OK)
