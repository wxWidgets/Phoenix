import unittest
from unittests import wtc
import wx

#---------------------------------------------------------------------------

class platinfo_Tests(wtc.WidgetTestCase):

    def test_platinfo(self):
        pi = wx.PlatformInformation.Get()

        pi.GetArchitecture()
        pi.GetOperatingSystemId()
        pi.GetPortId()



    def test_platinfoProperties(self):
        pi = wx.PlatformInformation.Get()
        pi.ArchName
        pi.Architecture
        pi.DesktopEnvironment
        pi.Endianness
        pi.EndiannessName
        pi.LinuxDistributionInfo
        pi.OSMajorVersion
        pi.OSMinorVersion
        pi.OperatingSystemDescription
        pi.OperatingSystemFamilyName
        pi.OperatingSystemId
        pi.OperatingSystemIdName
        pi.PortId
        pi.PortIdName
        pi.PortIdShortName
        pi.ToolkitMajorVersion
        pi.ToolkitMinorVersion


    def test_platinfoFlags(self):
        wx.OS_UNKNOWN
        wx.OS_MAC_OS
        wx.OS_MAC_OSX_DARWIN
        wx.OS_MAC
        wx.OS_WINDOWS_9X
        wx.OS_WINDOWS_NT
        wx.OS_WINDOWS_MICRO
        wx.OS_WINDOWS_CE
        wx.OS_WINDOWS
        wx.OS_UNIX_LINUX
        wx.OS_UNIX_FREEBSD
        wx.OS_UNIX_OPENBSD
        wx.OS_UNIX_NETBSD
        wx.OS_UNIX_SOLARIS
        wx.OS_UNIX_AIX
        wx.OS_UNIX_HPUX
        wx.OS_UNIX
        wx.OS_DOS
        wx.OS_OS2

        wx.PORT_UNKNOWN
        wx.PORT_BASE
        wx.PORT_MSW
        wx.PORT_MOTIF
        wx.PORT_GTK
        wx.PORT_X11
        wx.PORT_OS2
        wx.PORT_MAC
        wx.PORT_COCOA
        wx.PORT_WINCE
        wx.PORT_DFB

        wx.ARCH_INVALID
        wx.ARCH_32
        wx.ARCH_64
        wx.ARCH_MAX

        wx.ENDIAN_INVALID
        wx.ENDIAN_BIG
        wx.ENDIAN_LITTLE
        wx.ENDIAN_PDP
        wx.ENDIAN_MAX

#---------------------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()
