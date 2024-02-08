import django, os
import time
from openai import OpenAI
import threading
from dotenv import load_dotenv, find_dotenv

# load the env file
if not os.environ.get("DATABASE_URL"):
    load_dotenv(find_dotenv())

# django setup
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "GPTNode.settings")
django.setup()
from AIStuff.models import AIResponse, Request, ChatPart

# openai setup
_api_key = os.environ['OPENAI_KEY']
client = OpenAI(api_key=_api_key)


# generate AI results
def generate_results(req):

    # avoid double gen
    req.generating = True
    req.save()

    chat = ChatPart.objects.filter(request=req).order_by("chat_id")
    messages = []

    # use openai to check for possible policy breach
    chat_to_check = "\n".join([c.content for c in chat])

    # check for possible input size, max 15x output tokens (in chars)
    too_big = False
    #print(len(chat_to_check))
    if len(chat_to_check) > req.tokens * 15:
        too_big = True

    response = client.moderations.create(
        input=chat_to_check
    )
    flagged = response.results[0].flagged

    # actual generation
    ai_resp = AIResponse.objects.get(result_code=req.result_code)
    if not flagged and not too_big:
        for c in chat:
            messages.append({"role": c.role, "content": c.content})
        completion = client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=messages,
            max_tokens=req.tokens
        )
        ai_resp.response = completion.choices[0].message.content
        #print(completion)
    else:
        ai_resp.response = "Content got flagged as violating OpenAis policy or has too many input characters (max 15x output tokens)!"

    # delete requests and messages
    ai_resp.save()
    chat.delete()
    #req.delete()
    req.finished = True
    req.save()


# main loop
while True:
    try:
        for req in Request.objects.filter(paid_for=True, generating=False, finished=False):
            t = threading.Thread(target=generate_results, args=[req], daemon=True)
            t.start()
    except Exception as e:
        print(e)
    time.sleep(5)


