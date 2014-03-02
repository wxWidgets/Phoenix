"""Filling is the gui tree control through which a user can navigate
the local namespace or any object."""

__author__ = "Patrick K. O'Brien <pobrien@orbtech.com>"
# Tags: py3-port

import wx
import wx.lib.six as six

from . import dispatcher
from . import editwindow
from . import images
import inspect
from . import introspect
import types


COMMONTYPES = [getattr(types, t) for t in dir(types) \
               if not t.startswith('_') \
               and t not in ('ClassType', 'InstanceType', 'ModuleType')]

DOCTYPES = ('BuiltinFunctionType', 'BuiltinMethodType', 'ClassType',
            'FunctionType', 'GeneratorType', 'InstanceType',
            'LambdaType', 'MethodType', 'ModuleType',
            'UnboundMethodType', 'method-wrapper')

SIMPLETYPES = [getattr(types, t) for t in dir(types) \
               if not t.startswith('_') and t not in DOCTYPES]

#del t

try:
    COMMONTYPES.append(type(''.__repr__))  # Method-wrapper in version 2.2.x.
except AttributeError:
    pass


class FillingTree(wx.TreeCtrl):
    """FillingTree based on TreeCtrl."""
    
    name = 'Filling Tree'

    def __init__(self, parent, id=-1, pos=wx.DefaultPosition,
                 size=wx.DefaultSize, style=wx.TR_DEFAULT_STYLE,
                 rootObject=None, rootLabel=None, rootIsNamespace=False,
                 static=False):
        """Create FillingTree instance."""
        wx.TreeCtrl.__init__(self, parent, id, pos, size, style)
        self.rootIsNamespace = rootIsNamespace
        import __main__
        if rootObject is None:
            rootObject = __main__.__dict__
            self.rootIsNamespace = True
        if rootObject is __main__.__dict__ and rootLabel is None:
            rootLabel = 'locals()'
        if not rootLabel:
            rootLabel = 'Ingredients'
        self.item = self.root = self.AddRoot(rootLabel, -1, -1, rootObject)
        self.SetItemHasChildren(self.root, self.objHasChildren(rootObject))
        self.Bind(wx.EVT_TREE_ITEM_EXPANDING, self.OnItemExpanding, id=self.GetId())
        self.Bind(wx.EVT_TREE_ITEM_COLLAPSED, self.OnItemCollapsed, id=self.GetId())
        self.Bind(wx.EVT_TREE_SEL_CHANGED, self.OnSelChanged, id=self.GetId())
        self.Bind(wx.EVT_TREE_ITEM_ACTIVATED, self.OnItemActivated, id=self.GetId())
        if not static:
            dispatcher.connect(receiver=self.push, signal='Interpreter.push')

    def push(self, command, more):
        """Receiver for Interpreter.push signal."""
        self.display()

    def OnItemExpanding(self, event):
        """Add children to the item."""
        busy = wx.BusyCursor()
        item = event.GetItem()
        if self.IsExpanded(item):
            return
        self.addChildren(item)
#        self.SelectItem(item)

    def OnItemCollapsed(self, event):
        """Remove all children from the item."""
        busy = wx.BusyCursor()
        item = event.GetItem()
