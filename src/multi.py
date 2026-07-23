import importlib
import sys

root = importlib.import_module(__package__)

_@NAME@ = importlib.import_module(f'.@NAME@_{root.__plat__}', __package__)

if hasattr(_@NAME@, '__all__'):
    __all__ = _@NAME@.__all__
else:
    __all__ = [name for name in dir(_@NAME@) if name != "__name__"]

globals().update({name: getattr(_@NAME@, name) for name in __all__})

del root
del _@NAME@
