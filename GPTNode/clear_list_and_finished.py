import django, os
import time
from datetime import timedelta
from dotenv import load_dotenv, find_dotenv
from web3 import Web3
import json

if not os.environ.get("DATABASE_URL"):
    load_dotenv(find_dotenv())

# django setup
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "GPTNode.settings")
django.setup()
from django.db.models.functions import Now
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

def clear_lists():
    unsent_market_tx = llm_market.functions.clearListAndReedemFunds().build_transaction({
        "from": public_key,
        "nonce": web3.eth.get_transaction_count(public_key)
    })
    signed_tx = web3.eth.account.sign_transaction(unsent_market_tx, private_key=private_key)

    tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)

    web3.eth.wait_for_transaction_receipt(tx_hash)
    tx_receipt = web3.eth.get_transaction_receipt(tx_hash)

def pause():
    unsent_market_tx = llm_market.functions.pause().build_transaction({
        "from": public_key,
        "nonce": web3.eth.get_transaction_count(public_key)
    })
    signed_tx = web3.eth.account.sign_transaction(unsent_market_tx, private_key=private_key)

    tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)

    web3.eth.wait_for_transaction_receipt(tx_hash)
    tx_receipt = web3.eth.get_transaction_receipt(tx_hash)

def unpause():
    unsent_market_tx = llm_market.functions.unpause().build_transaction({
        "from": public_key,
        "nonce": web3.eth.get_transaction_count(public_key)
    })
    signed_tx = web3.eth.account.sign_transaction(unsent_market_tx, private_key=private_key)

    tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)

    web3.eth.wait_for_transaction_receipt(tx_hash)
    tx_receipt = web3.eth.get_transaction_receipt(tx_hash)


# delete all requests that are unpaid and more than 3 minutes old
while True:
    try:
        pause()
        time.sleep(5)
        Request.objects.filter(finished=True).delete()
        clear_lists()
        unpause()
    except Exception as e:
        print(e)
    time.sleep(60*60)


