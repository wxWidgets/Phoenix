#---------------------------------------------------------------------------
# Name:        etgtools/generators.py
# Author:      Robin Dunn
#
# Created:     3-Nov-2010
# Copyright:   (c) 2010-2020 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

"""
Just some base classes and stubs for the various generators
"""

import sys

#---------------------------------------------------------------------------

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


def wrapText(text, dontWrap: str = ''):
    import textwrap
    lines = []
    tw = textwrap.TextWrapper(width=70, break_long_words=False)
    for line in text.split('\n'):
        if dontWrap and line.lstrip().startswith(dontWrap):
            lines.append(line)
        else:
            lines.append(tw.fill(line))
    return '\n'.join(lines)


#---------------------------------------------------------------------------

# io.StringIO reads/writes unicode objects for both Python 2.7 and 3.x. For
# 2.7 we'll convert any string values to unicode objects before storing them
# in the StringIO
import io
class Utf8EncodingStream(io.StringIO):
    if sys.version_info < (3,):
        def write(self, text):
            if isinstance(text, str):
                text = text.decode('utf-8')
            return io.StringIO.write(self, text)




def textfile_open(filename, mode='rt'):
    """
    Simple wrapper around open() that will use codecs.open on Python2 and
    on Python3 will add the encoding parameter to the normal open(). The
    mode parameter must include the 't' to put the stream into text mode.
    """
    assert 't' in mode
    if sys.version_info < (3,):
        import codecs
        mode = mode.replace('t', '')
        return codecs.open(filename, mode, encoding='utf-8')
    else:
        return open(filename, mode, encoding='utf-8')


#---------------------------------------------------------------------------

