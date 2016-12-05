#!/usr/bin/env python

"""
BNA-Editor: a simple app for editing polygons in BNA files

BNA is a simple text format for storing polygons in lat-long coordinates.

"""
import os, sys
import sets

import numpy as N

#### import local version:
#sys.path.append("..")
#from floatcanvas import NavCanvas, FloatCanvas

## import the installed version
from wx.lib.floatcanvas import NavCanvas, FloatCanvas

import wx
import sys

if len(sys.argv) > 1:
    StartFileName = sys.argv[1]
else:
    StartFileName = None

### These utilities are required to load and save BNA data.
class BNAData:
    """
    Class to store the full set of data in a BNA file

    """
    def __init__(self, Filename = None):
        self.Filename = Filename
        self.PointsData = None
        self.Filename = None
        self.Names = None
        self.Types = None
        if Filename is not None:
            self.Load(Filename)

    def __getitem__(self,index):
        return (self.PointsData[index], self.Names[index])

    def __len__(self):
        return len(self.PointsData)

    def Save(self, filename = None):
        if not filename:
            filename = self.filename
        file = open(filename, 'w')
        for i, points in enumerate(self.PointsData):
            file.write('"%s","%s", %i\n'%(self.Names[i],self.Types[i],len(points) ) )
            for p in points:
                file.write("%.12f,%.12f\n"%(tuple(p)))

    def Load(self, filename):
        #print("Loading:", filename)
        file = open(filename,'rU')

        self.Filename = filename
        self.PointsData = []
        self.Names = []
        self.Types = []
        while 1:
            line = file.readline()
            if not line:
                break
            line = line.strip()
            Name, line = line.split('","')
            Name = Name[1:]
            Type,line = line.split('",')
            num_points = int(line)
            self.Types.append(Type)
            self.Names.append(Name)
            polygon = N.zeros((num_points,2),N.float)
            for i in range(num_points):
                polygon[i,:] = map(float, file.readline().split(','))
            self.PointsData.append(polygon)

        file.close()
        return None

