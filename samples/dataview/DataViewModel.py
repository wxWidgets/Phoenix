import sys
import wx
import wx.dataview as dv

import random

#----------------------------------------------------------------------

def makeBlank(self):
    # Just a little helper function to make an empty image for our
    # model to use.
    empty = wx.Bitmap(16,16,32)
    dc = wx.MemoryDC(empty)
    dc.SetBackground(wx.Brush((0,0,0,0)))
    dc.Clear()
    del dc
    return empty

#----------------------------------------------------------------------
# We'll use instaces of these classes to hold our music data. Items in the
# tree will get associated back to the coresponding Song or Genre object.

class Song(object):
    def __init__(self, id, artist, title, genre):
        self.id = id
        self.artist = artist
        self.title = title
        self.genre = genre
        self.like = False
        # get a random date value
        d = random.choice(range(27))+1
        m = random.choice(range(12))
        y = random.choice(range(1980, 2005))
        self.date = wx.DateTime.FromDMY(d,m,y)

    def __repr__(self):
        return 'Song: %s-%s' % (self.artist, self.title)


class Genre(object):
    def __init__(self, name):
        self.name = name
        self.songs = []

    def __repr__(self):
        return 'Genre: ' + self.name

#----------------------------------------------------------------------

# This model acts as a bridge between the DataViewCtrl and the music data, and
# organizes it hierarchically as a collection of Genres, each of which is a
# collection of songs.

# This model provides these data columns:
#
#     0. Genre:   string
#     1. Artist:  string
#     2. Title:   string
#     3. id:      integer
#     4. Aquired: date
#     5. Liked:   bool
#

class MyTreeListModel(dv.PyDataViewModel):
    def __init__(self, data, log):
        dv.PyDataViewModel.__init__(self)
        self.data = data
        self.log = log

        # The PyDataViewModel derives from both DataViewModel and from
        # DataViewItemObjectMapper, which has methods that help associate
        # data view items with Python objects. Normally a dictionary is used
        # so any Python object can be used as data nodes. If the data nodes
        # are weak-referencable then the objmapper can use a
        # WeakValueDictionary instead.
        self.UseWeakRefs(True)


    # Report how many columns this model provides data for.
    def GetColumnCount(self):
        return 6


    def GetChildren(self, parent, children):
        # The view calls this method to find the children of any node in the
        # control. There is an implicit hidden root node, and the top level
        # item(s) should be reported as children of this node. A List view
        # simply provides all items as children of this hidden root. A Tree
        # view adds additional items as children of the other items, as needed,
        # to provide the tree hierachy.

        # If the parent item is invalid then it represents the hidden root
        # item, so we'll use the genre objects as its children and they will
        # end up being the collection of visible roots in our tree.
        if not parent:
            for genre in self.data:
                children.append(self.ObjectToItem(genre))
            return len(self.data)

        # Otherwise we'll fetch the python object associated with the parent
        # item and make DV items for each of it's child objects.
        node = self.ItemToObject(parent)
        if isinstance(node, Genre):
            for song in node.songs:
                children.append(self.ObjectToItem(song))
            return len(node.songs)
        return 0


    def IsContainer(self, item):
        # Return True if the item has children, False otherwise.

        # The hidden root is a container
        if not item:
            return True
        # and in this model the genre objects are containers
        node = self.ItemToObject(item)
        if isinstance(node, Genre):
            return True
        # but everything else (the song objects) are not
        return False


    def GetParent(self, item):
        # Return the item which is this item's parent.
        ##self.log.write("GetParent\n")

        if not item:
            return dv.NullDataViewItem

        node = self.ItemToObject(item)
        if isinstance(node, Genre):
            return dv.NullDataViewItem
        elif isinstance(node, Song):
            for g in self.data:
                if g.name == node.genre:
                    return self.ObjectToItem(g)


    def GetValue(self, item, col):
        # Return the value to be displayed for this item and column. For this
        # example we'll just pull the values from the data objects we
        # associated with the items in GetChildren.

        # Fetch the data object for this item.
        node = self.ItemToObject(item)

        if isinstance(node, Genre):
            # We'll only use the first column for the Genre objects,
            # for the other columns lets just return empty values
            mapper = { 0 : node.name,
                       1 : "",
                       2 : "",
                       3 : "",
                       4 : wx.DateTime.FromTimeT(0),  # TODO: There should be some way to indicate a null value...
                       5 : False,
                       }
            return mapper[col]


        elif isinstance(node, Song):
            mapper = { 0 : node.genre,
                       1 : node.artist,
                       2 : node.title,
                       3 : node.id,
                       4 : node.date,
                       5 : node.like,
                       }
            return mapper[col]

        else:
            raise RuntimeError("unknown node type")



    def GetAttr(self, item, col, attr):
        ##self.log.write('GetAttr')
        node = self.ItemToObject(item)
        if isinstance(node, Genre):
            attr.SetColour('blue')
            attr.SetBold(True)
            return True
        return False


    def SetValue(self, value, item, col):
        self.log.write("SetValue: col %d,  %s\n" % (col, value))

        # We're not allowing edits in column zero (see below) so we just need
        # to deal with Song objects and cols 1 - 5

        node = self.ItemToObject(item)
        if isinstance(node, Song):
            if col == 1:
                node.artist = value
            elif col == 2:
                node.title = value
            elif col == 3:
                node.id = value
            elif col == 4:
                node.date = value
            elif col == 5:
                node.like = value
        return True

