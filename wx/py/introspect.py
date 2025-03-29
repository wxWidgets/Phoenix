"""Provides a variety of introspective-type support functions for
things like call tips and command auto completion."""

__author__ = "Patrick K. O'Brien <pobrien@orbtech.com>"

import re
import sys
import inspect
import tokenize
import types
import wx
from io import BytesIO

def getAutoCompleteList(command='', locals=None, includeMagic=1,
                        includeSingle=1, includeDouble=1):
    """Return list of auto-completion options for command.

    The list of options will be based on the locals namespace."""
    attributes = []
    # Get the proper chunk of code from the command.
    root = getRoot(command, terminator='.')
    try:
        if locals is not None:
            obj = eval(root, locals)
        else:
            obj = eval(root)
    except:
        pass
    else:
        attributes = getAttributeNames(obj, includeMagic,
                                       includeSingle, includeDouble)
    return attributes

def getAttributeNames(obj, includeMagic=1, includeSingle=1,
                      includeDouble=1):
    """Return list of unique attributes, including inherited, for obj."""
    attributes = []
    dict = {}
    if not hasattrAlwaysReturnsTrue(obj):
        # Add some attributes that don't always get picked up.
        special_attrs = ['__bases__', '__class__', '__dict__', '__name__',
                         '__closure__', '__code__', '__defaults__',
                         '__kwdefaults__', '__globals__', '__qualname__',
                         '__builtins__',  # Added to method attributes in 3.10
                         '__get__',       # Not found in `dir(method)` in 3.11
                         ]
        attributes += [attr for attr in special_attrs \
                       if hasattr(obj, attr)]
    if includeMagic:
        try: attributes += obj._getAttributeNames()
        except: pass
        # Special code to allow traits to be caught by autocomplete
        if hasattr(obj,'trait_get'):
            try:
                for i in obj.trait_get():
                    if i not in attributes:
                        if hasattr(obj, i):
                            attributes += i
            except:
                pass
    # Get all attribute names.
    str_type = str(type(obj))
    if str_type == "<type 'array'>":
        attributes += dir(obj)
    else:
        attrdict = getAllAttributeNames(obj)
        # Store the obj's dir.
        obj_dir = dir(obj)
        for (obj_type_name, technique, count), attrlist in attrdict.items():
            # This complexity is necessary to avoid accessing all the
            # attributes of the obj.  This is very handy for objects
            # whose attributes are lazily evaluated.
            if type(obj).__name__ == obj_type_name and technique == 'dir':
                attributes += attrlist
            else:
                attributes += [attr for attr in attrlist \
                               if attr not in obj_dir and hasattr(obj, attr)]

    # Remove duplicates from the attribute list.
    for item in attributes:
        dict[item] = None
    attributes = list(dict)
    # new-style swig wrappings can result in non-string attributes
    # e.g. ITK http://www.itk.org/
    attributes = [attribute for attribute in attributes
                  if type(attribute) == str]
    attributes.sort(key=lambda x: x.upper())
    if not includeSingle:
        attributes = filter(lambda item: item[0]!='_' \
                            or item[1:2]=='_', attributes)
    if not includeDouble:
        attributes = filter(lambda item: item[:2]!='__', attributes)
    return attributes

def hasattrAlwaysReturnsTrue(obj):
    return hasattr(obj, 'bogu5_123_aTTri8ute')

def getAllAttributeNames(obj):
    """Return dict of all attributes, including inherited, for an object.

    Recursively walk through a class and all base classes.
    """
    attrdict = {}  # (object, technique, count): [list of attributes]
    # !!!
    # Do Not use hasattr() as a test anywhere in this function,
    # because it is unreliable with remote objects: xmlrpc, soap, etc.
    # They always return true for hasattr().
    # !!!
    try:
        # This could(?) fail if the type is poorly defined without
        # even a name.
        key = type(obj).__name__
    except Exception:
        key = 'anonymous'
    # Wake up sleepy objects - a hack for ZODB objects in "ghost" state.
    wakeupcall = dir(obj)
    del wakeupcall
    # Get attributes available through the normal convention.
    attributes = dir(obj)
    attrdict[(key, 'dir', len(attributes))] = attributes
    # Get attributes from the object's dictionary, if it has one.
    try:
        attributes = sorted(obj.__dict__)
    except Exception:  # Must catch all because object might have __getattr__.
        pass
    else:
        attrdict[(key, '__dict__', len(attributes))] = attributes
    # For a class instance, get the attributes for the class.
    try:
        klass = obj.__class__
    except:  # Must catch all because object might have __getattr__.
        pass
    else:
        if klass is obj:
            # Break a circular reference. This happens with extension
            # classes.
            pass
        else:
            attrdict.update(getAllAttributeNames(klass))
    # Also get attributes from any and all parent classes.
    try:
        bases = obj.__bases__
    except:  # Must catch all because object might have __getattr__.
        pass
    else:
        if isinstance(bases, tuple):
            for base in bases:
                if type(base) is type:
                    # Break a circular reference. Happens in Python 2.2.
                    pass
                else:
                    attrdict.update(getAllAttributeNames(base))
    return attrdict

