# -*- coding: utf-8 -*-
#!/usr/bin/env python

#---------------------------------------------------------------------------
# Name:        sphinxtools/inheritance.py
# Author:      Andrea Gavana
#
# Created:     30-Nov-2010
# Copyright:   (c) 2011 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

# Standard library imports

import os
import errno
from subprocess import Popen, PIPE

# Phoenix-specific imports

from utilities import Wx2Sphinx
from constants import INHERITANCEROOT

ENOENT = getattr(errno, 'ENOENT', 0)
EPIPE  = getattr(errno, 'EPIPE', 0)


class InheritanceDiagram(object):
    """
    Given a list of classes, determines the set of classes that they inherit
    from all the way to the root "object", and then is able to generate a
    graphviz dot graph from them.
    """

    # ----------------------------------------------------------------------- #

    def __init__(self, class_info):

        print class_info
        print
        print
        
        self.class_info, self.specials = class_info


    # These are the default attrs for graphviz
    default_graph_attrs = {
        'rankdir': 'LR',
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


    # ----------------------------------------------------------------------- #

    def FormatNodeAttrs(self, attrs):

        return ','.join(['%s=%s' % x for x in attrs.items()])


    # ----------------------------------------------------------------------- #

    def FormatGraphAttrs(self, attrs):

        return ''.join(['%s=%s;\n' % x for x in attrs.items()])


    # ----------------------------------------------------------------------- #

    def GenerateDot(self, name="dummy"):
        """
        Generate a graphviz dot graph from the classes that were passed in to `__init__`.

        :param string `name`: the name of the graph.

        :rtype: `string`

        :returns: A string representing the Graphviz dot diagram.        
        """

        inheritance_graph_attrs = dict(fontsize=9, ratio='auto', size='""', rankdir="LR")
        inheritance_node_attrs = {"align": "center", 'shape': 'box',
                                  'fontsize': 10, 'height': 0.3,
                                  'fontname': 'Vera Sans, DejaVu Sans, Liberation Sans, '
                                  'Arial, Helvetica, sans', 'style': '"setlinewidth(0.5)"',
                                  'labelloc': 'c', 'fontcolor': 'grey45'}

        inheritance_edge_attrs = {'arrowsize': 0.5, 'style': '"setlinewidth(0.5)"', "color": "black"}
        
        g_attrs = self.default_graph_attrs.copy()
        n_attrs = self.default_node_attrs.copy()
        e_attrs = self.default_edge_attrs.copy()
        g_attrs.update(inheritance_graph_attrs)
        n_attrs.update(inheritance_node_attrs)
        e_attrs.update(inheritance_edge_attrs)

        res = []
        res.append('digraph %s {\n' % name)
        res.append(self.FormatGraphAttrs(g_attrs))

        for name, fullname, bases in self.class_info.values():
            # Write the node
            this_node_attrs = n_attrs.copy()

            if name in self.specials:
                this_node_attrs['fontcolor'] = 'black'
                this_node_attrs['color'] = 'blue'
                this_node_attrs['style'] = 'bold'

            newname, fullname = Wx2Sphinx(name)

            this_node_attrs['URL'] = '"%s.html"'%fullname
            res.append('  "%s" [%s];\n' %
                       (newname, self.FormatNodeAttrs(this_node_attrs)))

            # Write the edges
            for base_name in bases:

                this_edge_attrs = e_attrs.copy()
                if name in self.specials:
                    this_edge_attrs['color'] = 'red'

                base_name, dummy = Wx2Sphinx(base_name)
                    
                res.append('  "%s" -> "%s" [%s];\n' %
                           (base_name, newname,
                            self.FormatNodeAttrs(this_edge_attrs)))
        res.append('}\n')
        return ''.join(res)


    # ----------------------------------------------------------------------- #

    def MakeInheritanceDiagram(self):
        """
        Actually generates the inheritance diagram as a PNG file plus the corresponding
        MAP file for mouse navigation over the inheritance boxes.

        These two files are saved into the ``INHERITANCEROOT`` folder (see `sphinxtools/constants.py`
        for more information).

        :rtype: `tuple`

        :returns: a tuple containing the PNG file name and a string representing the content
         of the MAP file (with newlines stripped away).

        .. note:: The MAP file is deleted as soon as its content has been read.         
        """

        code = self.GenerateDot()
        
        # graphviz expects UTF-8 by default
        if isinstance(code, unicode):
            code = code.encode('utf-8')

        static_root = INHERITANCEROOT

        dot_args = ['dot']
        dummy, filename = Wx2Sphinx(self.specials[0])
        outfn = os.path.join(static_root, filename + '_inheritance.png')

        if os.path.isfile(outfn):
            os.remove(outfn)
        if os.path.isfile(outfn + '.map'):
            os.remove(outfn + '.map')
            
        dot_args.extend(['-Tpng', '-o' + outfn])
        dot_args.extend(['-Tcmapx', '-o%s.map' % outfn])
        
        try:
            
            p = Popen(dot_args, stdout=PIPE, stdin=PIPE, stderr=PIPE)

        except OSError, err:

            if err.errno != ENOENT:   # No such file or directory
                raise

            print '\nERROR: Graphviz command `dot` cannot be run (needed for Graphviz output), check your ``PATH`` setting'
        
        try:
            # Graphviz may close standard input when an error occurs,
            # resulting in a broken pipe on communicate()
            stdout, stderr = p.communicate(code)

        except OSError, err:

            # in this case, read the standard output and standard error streams
            # directly, to get the error message(s)
            stdout, stderr = p.stdout.read(), p.stderr.read()
            p.wait()
            
        if p.returncode != 0:
            print '\nERROR: Graphviz `dot` command exited with error:\n[stderr]\n%s\n[stdout]\n%s\n\n' % (stderr, stdout)

        mapfile = outfn + '.map'

        fid = open(mapfile, 'rt')
        map = fid.read()
        fid.close()
        
        os.remove(mapfile)        
        
        return os.path.split(outfn)[1], map.replace('\n', ' ')