class DrawFrame(wx.Frame):
    """
    A frame used for the BNA Editor

    """

    def __init__(self,parent, id,title,position,size):
        wx.Frame.__init__(self,parent, id,title,position, size)

        ## Set up the MenuBar
        MenuBar = wx.MenuBar()

        FileMenu = wx.Menu()

        OpenMenu = FileMenu.Append(wx.ID_ANY, "&Open", "Open BNA")
        self.Bind(wx.EVT_MENU, self.OpenBNA, OpenMenu)

        SaveMenu = FileMenu.Append(wx.ID_ANY, "&Save", "Save BNA")
        self.Bind(wx.EVT_MENU, self.SaveBNA, SaveMenu)

        CloseMenu = FileMenu.Append(wx.ID_EXIT, "", "Close Application")
        self.Bind(wx.EVT_MENU, self.OnQuit, CloseMenu)

        MenuBar.Append(FileMenu, "&File")

        view_menu = wx.Menu()
        ZoomMenu = view_menu.Append(wx.ID_ANY, "Zoom to &Fit","Zoom to fit the window")
        self.Bind(wx.EVT_MENU, self.ZoomToFit, ZoomMenu)
        MenuBar.Append(view_menu, "&View")

        help_menu = wx.Menu()
        AboutMenu = help_menu.Append(wx.ID_ABOUT, "",
                                "More information About this program")
        self.Bind(wx.EVT_MENU, self.OnAbout, AboutMenu)
        MenuBar.Append(help_menu, "&Help")

        self.SetMenuBar(MenuBar)

        self.CreateStatusBar()
        # Add the Canvas
        self.Canvas = NavCanvas.NavCanvas(self,-1,(500,500),
                                          Debug = 0,
                                          BackgroundColor = "DARK SLATE BLUE"
                                          ).Canvas

        wx.EVT_CLOSE(self, self.OnCloseWindow)

        FloatCanvas.EVT_MOTION(self.Canvas, self.OnMove )
        FloatCanvas.EVT_LEFT_UP(self.Canvas, self.OnLeftUp )
        FloatCanvas.EVT_LEFT_DOWN(self.Canvas, self.OnLeftDown)

        try:
            self.FileDialog = wx.FileDialog(self, "Pick a BNA file",".","","*", wx.FD_OPEN)
        except wx._core.PyAssertionError:
            self.FileDialog = None

        self.ResetSelections()
        return None

    def ResetSelections(self):
        self.SelectedPoly = None
        self.SelectedPolyOrig = None
        self.SelectedPoints = None
        self.PointSelected = False
        self.SelectedPointNeighbors = None

    def OnLeftDown(self,event):
        if self.SelectedPoly:
            self.DeSelectPoly()
            self.Canvas.Draw()

    def OnAbout(self, event):
        dlg = wx.MessageDialog(self, "This is a small program to demonstrate\n"
                                                  "the use of the FloatCanvas\n",
                                                  "About Me", wx.OK | wx.ICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()

    def ZoomToFit(self,event):
        self.Canvas.ZoomToBB()

    def OpenBNA(self, event):
        if self.FileDialog is None:
            self.FileDialog = wx.FileDialog(self, "Pick a BNA file",style= wx.OPEN)
        dlg = self.FileDialog
        dlg.SetMessage("Pick a BNA file")
        if dlg.ShowModal() == wx.ID_OK:
            filename = dlg.GetPath()
            self.LoadBNA(filename)

    def SaveBNA(self, event):
        for i in self.ChangedPolys:
            self.BNAFile.PointsData[i] = self.AllPolys[i].Points
        dlg = wx.FileDialog(self,
                               message="Pick a BNA file",
                               style=wx.FD_SAVE)
        if dlg.ShowModal() == wx.ID_OK:
            filename = dlg.GetPath()
            self.BNAFile.Save(filename)

    def Clear(self,event = None):
        self.Canvas.ClearAll()
        self.Canvas.Draw(True)

    def OnQuit(self,event):
        self.Close(True)

    def OnCloseWindow(self, event):
        self.Destroy()

    def OnMove(self, event):
        """
        Updates the status bar with the world coordinates
        And moves a point if there is one

        """
        self.SetStatusText("%.4f, %.4f"%tuple(event.Coords))

        if self.PointSelected:
            PolyPoints = self.SelectedPoly.Points
            Index = self.SelectedPoints.Index
            dc = wx.ClientDC(self.Canvas)
            PixelCoords = event.GetPosition()
            dc.SetPen(wx.Pen('WHITE', 2, wx.SHORT_DASH))
            dc.SetLogicalFunction(wx.XOR)
            if self.SelectedPointNeighbors is None:
                self.SelectedPointNeighbors = N.zeros((3,2), N.float)
                #fixme: This feels very inelegant!
                if Index == 0:
                    self.SelectedPointNeighbors[0] = self.SelectedPoly.Points[-1]
                    self.SelectedPointNeighbors[1:3] = self.SelectedPoly.Points[:2]
                elif Index == len(self.SelectedPoly.Points)-1:
                    self.SelectedPointNeighbors[0:2] = self.SelectedPoly.Points[-2:]
                    self.SelectedPointNeighbors[2] = self.SelectedPoly.Points[0]
                else:
                    self.SelectedPointNeighbors = self.SelectedPoly.Points[Index-1:Index+2]
                self.SelectedPointNeighbors = self.Canvas.WorldToPixel(self.SelectedPointNeighbors)
            else:
                    dc.DrawLines(self.SelectedPointNeighbors)
            self.SelectedPointNeighbors[1] = PixelCoords
            dc.DrawLines(self.SelectedPointNeighbors)

    def OnLeftUp(self, event):
        if self.PointSelected:
            self.SelectedPoly.Points[self.SelectedPoints.Index] = event.GetCoords()
            self.SelectedPoly.SetPoints(self.SelectedPoly.Points, copy = False)
            self.SelectedPoints.SetPoints(self.SelectedPoly.Points, copy = False)
            self.PointSelected = False
            self.SelectedPointNeighbors = None
            self.SelectedPoly.HasChanged = True
            self.Canvas.Draw()

    def DeSelectPoly(self):
        Canvas = self.Canvas
        if self.SelectedPoly.HasChanged:
            self.ChangedPolys.add(self.SelectedPolyOrig.BNAIndex)
            self.SelectedPolyOrig.SetPoints(self.SelectedPoly.Points, copy = False)
            self.Canvas.Draw(Force = True)
        Canvas.RemoveObject(self.SelectedPoly)
        Canvas.RemoveObject(self.SelectedPoints)
        self.ResetSelections()

    def SelectPoly(self, Object):
        Canvas = self.Canvas
        if Object is self.SelectedPolyOrig:
            pass
        else:
            if self.SelectedPoly is not None:
                self.DeSelectPoly()
            self.SelectedPolyOrig = Object
            self.SelectedPoly = Canvas.AddPolygon(Object.Points,
                                                  LineWidth = 1,
                                                  LineColor = "Red",
                                                  FillColor = None,
                                                  InForeground = True)
            self.SelectedPoly.HasChanged = False
            # Draw points on the Vertices of the Selected Poly:
            self.SelectedPoints = Canvas.AddPointSet(Object.Points,
                                                     Diameter = 4,
                                                     Color = "Red",
                                                     InForeground = True)
            self.SelectedPoints.HitLineWidth = 8 # make it a bit easier to hit
            self.SelectedPoints.Bind(FloatCanvas.EVT_FC_LEFT_DOWN, self.SelectPointHit)
            Canvas.Draw()

    def SelectPointHit(self, PointSet):
        PointSet.Index = PointSet.FindClosestPoint(PointSet.HitCoords)
        self.PointSelected = True

    def LoadBNA(self, filename):
        self.ResetSelections()
        self.Canvas.ClearAll()
        self.Canvas.SetProjectionFun('FlatEarth')
        try:
            AllPolys = []
            self.BNAFile  = BNAData(filename)
            print("loaded BNAFile:", self.BNAFile.Filename)
            for i, shoreline in enumerate(self.BNAFile.PointsData):
                Poly = self.Canvas.AddPolygon(shoreline,
                                       LineWidth = 1,
                                       LineColor = "Black",
                                       FillColor = "Brown",
                                       FillStyle = 'Solid')
                Poly.Bind(FloatCanvas.EVT_FC_LEFT_DOWN, self.SelectPoly)
                Poly.BNAIndex = i
                AllPolys.append(Poly)
            self.Canvas.ZoomToBB()
            self.ChangedPolys = sets.Set()
            self.AllPolys = AllPolys
        except:
            #raise
            dlg = wx.MessageDialog(None,
                                   'There was something wrong with the selected bna file',
                                   'File Loading Error',
                                   wx.OK | wx.ICON_ERROR)
            dlg.ShowModal()
            dlg.Destroy()


class BNAEditor(wx.App):
    """
    Once you have a picture drawn, you can zoom in and out and move about
    the picture. There is a tool bar with three tools that can be
    selected.
    """

    def __init__(self, *args, **kwargs):
        wx.App.__init__(self, *args, **kwargs)

    def OnInit(self):
        frame = DrawFrame(None, -1, "BNA Editor",wx.DefaultPosition,(700,700))

        self.SetTopWindow(frame)
        frame.Show()

        if StartFileName:
            frame.LoadBNA(StartFileName)
        else:
            ##frame.LoadBNA("Tests/Small.bna")
            frame.LoadBNA("Tiny.bna")
        return True


app = BNAEditor(False)# put in True if you want output to go to it's own window.
app.MainLoop()























