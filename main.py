import random
import threading
import time

import requests
import hashlib
from threading import Thread


url = "https://darkbluestealth.pythonanywhere.com/"
hash_value = "None"
username = ""
password = ""

session = requests.Session()

def get_new_hash(given_hash):
    r = session.post(url, json={"Hash": given_hash, "Method": "CheckHash"})
    global hash_value
    hash_value = given_hash if r.text == "405" else r.text

def get_balance():
    r = session.post(url, json={"Username": username, "Password": password, "Method": "CheckBalance"})
    return r.text
def check_if_correct(given_hash, nonce_val, result, username_val):
    r = session.post(url, json={"Hash": given_hash, "Nonce": str(nonce_val), "Username": username_val, "Outcome": result, "Method": "FoundHash"})
    if r.text == "100":
        print(f"[{time.time()}] - Solved. New balance: ", get_balance())
        return "success"
    elif r.text == "402":
        pass
    else:
        print(r.text)
        #print("Wrong hash", 402)

def miner():
    print("Starting miner", threading.get_ident())
    while True:
        nonce_val = random.randint(0, 99999999)
        result = hashlib.sha256((hash_value + str(nonce_val)).encode('utf-8')).hexdigest()
        if result[:6] != "000000":
            continue
        check_if_correct(hash_value, nonce_val, result, username)

get_new_hash(hash_value)
def ensurer():
    print("Started hash checker")
    while True:
        print(f"[{time.time()}] - Checking for new hash")
        old = hash_value
        get_new_hash(hash_value)
        if hash_value != old:
            print(f"[{time.time()}] - Now hash is:", hash_value)
        time.sleep(5)

Thread(target=ensurer).start()

for _ in range(50):
    Thread(target=miner).start()
