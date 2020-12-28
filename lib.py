
'''
'''

import json
import os
import re
import sys
import time

from pywebostv.connection import WebOSClient
from pywebostv.controls import ApplicationControl
from wakeonlan import send_magic_packet

STORE = "store.json"


def get_macaddr(ip):
    with open("/proc/net/arp") as arp:
        for line in arp.readlines():
            line = line.strip()
            parts = re.split(r"\s+", line)
            if len(parts) == 6 and parts[0] == ip:
                return parts[3]
    return None


def init(wakeup=True):
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
        if wakeup and "macaddr" in store:
            print("Starting TV")
            send_magic_packet(store["macaddr"])
            time.sleep(10)
            return init(False)
        print("TV is off", file=sys.stderr)
        sys.exit(1)

    for status in client.register(store):
        if status == WebOSClient.PROMPTED:
            print("Please accept the connect on the TV!")
        elif status == WebOSClient.REGISTERED:
            pass

    store["ipaddr"] = client.host
    macaddr = get_macaddr(store["ipaddr"])

    if macaddr:
        store["macaddr"] = macaddr

    with open(STORE, "w") as out:
        json.dump(store, out)

    return client


def launch_app(name, client):
    ctl = ApplicationControl(client)
    apps = ctl.list_apps()
    app = [x for x in apps if name in x["title"].lower()][0]
    launch_info = ctl.launch(app)
    return launch_info

# lib.py ends here