#----------------------------------------------------------------------

class TestPanel(wx.Panel):
    def __init__(self, parent, log, data=None, model=None):
        self.log = log
        wx.Panel.__init__(self, parent, -1)

        # Create a dataview control
        self.dvc = dv.DataViewCtrl(self,
                                   style=wx.BORDER_THEME
                                   | dv.DV_ROW_LINES # nice alternating bg colors
                                   #| dv.DV_HORIZ_RULES
                                   | dv.DV_VERT_RULES
                                   | dv.DV_MULTIPLE
                                   )

        # Create an instance of our model...
        if model is None:
            self.model = MyTreeListModel(data, log)
        else:
            self.model = model

        # Tel the DVC to use the model
        self.dvc.AssociateModel(self.model)

        # Define the columns that we want in the view.  Notice the
        # parameter which tells the view which col in the data model to pull
        # values from for each view column.
        if 0:
            self.tr = tr = dv.DataViewTextRenderer()
            c0 = dv.DataViewColumn("Genre",   # title
                                   tr,        # renderer
                                   0,         # data model column
                                   width=80)
            self.dvc.AppendColumn(c0)
        else:
            self.dvc.AppendTextColumn("Genre",   0, width=80)

        c1 = self.dvc.AppendTextColumn("Artist",   1, width=170, mode=dv.DATAVIEW_CELL_EDITABLE)
        c2 = self.dvc.AppendTextColumn("Title",    2, width=260, mode=dv.DATAVIEW_CELL_EDITABLE)
        c3 = self.dvc.AppendDateColumn('Acquired', 4, width=100, mode=dv.DATAVIEW_CELL_ACTIVATABLE)
        c4 = self.dvc.AppendToggleColumn('Like',   5, width=40, mode=dv.DATAVIEW_CELL_ACTIVATABLE)

        # Notice how we pull the data from col 3, but this is the 6th col
        # added to the DVC. The order of the view columns is not dependent on
        # the order of the model columns at all.
        c5 = self.dvc.AppendTextColumn("id", 3, width=40,  mode=dv.DATAVIEW_CELL_EDITABLE)
        c5.Alignment = wx.ALIGN_RIGHT

        # Set some additional attributes for all the columns
        for c in self.dvc.Columns:
            c.Sortable = True
            c.Reorderable = True


        self.Sizer = wx.BoxSizer(wx.VERTICAL)
        self.Sizer.Add(self.dvc, 1, wx.EXPAND)

        b1 = wx.Button(self, label="New View", name="newView")
        self.Bind(wx.EVT_BUTTON, self.OnNewView, b1)

        self.Sizer.Add(b1, 0, wx.ALL, 5)


    def OnNewView(self, evt):
        f = wx.Frame(None, title="New view, shared model", size=(600,400))
        TestPanel(f, self.log, model=self.model)
        b = f.FindWindowByName("newView")
        b.Disable()
        f.Show()


#----------------------------------------------------------------------

def main():
    from data import musicdata

    # our data structure will be a collection of Genres, each of which is a
    # collection of Songs
    data = dict()
    for key, artist, title, genre in musicdata:
        song = Song(str(key), artist, title, genre)
        genre = data.get(song.genre)
        if genre is None:
            genre = Genre(song.genre)
            data[song.genre] = genre
        genre.songs.append(song)
    data = data.values()

    app = wx.App()
    frm = wx.Frame(None, title="DataViewModel sample", size=(700,500))
    pnl = TestPanel(frm, sys.stdout, data=data)
    frm.Show()
    app.MainLoop()


#----------------------------------------------------------------------


if __name__ == '__main__':
    main()

