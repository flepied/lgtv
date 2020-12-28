
'''
'''

import json
import os
import sys

from pywebostv.connection import WebOSClient

STORE = "store.json"


def init():
    if not os.path.exists(STORE):
        store = {}
    else:
        with open(STORE) as fh:
            store = json.load(fh)

    if "ipaddr" in store:
        client = WebOSClient(store["ipaddr"])
    else:
        clients = WebOSClient.discover()
        client = clients[0]

    try:
        client.connect()
    except OSError:
        print("TV is off", file=sys.stderr)
        sys.exit(1)

    for status in client.register(store):
        if status == WebOSClient.PROMPTED:
            print("Please accept the connect on the TV!")
        elif status == WebOSClient.REGISTERED:
            pass

    store["ipaddr"] = client.host
    with open(STORE, "w") as out:
        json.dump(store, out)

    return client


# essai.py ends here
