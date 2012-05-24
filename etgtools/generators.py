#---------------------------------------------------------------------------
# Name:        etgtools/generators.py
# Author:      Robin Dunn
#
# Created:     3-Nov-2010
# Copyright:   (c) 2011 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

"""
Just some base classes and stubs for the various generators
"""

import sys

class WrapperGeneratorBase(object):
    def __init__(self):
        pass    
    def generate(self, module, destFile=None):
        raise NotImplementedError
        
    
class DocsGeneratorBase(object):
    def __init__(self):
        pass        
    def generate(self, module):
        raise NotImplementedError
    
    
class StubbedDocsGenerator(DocsGeneratorBase):
    def generate(self, module):
        pass


class SphinxGenerator(DocsGeneratorBase):
    def generate(self, module):
        pass

#---------------------------------------------------------------------------
# helpers

def nci(text, numSpaces=0, stripLeading=True):
    """
    Normalize Code Indents
    
    First use the count of leading spaces on the first line and remove that
    many spaces from the front of all lines, and then indent each line by
    adding numSpaces spaces. This is used so we can convert the arbitrary
    indents that might be used by the tweaker code into what is expected for
    the context we are generating for.
    """
    def _getLeadingSpaceCount(line):
        count = 0
        for c in line:
            assert c != '\t', "Use spaces for indent, not tabs"
            if c != ' ':
                break
            count += 1
        return count
    
    def _allSpaces(text):
        for c in text:
            if c != ' ':
                return False
        return True

    
    lines = text.rstrip().split('\n')
    if stripLeading:
        numStrip = _getLeadingSpaceCount(lines[0])
    else:
        numStrip = 0
    
    for idx, line in enumerate(lines):
        assert _allSpaces(line[:numStrip]), "Indentation inconsistent with first line"
        lines[idx] = ' '*numSpaces + line[numStrip:]

    newText = '\n'.join(lines) + '\n'
    return newText

#---------------------------------------------------------------------------

if sys.version_info < (3,):
    # For Python 2.x we'll convert any unicode text values to strings before
    # adding them to the buffer
    from StringIO import StringIO
    class Utf8EncodingStream(StringIO):
        def write(self, text):
            if isinstance(text, unicode):
                text = text.encode('utf-8')
            return StringIO.write(self, text)

else:
    # For Python 3.x we'll keep it all as str (unicode) objects and let the
    # conversion to bytes happen when the text is written to the actual
    # file.
    from io import StringIO
    class Utf8EncodingStream(StringIO):
        pass



def textfile_open(filename, mode='rt'):
    """
    Simple wrapper around open() that will open normally on Python 2.x and on
    Python 2.3 will add the encoding parameter. The mode parameter must
    include the 't' to put the stream into text mode.
    """
    assert 't' in mode
    if sys.version_info < (3,):
        return open(filename, mode)
    else:
        return open(filename, mode, encoding='utf-8')
    
    
#---------------------------------------------------------------------------
