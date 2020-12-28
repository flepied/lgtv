#!/usr/bin/env python3

import os
import sys
import select
import termios
import tty

from pywebostv.controls import InputControl

from lib import init


def getKey():
    tty.setraw(sys.stdin.fileno())
    rfds, wfds, efds = select.select([sys.stdin], [], [])

    if len(rfds) > 0 or len(wfds) > 0 or len(efds) > 0:
        key = sys.stdin.read(1)
        # keyboard arrows are a 'triplet' (3 codes), so if the keycode
        # begin with x1b, we asume the rest are the 2 remaining keycodes
        if key == "\x1b":
            key += sys.stdin.read(2)
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
        return key
    else:
        return None


if __name__ == "__main__":
    client = init()

    inp = InputControl(client)
    inp.connect_input()
    try:
        while True:
            settings = termios.tcgetattr(sys.stdin)
            key = getKey()
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
            if key == 'q' or key == 'Q':
                break
            if key == "\x1b[A":
                print("up")
                inp.up(block=True)
            elif key == "\x1b[B":
                print("down")
                inp.down(block=True)
            elif key == "\x1b[C":
                print("right")
                inp.right(block=True)
            elif key == "\x1b[D":
                print("left")
                inp.left(block=True)
            elif key == "\x1b[H":
                print("home")
                inp.home(block=True)
            elif len(key) == 1:
                if ord(key) == 127:
                    print("backspace")
                    inp.back(block=True)
                elif ord(key) == 13:
                    print("return")
                    inp.ok(block=True)
            else:
                print("Unkown key", [ord(x) for x in key], key[-1])
    except Exception as e:
        print(e)

    finally:
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
