# -*- coding: utf-8 -*-
#!/usr/bin/env python

#---------------------------------------------------------------------------
# Name:        sphinxtools/inheritance.py
# Author:      Andrea Gavana
#
# Created:     30-Nov-2010
# Copyright:   (c) 2013 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

# Standard library imports

import os
import sys
import errno
from subprocess import Popen, PIPE

# Phoenix-specific imports

from .utilities import Wx2Sphinx, FormatExternalLink
from .constants import INHERITANCEROOT

ENOENT = getattr(errno, 'ENOENT', 0)
EPIPE  = getattr(errno, 'EPIPE', 0)

if sys.version_info < (3, ):
    string_base = basestring
else:    
    string_base = str


class InheritanceDiagram(object):
    """
    Given a list of classes, determines the set of classes that they inherit
    from all the way to the root "object", and then is able to generate a
    graphviz dot graph from them.
    """

    def __init__(self, classes, main_class=None):

        if main_class is None:
            self.class_info, self.specials = classes
            self.class_info = list(self.class_info.values())
        else:
            self.class_info, self.specials = self._class_info(classes)
            
        self.main_class = main_class


    def _class_info(self, classes):
        """Return name and bases for all classes that are ancestors of
        *classes*.

        *parts* gives the number of dotted name parts that is removed from the
        displayed node names.
        """

        all_classes = {}
        specials = []

        def recurse(cls):
            nodename, fullname = self.class_name(cls)
            if cls in [object] or nodename.startswith('sip.'):
                return
            
            baselist = []
            all_classes[cls] = (nodename, fullname, baselist)

            for base in cls.__bases__:
                if base in [object] or self.class_name(base)[0].startswith('sip.'):
                    continue
                baselist.append(self.class_name(base)[0])
                if base not in all_classes:
                    recurse(base)

        for cls in classes:
            recurse(cls)
            specials.append(self.class_name(cls)[1])

        return list(all_classes.values()), specials


    def class_name(self, cls):
        """Given a class object, return a fully-qualified name.

        This works for things I've tested in matplotlib so far, but may not be
        completely general.
        """

        module = cls.__module__

        if module == '__builtin__':
            fullname = cls.__name__
        else:
            fullname = '%s.%s' % (module, cls.__name__)

        name_parts = fullname.split('.')
        if 'wx._' in fullname:
            nodename = fullname = name_parts[-1]
        else:
            # Just the last 2 parts
            nodename = '.'.join(name_parts[-2:])
            if fullname.startswith('wx.'):
                fullname = fullname[3:]
                
        return nodename, fullname


    # These are the default attrs for graphviz
    default_graph_attrs = {
        'rankdir': 'TB',
        'size': '"8.0, 12.0"',
    }
    default_node_attrs = {
        'shape': 'box',
        'fontsize': 10,
        'height': 0.3,
        'fontname': 'Vera Sans, DejaVu Sans, Liberation Sans, '
                    'Arial, Helvetica, sans',
        'style': '"setlinewidth(0.5)"',
    }
    default_edge_attrs = {
        'arrowsize': 0.5,
        'style': '"setlinewidth(0.5)"',
    }

    def _format_node_attrs(self, attrs):
        return ','.join(['%s=%s' % x for x in list(attrs.items())])

    def _format_graph_attrs(self, attrs):
        return ''.join(['%s=%s;\n' % x for x in list(attrs.items())])

    def generate_dot(self, class_summary, name="dummy", graph_attrs={}, node_attrs={}, edge_attrs={}):
        """Generate a graphviz dot graph from the classes that were passed in
        to __init__.

        *name* is the name of the graph.

        *graph_attrs*, *node_attrs*, *edge_attrs* are dictionaries containing
        key/value pairs to pass on as graphviz properties.
        """

        inheritance_graph_attrs = dict(fontsize=9, ratio='auto', size='""', rankdir="TB")
        inheritance_node_attrs = {"align": "center", 'shape': 'box',
                                  'fontsize': 10, 'height': 0.3,
                                  'fontname': 'Vera Sans, DejaVu Sans, Liberation Sans, '
                                  'Arial, Helvetica, sans', 'style': '"setlinewidth(0.5)"',
                                  'labelloc': 'c', 'fontcolor': 'grey45'}

        inheritance_edge_attrs = {'arrowsize': 0.5, 
                                  'style': '"setlinewidth(0.5)"', 
                                  'color': '"#23238E"',
                                  'dir': 'back',
                                  'arrowtail': 'open',
                                  }

        g_attrs = self.default_graph_attrs.copy()
        n_attrs = self.default_node_attrs.copy()
        e_attrs = self.default_edge_attrs.copy()
        g_attrs.update(inheritance_graph_attrs)
        n_attrs.update(inheritance_node_attrs)
        e_attrs.update(inheritance_edge_attrs)

        res = []
        res.append('digraph %s {\n' % name)
        res.append(self._format_graph_attrs(g_attrs))

        for name, fullname, bases in self.class_info:
            # Write the node
            this_node_attrs = n_attrs.copy()

            if fullname in self.specials:
                this_node_attrs['fontcolor'] = 'black'
                this_node_attrs['color'] = 'blue'
                this_node_attrs['style'] = 'bold'

            if self.main_class is None:
                newname, fullname = Wx2Sphinx(name)
            else:
                newname = name

            if class_summary is None:
                # Phoenix base classes, assume there is always a link
                this_node_attrs['URL'] = '"%s.html"'%fullname
            else:
                if 'wx.' in fullname:
                    fullname = fullname[3:]
                
                if fullname in class_summary:
                    this_node_attrs['URL'] = '"%s.html"'%fullname
                else:
                    full_page = FormatExternalLink(fullname, inheritance=True)
                    if full_page:
                        this_node_attrs['URL'] = full_page
                    
            res.append('  "%s" [%s];\n' %
                       (newname, self._format_node_attrs(this_node_attrs)))

            # Write the edges
            for base_name in bases:

                this_edge_attrs = e_attrs.copy()
                if fullname in self.specials:
                    this_edge_attrs['color'] = 'red'

                if self.main_class is None:
                    base_name, dummy = Wx2Sphinx(base_name)

                res.append('  "%s" -> "%s" [%s];\n' %
                           (base_name, newname,
                            self._format_node_attrs(this_edge_attrs)))
        res.append('}\n')
        return ''.join(res)


    # ----------------------------------------------------------------------- #

    def MakeInheritanceDiagram(self, class_summary=None):
        """
        Actually generates the inheritance diagram as a PNG file plus the corresponding
        MAP file for mouse navigation over the inheritance boxes.

        These two files are saved into the ``INHERITANCEROOT`` folder (see `sphinxtools/constants.py`
        for more information).

        :param `class_summary`: if not ``None``, used to identify if a class is actually been
         wrapped or not (to avoid links pointing to non-existent pages).

        :rtype: `tuple`

        :returns: a tuple containing the PNG file name and a string representing the content
         of the MAP file (with newlines stripped away).

        .. note:: The MAP file is deleted as soon as its content has been read.
        """

        static_root = INHERITANCEROOT

        if self.main_class is not None:
            filename = self.main_class.name
        else:                        
            dummy, filename = Wx2Sphinx(self.specials[0])

        outfn = os.path.join(static_root, filename + '_inheritance.png')
        mapfile = outfn + '.map'

        if os.path.isfile(outfn) and os.path.isfile(mapfile):
            fid = open(mapfile, 'rt')
            map = fid.read()
            fid.close()
            return os.path.split(outfn)[1], map.replace('\n', ' ')

        code = self.generate_dot(class_summary)

        # graphviz expects UTF-8 by default
        if isinstance(code, string_base):
            code = code.encode('utf-8')

        dot_args = ['dot']

        if os.path.isfile(outfn):
            os.remove(outfn)
        if os.path.isfile(mapfile):
            os.remove(mapfile)

        dot_args.extend(['-Tpng', '-o' + outfn])
        dot_args.extend(['-Tcmapx', '-o' + mapfile])

        try:

            p = Popen(dot_args, stdout=PIPE, stdin=PIPE, stderr=PIPE)

        except OSError as err:

            if err.errno != ENOENT:   # No such file or directory
                raise

            print('\nERROR: Graphviz command `dot` cannot be run (needed for Graphviz output), check your ``PATH`` setting')

        try:
            # Graphviz may close standard input when an error occurs,
            # resulting in a broken pipe on communicate()
            stdout, stderr = p.communicate(code)

        except OSError as err:

            # in this case, read the standard output and standard error streams
            # directly, to get the error message(s)
            stdout, stderr = p.stdout.read(), p.stderr.read()
            p.wait()

        if p.returncode != 0:
            print(('\nERROR: Graphviz `dot` command exited with error:\n[stderr]\n%s\n[stdout]\n%s\n\n' % (stderr, stdout)))

        fid = open(mapfile, 'rt')
        map = fid.read()
        fid.close()

        return os.path.split(outfn)[1], map.replace('\n', ' ')
