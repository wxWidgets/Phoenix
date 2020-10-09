#!/usr/bin/env python

import os
import sys
from math import pi, sin, cos

import wx

try:
    from wx import glcanvas
    haveGLCanvas = True
except ImportError:
    haveGLCanvas = False

try:
    # The Python OpenGL package can be found at
    # http://PyOpenGL.sourceforge.net/
    from OpenGL.GL import *
    from OpenGL.GLU import *
    haveOpenGL = True
except ImportError:
    haveOpenGL = False


#----------------------------------------------------------------------


buttonDefs = {
    wx.NewIdRef() : ('CubeCanvas', 'Cube'),
    wx.NewIdRef() : ('ConeCanvas', 'Cone'),
    }

class ButtonPanel(wx.Panel):
    def __init__(self, parent, log):
        wx.Panel.__init__(self, parent, wx.ID_ANY)
        self.log = log

        box = wx.BoxSizer(wx.VERTICAL)
        box.Add((20, 30))
        keys = sorted(buttonDefs)
        for k in keys:
            text = buttonDefs[k][1]
            btn = wx.Button(self, k, text)
            box.Add(btn, 0, wx.ALIGN_CENTER | wx.ALL, 15)
            self.Bind(wx.EVT_BUTTON, self.OnButton, btn)

        #** Enable this to show putting a GLCanvas on the wx.Panel .
        if 0:
            c = CubeCanvas(self)
            c.SetSize((200, 200))
            box.Add(c, 0, wx.ALIGN_CENTER | wx.ALL, 15)

        self.SetAutoLayout(True)
        self.SetSizer(box)


    def OnButton(self, evt):
        if not haveGLCanvas:
            dlg = wx.MessageDialog(self,
                                   'The GLCanvas class has not been included with this build of wxPython!',
                                   'Sorry', wx.OK | wx.ICON_WARNING)
            dlg.ShowModal()
            dlg.Destroy()

        elif not haveOpenGL:
            dlg = wx.MessageDialog(self,
                                   'The OpenGL package was not found.  You can get it at\n'
                                   'http://PyOpenGL.sourceforge.net/ \n'
                                   'or $ pip install PyOpenGL PyOpenGL_accelerate',
                                   'Sorry', wx.OK | wx.ICON_WARNING)
            dlg.ShowModal()
            dlg.Destroy()

        else:
            canvasClassName = buttonDefs[evt.GetId()][0]
            canvasClass = eval(canvasClassName)
            frame = wx.Frame(None, wx.ID_ANY, canvasClassName, size=(400, 400))
            canvas = canvasClass(frame)
            frame.Show(True)


class MyCanvasBase(glcanvas.GLCanvas):
    def __init__(self, parent):
        glcanvas.GLCanvas.__init__(self, parent, -1)
        self.init = False
        self.context = glcanvas.GLContext(self)

        # Initial mouse position.
        self.lastx = self.x = 30
        self.lasty = self.y = 30
        self.size = None
        self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground)
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_LEFT_DOWN, self.OnMouseDown)
        self.Bind(wx.EVT_LEFT_UP, self.OnMouseUp)
        self.Bind(wx.EVT_MOTION, self.OnMouseMotion)


    def OnEraseBackground(self, event):
        pass  # Do nothing, to avoid flashing on MSW.

    def OnSize(self, event):
        wx.CallAfter(self.DoSetViewport)
        event.Skip()

    def DoSetViewport(self):
        size = self.size = self.GetClientSize() * self.GetContentScaleFactor()
        self.SetCurrent(self.context)
        glViewport(0, 0, size.width, size.height)

    def OnPaint(self, event):
        dc = wx.PaintDC(self)
        self.SetCurrent(self.context)
        if not self.init:
            self.InitGL()
            self.init = True
        self.OnDraw()

    def OnMouseDown(self, event):
        if self.HasCapture():
            self.ReleaseMouse()
        self.CaptureMouse()
        self.x, self.y = self.lastx, self.lasty = event.GetPosition()

    def OnMouseUp(self, event):
        if self.HasCapture():
            self.ReleaseMouse()

    def OnMouseMotion(self, event):
        if event.Dragging() and event.LeftIsDown():
            self.lastx, self.lasty = self.x, self.y
            self.x, self.y = event.GetPosition()
            self.Refresh(False)


