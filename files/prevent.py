import sys
from typing import Any

def open(filename: str, mode: str):
    raise BaseException("Cannot interact with files")

def ri(name, globals=None, locals=None, fromlist=(), level=0):
    raise ImportError("Importing this module is not allowed")

ri.__vl = __import__

sys.modules["builtins"].__import__ = ri

from math import sin