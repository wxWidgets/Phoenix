# Author: Samuel Dunn
# Intent: Provide an admonishment for wx deprecations
# Date: 2 / 19 / 18

from docutils import nodes
from docutils.parsers.rst import Directive

from sphinx.locale import _ as convertLocale

class wxdeprecated_node(nodes.Admonition, nodes.Element): pass

def visit_wxdeprecated_node(self, node):
    for c in ('admonition', 'wxdeprecated'):
        if not c in node.get('classes'):
            node.get('classes').append(c)

    self.visit_admonition(node)

def depart_wxdeprecated_node(self, node):
    self.depart_admonition(node)


# Barely more than a copy-paste from sphinx-doc.org/en/1.6/extdev/tutorial.html
class wxDeprecated(Directive):
    has_content = True

    def run(self):
        # docutils will assign magic-members to the instance
        # before invoking run.

        # convenience reference to the build environment:
        env = self.state.document.settings.env

        targetid = "deprecated-{}".format(env.new_serialno('deprecated'))
        targetnode = nodes.target("", "", ids=[targetid])   # ?

        # create a node and pass content and such in.
        dn = wxdeprecated_node("\n".join(self.content))
        dn += nodes.title(convertLocale("Deprecated"), convertLocale("Deprecated"))

        # Parse all sub-elements into deprecation_node instance
        self.state.nested_parse(self.content, self.content_offset, dn)

        if not hasattr(env, 'all_deprecations'):
            env.all_deprecations = []

        env.all_deprecations.append(
            {
                'docname'    : env.docname,
                'lineno'     : self.lineno,
                'deprecated' : dn.deepcopy(),
                'target'     : targetnode
            })

        return [targetnode, dn]


def setup(app):
  app.add_node(wxdeprecated_node, html=(visit_wxdeprecated_node, depart_wxdeprecated_node))
  app.add_directive('wxdeprecated', wxDeprecated)
