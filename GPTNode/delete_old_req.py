import django, os
import time
from datetime import timedelta

# django setup
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "GPTNode.settings")
django.setup()
from django.db.models.functions import Now
from AIStuff.models import Request


# delete all requests that are unpaid and more than 3 minutes old
while True:
    try:
        Request.objects.filter(paid_for=False, req_date__lt=Now()-timedelta(minutes=3)).delete()
        Request.objects.filter(paid_for=True, req_date__lt=Now() - timedelta(hours=1)).delete()
    except Exception as e:
        print(e)
    time.sleep(10)


