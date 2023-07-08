import sys
granted_modules = ["math", "random", "re"]

def restricted_open(filename: str, mode: str = "w", **kw):
    raise PermissionError("Cannot interact with files")
tt = __import__
def restricted_import(name, globals=None, locals=None, fromlist=(), level=0):
    if globals["__name__"] != "__main__" or name in granted_modules:
        return tt(name, globals, locals, fromlist, level)
    else:
        raise ImportError("Importing this module is not allowed")

sys.modules["builtins"].__import__ = restricted_import
data = int(input("enter a number:"))
print(data)
print(data + 13)