# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# Name:        etgtools/map_generator.py
# Author:      Robin Dunn
#
# Created:     20-May-2016
# Copyright:   (c) 2016-2020 by Total Control Software
# License:     wxWindows License
# ---------------------------------------------------------------------------

"""
This module provides a class that manages a persistent mapping, currently just
for mapping module item names to the name of their module, so other phases of
the code generation can find things that may not have been seen yet.  This
class can easily be adapted to other purposes however, if the need arises.
"""

# Standard library imports
import os.path as op
import json


# Phoenix imports
from .generators import textfile_open
from sphinxtools.constants import SPHINXROOT

# ---------------------------------------------------------------------------

class ItemModuleMap(object):
    """
    A persistent (across builds) mapping.  It manages the data in a
    dictionary, and also has a few methods to make the object quack a little
    like a real dictionary.
    """

    # This is the Borg pattern, so all instances of this class actually share
    # the same data attributes
    __shared_state = dict(_haveReadData=False,
                          _items=dict())

    def __init__(self):
        self.__dict__ = self.__shared_state # Borg part 2
        self.fileName = op.join(SPHINXROOT, 'itemToModuleMap.json')


    @property
    def items(self):
        # lazy load the items on first use
        if not self._haveReadData:
            self.read()
        return self._items


    # Methods for reading/writing the data from/to persistent storage.
    def read(self):
        if op.isfile(self.fileName):
            with textfile_open(self.fileName, 'rt') as fid:
                items = json.load(fid)
                # TODO: catch JSON exception...
                if items is None:
                    items = dict()
        else:
            items = dict()

        self._items.clear()
        self._items.update(items)
        self._haveReadData = True


    def flush(self):
        if not self._haveReadData and not self._items:
            return
        with textfile_open(self.fileName, 'wt') as fid:
            # Dump the data to a file in json, using a format that minimizes
            # excess whitespace.
            json.dump(self._items, fid, sort_keys=True,
                      indent=0, separators=(',', ':'))


    def reset(self):
        self._haveReadData = False,
        self._items.clear()


    def get_module(self, name):
        return self.items.get(name)

    def get_fullname(self, name):
        module = self.items.get(name)
        if not module:
            return name
        return module + name



    # Methods for a dictionary Facade, for convenience
    def get(self, key, default=None):
        return self.items.get(key, default)

    def clear(self):
        self.items.clear()

    def __len__(self):
        return len(self.items)

    def __getitem__(self, key):
        if key in self.items:
            return self.items[key]
        raise KeyError(key)

    def __setitem__(self, key, item):
        self.items[key] = item

    def __delitem__(self, key):
        del self.items[key]

    def __iter__(self):
        return iter(self.items)

    def __contains__(self, key):
        return key in self.items




# ---------------------------------------------------------------------------