def getCallTip(command='', locals=None):
    """For a command, return a tuple of object name, argspec, tip text.

    The call tip information will be based on the locals namespace."""
    calltip = ('', '', '')  # object name, argspec, tip text.
    # Get the proper chunk of code from the command.
    root = getRoot(command, terminator='(')
    try:
        if locals is not None:
            obj = eval(root, locals)
        else:
            obj = eval(root)
    except:
        return calltip
    name = ''
    obj, dropSelf = getBaseObject(obj)
    try:
        name = obj.__name__
    except AttributeError:
        pass
    tip1 = ''
    argspec = ''
    obj = inspect.unwrap(obj)
    if inspect.isbuiltin(obj):
        # Builtin functions don't have an argspec that we can get.
        pass
    elif inspect.isfunction(obj):
        # tip1 is a string like: "getCallTip(command='', locals=None)"
        try:
            argspec = str(inspect.signature(obj)) # PY35 or later
        except AttributeError:
            argspec = inspect.getfullargspec(obj)
            argspec = inspect.formatargspec(*argspec)
        if dropSelf:
            # The first parameter to a method is a reference to an
            # instance, usually coded as "self", and is usually passed
            # automatically by Python; therefore we want to drop it.
            temp = argspec.split(',')
            if len(temp) == 1:  # No other arguments.
                argspec = '()'
            elif temp[0][:2] == '(*': # first param is like *args, not self
                pass
            else:  # Drop the first argument.
                argspec = '(' + ','.join(temp[1:]).lstrip()
        tip1 = name + argspec
    doc = ''
    if callable(obj):
        try:
            doc = inspect.getdoc(obj)
        except:
            pass
    if doc:
        # tip2 is the first separated line of the docstring, like:
        # "Return call tip text for a command."
        # tip3 is the rest of the docstring, like:
        # "The call tip information will be based on ... <snip>
        firstline = doc.split('\n')[0].lstrip()
        if tip1 == firstline or firstline[:len(name)+1] == name+'(':
            tip1 = ''
        else:
            tip1 += '\n\n'
        docpieces = doc.split('\n\n')
        tip2 = docpieces[0]
        tip3 = '\n\n'.join(docpieces[1:])
        tip = '%s%s\n\n%s' % (tip1, tip2, tip3)
    else:
        tip = tip1
    # Extract argspec from the signature e.g., (x, /, *, ...) -> int
    m = re.search(r'\((.*)\)', argspec)
    if m:
        argspec = m.group(1)
    calltip = (name, argspec, tip.strip())
    return calltip

