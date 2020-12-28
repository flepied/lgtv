#!/usr/bin/env python3

from pywebostv.controls import ApplicationControl

from lib import init

client = init()

app = ApplicationControl(client)
apps = app.list_apps()
netflix = [x for x in apps if "netflix" in x["title"].lower()][0]
launch_info = app.launch(netflix)
print(launch_info)

# netflix.py ends here
