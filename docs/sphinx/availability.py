# -*- coding: utf-8 -*-

"""
Allow "availability" admonitions to be inserted into your documentation.
Inclusion of availabilities can be switched of by a configuration variable.
The availabilitylist directive collects all availabilities of your project
and lists them along with a backlink to the original location.
"""

from docutils import nodes

from sphinx.locale import _
try:
    from sphinx.errors import NoUri         # since Sphinx 3.0
except ImportError:
    from sphinx.environment import NoUri    # till Sphinx 3.0
from sphinx.util.nodes import set_source_info
from docutils.parsers.rst import Directive

# ----------------------------------------------------------------------- #
class availability_node(nodes.Admonition, nodes.Element): pass

# ----------------------------------------------------------------------- #
class availabilitylist(nodes.General, nodes.Element): pass

# ----------------------------------------------------------------------- #


class Availability(Directive):
    """
    An "availability" entry, displayed (if configured) in the form of an admonition.
    """

    has_content = True
    required_arguments = 0
    optional_arguments = 0
    final_argument_whitespace = False
    option_spec = {}


   # ----------------------------------------------------------------------- #

    def run(self):
        env = self.state.document.settings.env
        targetid = 'index-%s' % env.new_serialno('index')
        targetnode = nodes.target('', '', ids=[targetid])

        avail_node = availability_node('\n'.join(self.content))
        avail_node += nodes.title(_("Availability"), _("Availability"))

        self.state.nested_parse(self.content, self.content_offset, avail_node)

        return [targetnode, avail_node]

# ----------------------------------------------------------------------- #

def process_availabilities(app, doctree):
    # collect all availabilities in the environment
    # this is not done in the directive itself because it some transformations
    # must have already been run, e.g. substitutions
    env = app.builder.env
    if not hasattr(env, 'availability_all_availabilities'):
        env.availability_all_availabilities = []
    for node in doctree.traverse(availability_node):
        try:
            targetnode = node.parent[node.parent.index(node) - 1]
            if not isinstance(targetnode, nodes.target):
                raise IndexError
        except IndexError:
            targetnode = None
        env.availability_all_availabilities.append({
            'docname': env.docname,
            'source': node.source or env.doc2path(env.docname),
            'lineno': node.line,
            'availability': node.deepcopy(),
            'target': targetnode,
        })


# ----------------------------------------------------------------------- #

class AvailabilityList(Directive):
    """
    A list of all availability entries.
    """

    has_content = False
    required_arguments = 0
    optional_arguments = 0
    final_argument_whitespace = False
    option_spec = {}


   # ----------------------------------------------------------------------- #

    def run(self):
        # Simply insert an empty availabilitylist node which will be replaced later
        # when process_availability_nodes is called
        return [availabilitylist('')]


# ----------------------------------------------------------------------- #

def process_availability_nodes(app, doctree, fromdocname):
    if not app.config['availability_include_availabilities']:
        for node in doctree.traverse(availability_node):
            node.parent.remove(node)

    # Replace all availabilitylist nodes with a list of the collected availabilities.
    # Augment each availability with a backlink to the original location.
    env = app.builder.env

    if not hasattr(env, 'availability_all_availabilities'):
        env.availability_all_availabilities = []

    for node in doctree.traverse(availabilitylist):
        if not app.config['availability_include_availabilities']:
            node.replace_self([])
            continue

        content = []

        for availability_info in env.availability_all_availabilities:
            para = nodes.paragraph(classes=['availability-source'])
            description = _('(The <<original entry>> is located in '
                            ' %s, line %d.)') % \
                          (availability_info['source'], availability_info['lineno'])
            desc1 = description[:description.find('<<')]
            desc2 = description[description.find('>>')+2:]
            para += nodes.Text(desc1, desc1)

            # Create a reference
            newnode = nodes.reference('', '', internal=True)
            innernode = nodes.emphasis(_('original entry'), _('original entry'))
            try:
                newnode['refuri'] = app.builder.get_relative_uri(
                    fromdocname, availability_info['docname'])
                newnode['refuri'] += '#' + availability_info['target']['refid']
            except NoUri:
                # ignore if no URI can be determined, e.g. for LaTeX output
                pass
            newnode.append(innernode)
            para += newnode
            para += nodes.Text(desc2, desc2)

            # (Recursively) resolve references in the availability content
            availability_entry = availability_info['availability']
            env.resolve_references(availability_entry, availability_info['docname'],
                                   app.builder)

            # Insert into the availabilitylist
            content.append(availability_entry)
            content.append(para)

        node.replace_self(content)


# ----------------------------------------------------------------------- #

def purge_availabilities(app, env, docname):
    if not hasattr(env, 'availability_all_availabilities'):
        return
    env.availability_all_availabilities = [availability for availability in env.availability_all_availabilities
                                           if availability['docname'] != docname]


# ----------------------------------------------------------------------- #

def visit_availability_node(self, node):
    classes = node.get('classes')
    for c in ("admonition", "availability"):
        if not c in classes:
            classes.append(c)

    self.visit_admonition(node)


# ----------------------------------------------------------------------- #

def depart_availability_node(self, node):
    self.depart_admonition(node)


# ----------------------------------------------------------------------- #

def setup(app):
    app.add_js_file('javascript/header.js')
    app.add_js_file('javascript/sidebar.js')
    app.add_js_file('javascript/jquery.collapse.js')
    app.add_js_file('javascript/jquery.cookie.js')
    app.add_js_file('javascript/toggle_visibility.js')

    app.add_config_value('availability_include_availabilities', False, False)

    app.add_node(availabilitylist)
    app.add_node(availability_node,
                 html=(visit_availability_node, depart_availability_node),
                 latex=(visit_availability_node, depart_availability_node),
                 text=(visit_availability_node, depart_availability_node),
                 man=(visit_availability_node, depart_availability_node),
                 texinfo=(visit_availability_node, depart_availability_node))

    app.add_directive('availability', Availability)
    app.add_directive('availabilitylist', AvailabilityList)
    app.connect('doctree-read', process_availabilities)
    app.connect('doctree-resolved', process_availability_nodes)
    app.connect('env-purge-doc', purge_availabilities)


# ----------------------------------------------------------------------- #