def getRoot(command, terminator=None):
    """Return the rightmost root portion of an arbitrary Python command.

    Return only the root portion that can be eval()'d without side
    effects.  The command would normally terminate with a '(' or
    '.'. The terminator and anything after the terminator will be
    dropped."""
    command = command.split('\n')[-1]
    if command.startswith(sys.ps2):
        command = command[len(sys.ps2):]
    command = command.lstrip()
    command = rtrimTerminus(command, terminator)
    if terminator == '.':
        tokens = getTokens(command)
        if tokens and tokens[-1][0] is tokenize.ENDMARKER:
            # Remove the end marker.
            del tokens[-1]
        if tokens and tokens[-1][0] is tokenize.NEWLINE:
            # Remove newline.
            del tokens[-1]
        if tokens and tokens[-1][0] is tokenize.NL:
            # Remove non-logical newline.
            del tokens[-1]
        if not tokens:
            return ''
        if tokens[-1][1] != '.' or tokens[-1][0] is not tokenize.OP:
            # Trap decimals in numbers, versus the dot operator.
            return ''

    # Strip off the terminator.
    if terminator and command.endswith(terminator):
        size = 0 - len(terminator)
        command = command[:size]

    command = command.rstrip()
    tokens = getTokens(command)
    tokens.reverse()
    line = ''
    start = None
    prefix = ''
    laststring = '.'
    lastline = ''
    emptyTypes = ('[]', '()', '{}')
    for token in tokens:
        tokentype = token[0]
        tokenstring = token[1]
        line = token[4]
        if tokentype in (tokenize.ENDMARKER, tokenize.NEWLINE, tokenize.NL):
            continue
        if tokentype is tokenize.ENCODING:
            line = lastline
            break
        if tokentype in (tokenize.NAME, tokenize.STRING, tokenize.NUMBER) \
        and laststring != '.':
            # We've reached something that's not part of the root.
            if prefix and line[token[3][1]] != ' ':
                # If it doesn't have a space after it, remove the prefix.
                prefix = ''
            break
        if tokentype in (tokenize.NAME, tokenize.STRING, tokenize.NUMBER) \
        or (tokentype is tokenize.OP and tokenstring == '.'):
            if prefix:
                # The prefix isn't valid because it comes after a dot.
                prefix = ''
                break
            else:
                # start represents the last known good point in the line.
                start = token[2][1]
        elif len(tokenstring) == 1 and tokenstring in ('[({])}'):
            # Remember, we're working backwards.
            # So prefix += tokenstring would be wrong.
            if prefix in emptyTypes and tokenstring in ('[({'):
                # We've already got an empty type identified so now we
                # are in a nested situation and we can break out with
                # what we've got.
                break
            else:
                prefix = tokenstring + prefix
        else:
            # We've reached something that's not part of the root.
            break
        laststring = tokenstring
        lastline = line
    if start is None:
        start = len(line)
    root = line[start:]
    if prefix in emptyTypes:
        # Empty types are safe to be eval()'d and introspected.
        root = prefix + root
    return root

def getTokens(command):
    """Return list of token tuples for command."""

    # In case the command is unicode try encoding it
    if isinstance(command,  str):
        try:
            command = command.encode('utf-8')
        except UnicodeEncodeError:
            pass # otherwise leave it alone

    f = BytesIO(command)
    # tokens is a list of token tuples, each looking like:
    # (type, string, (srow, scol), (erow, ecol), line)
    tokens = []
    # Can't use list comprehension:
    #   tokens = [token for token in tokenize.generate_tokens(f.readline)]
    # because of need to append as much as possible before TokenError.
    try:
        for t in tokenize.tokenize(f.readline):
            tokens.append(t)
    except tokenize.TokenError:
        # This is due to a premature EOF, which we expect since we are
        # feeding in fragments of Python code.
        pass
    return tokens

def rtrimTerminus(command, terminator=None):
    """Return command minus anything that follows the final terminator."""
    if terminator:
        pieces = command.split(terminator)
        if len(pieces) > 1:
            command = terminator.join(pieces[:-1]) + terminator
    return command

def getBaseObject(obj):
    """Return base object and dropSelf indicator for an object."""
    if inspect.isbuiltin(obj):
        # Builtin functions don't have an argspec that we can get.
        dropSelf = 0
    elif inspect.ismethod(obj):
        # Get the function from the object otherwise
        # inspect.getargspec() complains that the object isn't a
        # Python function.
        try:
            if obj.__self__ is None:
                # This is an unbound method so we do not drop self
                # from the argspec, since an instance must be passed
                # as the first arg.
                dropSelf = 0
            else:
                dropSelf = 1
            obj = obj.__func__
        except AttributeError:
            dropSelf = 0
    elif inspect.isclass(obj):
        # Get the __init__ method function for the class.
        constructor = getConstructor(obj)
        if constructor is not None:
            obj = constructor
            dropSelf = 1
        else:
            dropSelf = 0
    elif callable(obj):
        # Get the __call__ method instead.
        try:
            obj = obj.__call__.__func__
            dropSelf = 1
        except AttributeError:
            dropSelf = 0
    else:
        dropSelf = 0
    return obj, dropSelf

def getConstructor(obj):
    """Return constructor for class object, or None if there isn't one."""
    try:
        return obj.__init__.__func__
    except AttributeError:
        for base in obj.__bases__:
            constructor = getConstructor(base)
            if constructor is not None:
                return constructor
    return None
