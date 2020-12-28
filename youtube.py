#!/usr/bin/env python3

from pywebostv.controls import ApplicationControl

from lib import init

client = init()

app = ApplicationControl(client)
apps = app.list_apps()
youtube = [x for x in apps if "youtube" in x["title"].lower()][0]
launch_info = app.launch(youtube)
print(launch_info)

# youtube.py ends here
