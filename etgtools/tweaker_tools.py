#---------------------------------------------------------------------------
# Name:        etgtools/tweaker_tools.py
# Author:      Robin Dunn
#
# Created:     3-Nov-2010
# Copyright:   (c) 2010 by Total Control Software
# Licence:     wxWindows license
#---------------------------------------------------------------------------

"""
Some helpers and utility functions that can assist with the tweaker
stage of the ETG scripts.
"""

import extractors



def removeWxPrefixes(node):
    """
    Rename items with a 'wx' prefix to not have the prefix.
    """
    for item in node.allItems():
        if not item.pyName \
           and item.name.startswith('wx') \
           and not item.name.startswith('wxEVT_') \
           and not isinstance(item, (extractors.TypedefDef,
                                     extractors.MethodDef )):  # TODO: Any others?
                item.pyName = item.name[2:]
            


def ignoreAssignmentOperators(node):
    """
    Set the ignored flag for all class methods that are assignment operators
    """
    for item in node.allItems():
        if isinstance(item, extractors.MethodDef) and item.name == 'operator=':
            item.ignore()

            
def ignoreAllOperators(node):
    """
    Set the ignored flag for all class methods that are any kind of operator
    """
    for item in node.allItems():
        if isinstance(item, extractors.MethodDef) and item.name.startswith('operator'):
            item.ignore()

            
def createPyArgsStrings(node):
    """
    TODO: Create a pythonized version of the argsString in function and method
    items that can be used as part of the docstring.
    """
    pass
