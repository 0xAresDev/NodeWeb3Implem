from django.db import models

# Create your models here.


class Request(models.Model):
    req_date = models.DateTimeField(auto_now=True)
    unique_code = models.BigIntegerField()
    result_code = models.CharField(max_length=40)
    paid_for = models.BooleanField(default=False)
    generating = models.BooleanField(default=False)
    finished = models.BooleanField(default=False)
    tokens = models.IntegerField(default=0)

class ChatPart(models.Model):
    role = models.CharField(max_length=10)
    content = models.TextField()
    chat_id = models.IntegerField()
    request = models.ForeignKey(Request, on_delete=models.CASCADE)


class AIResponse(models.Model):
    result_code = models.CharField(max_length=40)
    response = models.TextField()
