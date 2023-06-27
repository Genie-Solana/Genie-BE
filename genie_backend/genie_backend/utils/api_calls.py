import os
import requests
import json
from solders.keypair import Keypair

SERVERLESS_ENDPOINT = os.environ.get("SERVERLESS_ENDPOINT")

def create_social_account_call():
    keypair = Keypair()
    endpoint = SERVERLESS_ENDPOINT + 'profile'
    sec_key = str(Keypair.from_bytes(bytes(keypair)).to_bytes_array()) 
    response = requests.post(endpoint, json={"sec_key": sec_key})
    data = json.loads(response.text)
    return data, sec_key

