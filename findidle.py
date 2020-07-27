from pynput.mouse import Button, Controller
import time
import datetime

def idletime(initialpos, i, idle, t):
    while True:
        finalpos = format(mouse.position)
        if initialpos != finalpos: #if mouse moved
            s = time.time()
            if i==1:
                idle = s-e
                return idle
            initialpos = finalpos
            i = 1
            e = time.time() #end timer
        if str(datetime.datetime.now().time()).startswith('23:59:50'):
            return idle