def ReadTexture(filename):
    # Load texture with PIL/PILLOW.  RGBA png seems to load fine with pillow.
    ## with Image.open(filename) as img:
    ##     imgWidth, imgHeight = img.size
    ##     img_data = img.tobytes("raw", "RGB", 0, -1)

    # Load texture with wxPython.
    # Hmmm this seems to be wrong channel order or something for wx.Image
    # with png alpha when using RGBA. Oh well. We will send jpg Robin instead.
    img = wx.Image(filename)
    ## if not img.HasAlpha():
    ##     img.InitAlpha()
    imgWidth, imgHeight = img.GetSize()
    img_data = bytes(img.GetData())
    return (imgWidth, imgHeight, img_data)

def GenerateTexture(imgWidth, imgHeight, img_data):
    textureID = glGenTextures(1)
    glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
    glBindTexture(GL_TEXTURE_2D, textureID)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_R, GL_CLAMP_TO_EDGE)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)

    # https://www.khronos.org/registry/OpenGL-Refpages/gl4/html/glTexImage2D.xhtml
    target = GL_TEXTURE_2D
    level = 0
    internalformat = GL_RGB  # GL_RGBA
    width = imgWidth
    height = imgHeight
    border = 0
    format =  GL_RGB  # GL_RGBA
    type = GL_UNSIGNED_BYTE
    data = img_data
    glTexImage2D(target, level, internalformat, width, height, border, format, type, data)
    # https://www.khronos.org/registry/OpenGL-Refpages/gl2.1/xhtml/glTexEnv.xml
    target = GL_TEXTURE_ENV
    pname = GL_TEXTURE_ENV_MODE
    params = GL_MODULATE
    glTexEnvf(target, pname, params)
    return textureID


class CubeCanvas(MyCanvasBase):
    def InitGL(self):
        # Set viewing projection.
        glMatrixMode(GL_PROJECTION)
        glFrustum(-0.5, 0.5, -0.5, 0.5, 1.0, 3.0)

        # Position viewer.
        glMatrixMode(GL_MODELVIEW)
        glTranslatef(0.0, 0.0, -2.0)

        # Position object.
        glRotatef(self.y, 1.0, 0.0, 0.0)
        glRotatef(self.x, 0.0, 1.0, 0.0)

        glEnable(GL_DEPTH_TEST)
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)

        self.textureID = None
        path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'bmp_source'))
        rd = 'robin.jpg'
        if os.path.exists(os.path.join(path, rd)):
            self.textureID = GenerateTexture(*ReadTexture(os.path.join(path, rd)))


    def OnDraw(self):
        # Clear color and depth buffers.
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Draw six faces of a cube.
        glBegin(GL_QUADS)
        ## glNormal3f( 0.0, 0.0, 1.0)
        ## glVertex3f( 0.5, 0.5, 0.5)
        ## glVertex3f(-0.5, 0.5, 0.5)
        ## glVertex3f(-0.5,-0.5, 0.5)
        ## glVertex3f( 0.5,-0.5, 0.5)

        glNormal3f( 0.0, 0.0,-1.0)
        glVertex3f(-0.5,-0.5,-0.5)
        glVertex3f(-0.5, 0.5,-0.5)
        glVertex3f( 0.5, 0.5,-0.5)
        glVertex3f( 0.5,-0.5,-0.5)

        glNormal3f( 0.0, 1.0, 0.0)
        glVertex3f( 0.5, 0.5, 0.5)
        glVertex3f( 0.5, 0.5,-0.5)
        glVertex3f(-0.5, 0.5,-0.5)
        glVertex3f(-0.5, 0.5, 0.5)

        glNormal3f( 0.0,-1.0, 0.0)
        glVertex3f(-0.5,-0.5,-0.5)
        glVertex3f( 0.5,-0.5,-0.5)
        glVertex3f( 0.5,-0.5, 0.5)
        glVertex3f(-0.5,-0.5, 0.5)

        glNormal3f( 1.0, 0.0, 0.0)
        glVertex3f( 0.5, 0.5, 0.5)
        glVertex3f( 0.5,-0.5, 0.5)
        glVertex3f( 0.5,-0.5,-0.5)
        glVertex3f( 0.5, 0.5,-0.5)

        glNormal3f(-1.0, 0.0, 0.0)
        glVertex3f(-0.5,-0.5,-0.5)
        glVertex3f(-0.5,-0.5, 0.5)
        glVertex3f(-0.5, 0.5, 0.5)
        glVertex3f(-0.5, 0.5,-0.5)
        glEnd()

        if self.textureID:
            glEnable(GL_TEXTURE_2D)
            ## glBindTexture(GL_TEXTURE_2D, self.textureID)
            glBegin(GL_QUADS)
            glNormal3f( 0.0, 0.0, 1.0)
            glTexCoord2f(0.0, 0.0)
            glVertex3fv((0.5, 0.5, 0.5))
            glTexCoord2f(1.0, 0.0)
            glVertex3fv((-0.5, 0.5, 0.5))
            glTexCoord2f(1.0, 1.0)
            glVertex3fv((-0.5,-0.5, 0.5))
            glTexCoord2f(0.0, 1.0)
            glVertex3fv((0.5,-0.5, 0.5))
            glEnd()

        if self.size is None:
            self.size = self.GetClientSize()
        w, h = self.size
        w = max(w, 1.0)
        h = max(h, 1.0)
        xScale = 180.0 / w
        yScale = 180.0 / h
        glRotatef((self.y - self.lasty) * yScale, 1.0, 0.0, 0.0);
        glRotatef((self.x - self.lastx) * xScale, 0.0, 1.0, 0.0);

        self.SwapBuffers()


