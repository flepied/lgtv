#!/usr/bin/env python3

from pywebostv.controls import SystemControl

from lib import init

client = init()

system = SystemControl(client)
system.notify("Powering down", block=True)
system.power_off()

# off.py ends here
