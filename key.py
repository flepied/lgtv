#!/usr/bin/env python3

import os
import sys

from pywebostv.controls import InputControl

from lib import init

client = init()

inp = InputControl(client)
inp.connect_input()

method = getattr(inp, os.path.basename(sys.argv[0]))
method(block=True)

# key.py ends here
