"""
test code for FC_Objects.py

Note: hardly anything here yet. If we add more, we should probably move this
to the main unittest suite location

On the Mac with conda, this needs to be run with pythonw:

pythonw -m pytest

"""

import pytest

import wx

from .FCObjects import _cycleidxs

app = wx.App()


def test__cycleidxs_start():
    """
    on first call, it should provide ...
    """
    CG = _cycleidxs(indexcount=3, maxvalue=256, step=1)
    assert next(CG) == (0, 0, 0)



def test__cycleidxs_multiple():
    """
    make sure it gets the first few anyway ...
    """
    CG = _cycleidxs(indexcount=3, maxvalue=256, step=1)

    print("first three")
    for i in range(3):
        color = next(CG)
        print(color)
        assert color == (0, 0, i)
    for i in range(253):
        next(CG)
    print("after 255")
    for i in range(3):
        color = next(CG)
        print(color)
        assert color == (0, 1, i)

    assert False
