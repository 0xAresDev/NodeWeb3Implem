from django.contrib import admin
from .models import Request, ChatPart, AIResponse
# Register your models here.

admin.site.register(Request)
admin.site.register(ChatPart)
admin.site.register(AIResponse)
