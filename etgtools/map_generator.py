# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# Name:        etgtools/map_generator.py
# Author:      Robin Dunn
#
# Created:     20-May-2016
# Copyright:   (c) 2016 by Total Control Software
# License:     wxWindows License
# ---------------------------------------------------------------------------

"""
This generator simply maintains a persistent map of top-level item names and
the module each is in.  This will be used in the Sphinx generator and will
perhaps help simplify other generator tasks as well.
"""


# Phoenix-specific imports
from . import extractors
from . import generators
from .tweaker_tools import removeWxPrefix
from .item_module_map import ItemModuleMap
from sphinxtools.constants import MODULENAME_REPLACE

# ---------------------------------------------------------------------------

class ItemMapGenerator(generators.DocsGeneratorBase):
    def __init__(self):
        super(ItemMapGenerator, self).__init__()

    def generate(self, module):
        assert isinstance(module, extractors.ModuleDef)
        realModuleName = MODULENAME_REPLACE[module.module]

        imm = ItemModuleMap()
        for item in module.items:
            name = self._getName(item)
            if not name or name.startswith('@'):
                continue

            if isinstance(item, extractors.ClassDef):
                for inner in item.innerclasses:
                    self.generateInnerClass(inner, imm,
                                            '{}{}.'.format(realModuleName, name))
            # TODO: Maybe nested enums too?


            # save the module that the name belongs to
            imm[name] = realModuleName

            # We don't need it currently, but this is how to also store the
            # reverse relationships in the same mapping.
            #mod_list = imm.get(realModuleName)
            #if mod_list is None:
            #    mod_list = imm[realModuleName] = list()
            #if name not in mod_list:
            #    mod_list.append(name)
            #    mod_list.sort()

        imm.flush()


    def generateInnerClass(self, klass, imm, scopeName):
        # Recursively handle any inner classes that may be defined, adding the
        # enclosing scope as we go to the module name
        name = self._getName(klass)
        imm[name] = scopeName
        for inner in klass.innerclasses:
            self.generateInnerClass(inner, imm, '{}{}.'.format(scopeName, name))


    def _getName(self, item):
        return item.pyName if item.pyName else removeWxPrefix(item.name)

# ---------------------------------------------------------------------------