class ConeCanvas(MyCanvasBase):
    def InitGL( self ):
        glMatrixMode(GL_PROJECTION)
        # Camera frustrum setup.
        glFrustum(-0.5, 0.5, -0.5, 0.5, 1.0, 3.0)
        glMaterial(GL_FRONT, GL_AMBIENT, [0.2, 0.2, 0.2, 1.0])
        glMaterial(GL_FRONT, GL_DIFFUSE, [0.8, 0.8, 0.8, 1.0])
        glMaterial(GL_FRONT, GL_SPECULAR, [1.0, 0.0, 1.0, 1.0])
        glMaterial(GL_FRONT, GL_SHININESS, 50.0)
        glLight(GL_LIGHT0, GL_AMBIENT, [0.0, 1.0, 0.0, 1.0])
        glLight(GL_LIGHT0, GL_DIFFUSE, [1.0, 1.0, 1.0, 1.0])
        glLight(GL_LIGHT0, GL_SPECULAR, [1.0, 1.0, 1.0, 1.0])
        glLight(GL_LIGHT0, GL_POSITION, [1.0, 1.0, 1.0, 0.0])
        glLightModelfv(GL_LIGHT_MODEL_AMBIENT, [0.2, 0.2, 0.2, 1.0])
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glDepthFunc(GL_LESS)
        glEnable(GL_DEPTH_TEST)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        # Position viewer.
        glMatrixMode(GL_MODELVIEW)
        # Position viewer.
        glTranslatef(0.0, 0.0, -2.0);


    def OnDraw(self):
        # Clear color and depth buffers.
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        # Use a fresh transformation matrix.
        glPushMatrix()
        # Position object.
        ## glTranslate(0.0, 0.0, -2.0)
        glRotate(30.0, 1.0, 0.0, 0.0)
        glRotate(30.0, 0.0, 1.0, 0.0)

        glTranslate(0, -1, 0)
        glRotate(250, 1, 0, 0)

        glEnable(GL_BLEND)
        glEnable(GL_POLYGON_SMOOTH)
        glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, (0.5, 0.5, 1.0, 0.5))
        glMaterialf(GL_FRONT_AND_BACK, GL_SHININESS, 1.0)
        glShadeModel(GL_FLAT)
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        # glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

        quad = gluNewQuadric()
        base = .5
        top = 0.0
        height = 1.0
        slices = 16
        stacks = 16
        # stacks = 0
        if stacks:
            # This is the premade way to make a cone.
            gluCylinder(quad, base, top, height, slices, stacks)
        else:
            # Draw cone open ended without glu.
            tau = pi * 2
            glBegin(GL_TRIANGLE_FAN)
            centerX, centerY, centerZ = 0.0, 0.0, height
            glVertex3f(centerX, centerY, centerZ)  # Center of circle.
            centerX, centerY, centerZ = 0.0, 0.0, 0.0
            for i in range(slices + 1):
                theta = tau * float(i) / float(slices)  # Get the current angle.
                x = base * cos(theta)  # Calculate the x component.
                y = base * sin(theta)  # Calculate the y component.
                glVertex3f(x + centerX, y + centerY, centerZ)  # Output vertex.
            glEnd()

        glPopMatrix()
        glRotatef((self.y - self.lasty), 0.0, 0.0, 1.0);
        glRotatef((self.x - self.lastx), 1.0, 0.0, 0.0);
        # Push into visible buffer.
        self.SwapBuffers()


#----------------------------------------------------------------------


def runTest(frame, nb, log):
    win = ButtonPanel(nb, log)
    return win


overview = """\
"""


if __name__ == '__main__':
    import sys,os
    import run
    run.main(['', os.path.basename(sys.argv[0])] + sys.argv[1:])