#        self.CollapseAndReset(item)
#        self.DeleteChildren(item)
#        self.SelectItem(item)

    def OnSelChanged(self, event):
        """Display information about the item."""
        busy = wx.BusyCursor()
        self.item = event.GetItem()
        self.display()

    def OnItemActivated(self, event):
        """Launch a DirFrame."""
        item = event.GetItem()
        text = self.getFullName(item)
        obj = self.GetItemData(item)
        frame = FillingFrame(parent=self, size=(600, 100), rootObject=obj,
                             rootLabel=text, rootIsNamespace=False)
        frame.Show()

    def objHasChildren(self, obj):
        """Return true if object has children."""
        if self.objGetChildren(obj):
            return True
        else:
            return False

    def objGetChildren(self, obj):
        """Return dictionary with attributes or contents of object."""
        busy = wx.BusyCursor()
        otype = type(obj)
        if (isinstance(obj, dict)
            or 'BTrees' in six.text_type(otype)
            and hasattr(obj, 'keys')):
            return obj
        d = {}
        if isinstance(obj, (list, tuple)):
            for n in range(len(obj)):
                key = '[' + six.text_type(n) + ']'
                d[key] = obj[n]
        if otype not in COMMONTYPES:
            for key in introspect.getAttributeNames(obj):
                # Believe it or not, some attributes can disappear,
                # such as the exc_traceback attribute of the sys
                # module. So this is nested in a try block.
                try:
                    d[key] = getattr(obj, key)
                except Exception:
                    pass
        return d

    def addChildren(self, item):
        self.DeleteChildren(item)
        obj = self.GetItemData(item)
        children = self.objGetChildren(obj)
        if not children:
            return
        keys = sorted(children.keys(), key=lambda x: six.text_type(x).lower())
        for key in keys:
            itemtext = six.text_type(key)
            # Show string dictionary items with single quotes, except
            # for the first level of items, if they represent a
            # namespace.
            if isinstance(obj, dict) \
            and isinstance(key, six.string_types) \
            and (item != self.root
                 or (item == self.root and not self.rootIsNamespace)):
                itemtext = repr(key)
            child = children[key]
            branch = self.AppendItem(parent=item, text=itemtext, data=child)
            self.SetItemHasChildren(branch, self.objHasChildren(child))

    def display(self):
        item = self.item
        if not item:
            return
        if self.IsExpanded(item):
            self.addChildren(item)
        self.setText('')
        obj = self.GetItemData(item)
        if wx.Platform == '__WXMSW__':
            if obj is None: # Windows bug fix.
                return
        self.SetItemHasChildren(item, self.objHasChildren(obj))
        otype = type(obj)
        text = ''
        text += self.getFullName(item)
        text += '\n\nType: ' + six.text_type(otype)
        try:
            value = six.text_type(obj)
        except Exception:
            value = ''
        if isinstance(obj, six.string_types):
            value = repr(obj)
        text += u'\n\nValue: ' + value
        if otype not in SIMPLETYPES:
            try:
                text += '\n\nDocstring:\n\n"""' + \
                        inspect.getdoc(obj).strip() + '"""'
            except Exception:
                pass
        if isinstance(obj, six.class_types):
            try:
                text += '\n\nClass Definition:\n\n' + \
                        inspect.getsource(obj.__class__)
            except Exception:
                pass
        else:
            try:
                text += '\n\nSource Code:\n\n' + \
                        inspect.getsource(obj)
            except Exception:
                pass
        self.setText(text)

    def getFullName(self, item, partial=''):
        """Return a syntactically proper name for item."""
        name = self.GetItemText(item)
        parent = None
        obj = None
        if item != self.root:
            parent = self.GetItemParent(item)
            obj = self.GetItemData(parent)
        # Apply dictionary syntax to dictionary items, except the root
        # and first level children of a namepace.
        if ((isinstance(obj, dict)
            or 'BTrees' in six.text_type(type(obj))
            and hasattr(obj, 'keys'))
            and ((item != self.root and parent != self.root)
            or (parent == self.root and not self.rootIsNamespace))):
            name = '[' + name + ']'
        # Apply dot syntax to multipart names.
        if partial:
            if partial[0] == '[':
                name += partial
            else:
                name += '.' + partial
        # Repeat for everything but the root item
        # and first level children of a namespace.
        if (item != self.root and parent != self.root) \
        or (parent == self.root and not self.rootIsNamespace):
            name = self.getFullName(parent, partial=name)
        return name

    def setText(self, text):
        """Display information about the current selection."""

        # This method will likely be replaced by the enclosing app to
        # do something more interesting, like write to a text control.
        print(text)

    def setStatusText(self, text):
        """Display status information."""

        # This method will likely be replaced by the enclosing app to
        # do something more interesting, like write to a status bar.
        print(text)


