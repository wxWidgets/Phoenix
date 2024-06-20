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


void * wxPyNativeWindowHandle(const wxWindow *win)
{
    return NULL;
}

enum NativeHandleType {
    HANDLE_TYPE_UNKNOWN,
};

int wxPyNativeWindowHandleType(const wxWindow *win)
{
    return HANDLE_TYPE_UNKNOWN;
}

const char * wxPyNativeWindowHandleTypeString(const wxWindow *win)
{
    switch (wxPyNativeWindowHandleType(win)) {
        default:
            return "";
    }
}
