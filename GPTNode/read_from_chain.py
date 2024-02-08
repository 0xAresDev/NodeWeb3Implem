import django, os
import time
from dotenv import load_dotenv, find_dotenv
from web3 import Web3
import json

# env import
if not os.environ.get("DATABASE_URL"):
    load_dotenv(find_dotenv())

# django stuff
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "GPTNode.settings")
django.setup()
from AIStuff.models import Request


connected = False
while not connected:
    rpc_shido = os.environ['RPC']
    web3 = Web3(Web3.HTTPProvider(rpc_shido))
    print(web3.is_connected())
    connected = web3.is_connected()

_llmmarket = os.environ['LLMMARKET']
f = open('LLMMarket.json')
data = json.load(f)
f.close()
abi = data["abi"]
llm_market = web3.eth.contract(address=_llmmarket, abi=abi)

public_key = os.environ['PUBLIC_KEY']
private_key = os.environ['PRIVATE_KEY']


_price = int(os.environ['PRICE'])

# get all active, paid, unfilled requests
def get_all_paid_requests():
    return llm_market.functions.getActiveRequests(public_key).call()

# get current wallet balance of account
def get_balance(public_key):
    return web3.eth.get_balance(public_key)



while True:
    try:
        req = get_all_paid_requests()

        for r in req:
            #print(r)
            if not isinstance(r[0], int) or len(Request.objects.filter(unique_code=r[0])) != 1:
                continue
            #print(2)
            r_ = Request.objects.get(unique_code=r[0])
            if not r_.paid_for:
                r_.paid_for = True
                r_.tokens = int(r[1]) / _price
                r_.save()

        time.sleep(2.5)
    except Exception as e:
        print(e)
