import sys
granted_modules = ["math", "random"]

def restricted_open(filename: str, mode: str = "w", **kw):
    raise PermissionError("Cannot interact with files")
tt = __import__
def restricted_import(name, globals=None, locals=None, fromlist=(), level=0):
    if globals["__name__"] != "__main__" or name in granted_modules:
        return tt(name, globals, locals, fromlist, level)
    else:
        raise ImportError("Importing this module is not allowed")

sys.modules["builtins"].__import__ = restricted_import
import math; print(math.sin(3))
sys.modules["builtins"].__import__ = tt
from runnable import *
import os
print(os.environ)
assert add_smth(2, 3) == 5
assert add_smth(4, 5) == 9