class FillingText(editwindow.EditWindow):
    """FillingText based on StyledTextCtrl."""

    name = 'Filling Text'

    def __init__(self, parent, id=-1, pos=wx.DefaultPosition,
                 size=wx.DefaultSize, style=wx.CLIP_CHILDREN,
                 static=False):
        """Create FillingText instance."""
        editwindow.EditWindow.__init__(self, parent, id, pos, size, style)
        # Configure various defaults and user preferences.
        self.SetReadOnly(True)
        self.SetWrapMode(True)
        self.SetMarginWidth(1, 0)
        if not static:
            dispatcher.connect(receiver=self.push, signal='Interpreter.push')

    def push(self, command, more):
        """Receiver for Interpreter.push signal."""
        self.Refresh()

    def SetText(self, *args, **kwds):
        self.SetReadOnly(False)
        editwindow.EditWindow.SetText(self, *args, **kwds)
        self.SetReadOnly(True)


class Filling(wx.SplitterWindow):
    """Filling based on wxSplitterWindow."""

    name = 'Filling'

    def __init__(self, parent, id=-1, pos=wx.DefaultPosition,
                 size=wx.DefaultSize, style=wx.SP_3D|wx.SP_LIVE_UPDATE,
                 name='Filling Window', rootObject=None,
                 rootLabel=None, rootIsNamespace=False, static=False):
        """Create a Filling instance."""
        wx.SplitterWindow.__init__(self, parent, id, pos, size, style, name)

        self.tree = FillingTree(parent=self, rootObject=rootObject,
                                rootLabel=rootLabel,
                                rootIsNamespace=rootIsNamespace,
                                static=static)
        self.text = FillingText(parent=self, static=static)
        
        wx.CallLater(1, self.SplitVertically, self.tree, self.text, 200)
        
        self.SetMinimumPaneSize(1)

        # Override the filling so that descriptions go to FillingText.
        self.tree.setText = self.text.SetText

        # Display the root item.
        self.tree.SelectItem(self.tree.root)
        self.tree.display()

        self.Bind(wx.EVT_SPLITTER_SASH_POS_CHANGED, self.OnChanged)

    def OnChanged(self, event):
        #this is important: do not evaluate this event=> otherwise,
        # splitterwindow behaves strangely
        #event.Skip()
        pass


    def LoadSettings(self, config):
        pos = config.ReadInt('Sash/FillingPos', 200)
        wx.CallLater(250, self.SetSashPosition, pos)
        zoom = config.ReadInt('View/Zoom/Filling', -99)
        if zoom != -99:
            self.text.SetZoom(zoom)

    def SaveSettings(self, config):
        config.WriteInt('Sash/FillingPos', self.GetSashPosition())
        config.WriteInt('View/Zoom/Filling', self.text.GetZoom())



class FillingFrame(wx.Frame):
    """Frame containing the namespace tree component."""

    name = 'Filling Frame'

    def __init__(self, parent=None, id=-1, title='PyFilling',
                 pos=wx.DefaultPosition, size=(600, 400),
                 style=wx.DEFAULT_FRAME_STYLE, rootObject=None,
                 rootLabel=None, rootIsNamespace=False, static=False):
        """Create FillingFrame instance."""
        wx.Frame.__init__(self, parent, id, title, pos, size, style)
        intro = 'PyFilling - The Tastiest Namespace Inspector'
        self.CreateStatusBar()
        self.SetStatusText(intro)
        self.SetIcon(images.getPyIcon())
        self.filling = Filling(parent=self, rootObject=rootObject,
                               rootLabel=rootLabel,
                               rootIsNamespace=rootIsNamespace,
                               static=static)
        # Override so that status messages go to the status bar.
        self.filling.tree.setStatusText = self.SetStatusText


class App(wx.App):
    """PyFilling standalone application."""

    def OnInit(self):
        self.fillingFrame = FillingFrame()
        self.fillingFrame.Show(True)
        self.SetTopWindow(self.fillingFrame)
        return True
