#include <stddef.h>
#ifdef __WXMSW__
#include <wx/msw/private.h>
#endif

#ifdef __WXGTK__
#include <gdk/gdkx.h>
#include <gtk/gtk.h>
#ifdef __WXGTK3__
// Unlike GDK_WINDOW_XWINDOW, GDK_WINDOW_XID can't handle a NULL, so check 1st
static XID GetXWindow(const wxWindow* wxwin) {
    if ((wxwin)->m_wxwindow) {
        if (gtk_widget_get_window((wxwin)->m_wxwindow))
            return GDK_WINDOW_XID(gtk_widget_get_window((wxwin)->m_wxwindow));
        return 0;
    }
    else {
        if (gtk_widget_get_window((wxwin)->m_widget))
            return GDK_WINDOW_XID(gtk_widget_get_window((wxwin)->m_widget));
        return 0;
    }
}
#else
#define GetXWindow(wxwin) (wxwin)->m_wxwindow ? \
                          GDK_WINDOW_XWINDOW((wxwin)->m_wxwindow->window) : \
                          GDK_WINDOW_XWINDOW((wxwin)->m_widget->window)
#endif
#endif





wxUIntPtr wxPyGetWinHandle(const wxWindow* win)
{
#ifdef __WXMSW__
    return (wxUIntPtr)win->GetHandle();
#endif
#if defined(__WXGTK__) || defined(__WXX11__)
    return (wxUIntPtr)GetXWindow(win);
#endif
#ifdef __WXMAC__
    return (wxUIntPtr)win->GetHandle();
#endif
    return 0;
}


enum NativeHandleType {
    HANDLE_TYPE_UNKNOWN,
    HANDLE_TYPE_XID,
    HANDLE_TYPE_WL_SURFACE,
    HANDLE_TYPE_NSWINDOW,
    HANDLE_TYPE_HWND,
};


#ifdef __WXGTK__
// *lots* of preprocessor junk throughout the GTK code, to handle different GTK
// backends en/disabled at compile-time.
//
// gdkconfig.h lists the possible GDK_WINDOWING_FOO #defines. the only one
// being skipped here is "Broadway" which is HTML/webassembly.
#ifdef GDK_WINDOWING_X11
#include <gdk/gdkx.h>
#endif
#ifdef GDK_WINDOWING_WAYLAND
#include <gdk/gdkwayland.h>
#endif
#ifdef GDK_WINDOWING_WIN32
#include <gdk/gdkwin32.h>
#endif
#ifdef GDK_WINDOWING_QUARTZ
#include <gdk/gdkquartz.h>
#endif

static GdkWindow * get_gdk_window(const wxWindow *win) {
    GtkWidget *gtk = win->GetHandle();
    if (!gtk) {
        return NULL;
    }
    // confusing: on X (and maybe others), every widget is a window, and the
    // GDK window will be the widget-window instead of the real toplevel
    // window. solution: passing through gtk_widget_get_toplevel. it
    // is...weirdly defined. the docs say to check the return value right away
    // with GTK_IS_WINDOW.
    GtkWidget *toplevel = gtk_widget_get_toplevel(gtk);
    if (!GTK_IS_WINDOW(toplevel)) {
        return NULL;
    }
    return gtk_widget_get_window(toplevel);
}

static int get_gtk_handle_type(const wxWindow *win) {
    GdkWindow *gdkwin = get_gdk_window(win);
    if (!gdkwin) {
        return HANDLE_TYPE_UNKNOWN;
    }
#ifdef GDK_WINDOWING_X11
    if (GDK_IS_X11_WINDOW(gdkwin)) {
        return HANDLE_TYPE_XID;
    }
#endif
#ifdef GDK_WINDOWING_WAYLAND
    if (GDK_IS_WAYLAND_WINDOW(gdkwin)) {
        return HANDLE_TYPE_WL_SURFACE;
    }
#endif
#ifdef GDK_WINDOWING_WIN32
    if (GDK_IS_WIN32_WINDOW(gdkwin)) {
        return HANDLE_TYPE_HWND;
    }
#endif
#ifdef GDK_WINDOWING_QUARTZ
    if (GDK_IS_QUARTZ_WINDOW(gdkwin)) {
        return HANDLE_TYPE_NSWINDOW;
    }
#endif
    return HANDLE_TYPE_UNKNOWN;
}

static void * get_gtk_handle(const wxWindow *win) {
    GdkWindow *gdkwin = get_gdk_window(win);
    if (!gdkwin) {
        return NULL;
    }
#ifdef GDK_WINDOWING_X11
    if (GDK_IS_X11_WINDOW(gdkwin)) {
        return (void *)gdk_x11_window_get_xid(gdkwin);
    }
#endif
#ifdef GDK_WINDOWING_WAYLAND
    if (GDK_IS_WAYLAND_WINDOW(gdkwin)) {
        return gdk_wayland_window_get_wl_surface(gdkwin);
    }
#endif
#ifdef GDK_WINDOWING_WIN32
    if (GDK_IS_WIN32_WINDOW(gdkwin)) {
        return gdk_win32_window_get_handle(gdkwin);
    }
#endif
#ifdef GDK_WINDOWING_QUARTZ
    if (GDK_IS_QUARTZ_WINDOW(gdkwin)) {
        return gdk_quartz_window_get_nswindow(gdkwin);
    }
#endif
    return NULL;
}
#endif // ifdef __WXGTK__

// All the possible __WXFOO__ port #defines are documented at:
// <https://docs.wxwidgets.org/latest/page_cppconst.html#page_cppconst_guisystem>

int wxPyNativeWindowHandleType(const wxWindow *win)
{
#ifdef __WXGTK__
    return get_gtk_handle_type(win);
#endif
#ifdef __WXX11__
    return HANDLE_TYPE_XID;
#endif
#ifdef __WXOSX_COCOA__
    return HANDLE_TYPE_NSWINDOW;
#endif
#ifdef __WXMSW__
    return HANDLE_TYPE_HWND;
#endif
    return HANDLE_TYPE_UNKNOWN;
}

const char * wxPyNativeWindowHandleTypeString(const wxWindow *win)
{
    switch (wxPyNativeWindowHandleType(win)) {
        case HANDLE_TYPE_XID:
            return "XID";
        case HANDLE_TYPE_WL_SURFACE:
            return "wl_surface";
        case HANDLE_TYPE_NSWINDOW:
            return "NSWindow";
        case HANDLE_TYPE_HWND:
            return "HWND";
        default:
            return "";
    }
}

#ifdef __WXOSX_COCOA__
#include <objc/objc-runtime.h>
#endif
void * wxPyNativeWindowHandle(const wxWindow *win)
{
#ifdef __WXGTK__
    return get_gtk_handle(win);
#endif
#if defined(__WXMSW__) || defined(__WXX11__)
    // TODO possibly wrong. hard to confirm.
    return win->GetHandle();
#endif
#ifdef __WXOSX_COCOA__
    id nsview = (id) win->GetHandle();
    // experimentally confirmed it's an NSView via libobjc's
    // object_getClassName.
    SEL window_sel = sel_registerName("window");
    if (!window_sel) {
        return NULL;
    }
    id (*invoke)(id, SEL) = (id (*)(id, SEL)) objc_msgSend;
    id nswindow = invoke(nsview, window_sel);
    if (!nswindow) {
        return NULL;
    }
    return nswindow;
#endif

    return NULL;
}
