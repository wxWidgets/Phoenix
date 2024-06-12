#ifdef __WXGTK__
#include <gdk/gdk.h>
#include <gtk/gtk.h>

// GDK3 gdkconfig.h lists the possible window backend #defines.
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

#endif // ifdef __WXGTK__




wxUIntPtr wxPyGetWinHandle(const wxWindow* win)
{
#ifdef __WXMSW__
    return (wxUIntPtr)win->GetHandle();
#endif

#ifdef __WXX11__
    return (wxUIntPtr)win->GetHandle();
#endif

#ifdef __WXMAC__
    return (wxUIntPtr)win->GetHandle();
#endif

#ifdef __WXGTK__
    GtkWidget *gtk_widget = win->GetHandle();
    if (!gtk_widget) {
        return 0;
    };
    // gtk_widget_get_window disappears in GTK4; then it will be via
    // gtk_widget_get_native() -> gtk_native_get_surface().
    GdkWindow *window = gtk_widget_get_window(gtk_widget);
    if (!window) {
        return 0;
    }
#ifdef GDK_WINDOWING_X11
    if (GDK_IS_X11_WINDOW(window)) {
        return (wxUIntPtr)gdk_x11_window_get_xid(window);
    }
#endif
#ifdef GDK_WINDOWING_WAYLAND
    if (GDK_IS_WAYLAND_WINDOW(window)) {
        return (wxUIntPtr)gdk_wayland_window_get_wl_surface(window);
    }
#endif
#ifdef GDK_WINDOWING_WIN32
    if (GDK_IS_WIN32_WINDOW(window)) {
        return (wxUIntPtr)gdk_win32_window_get_handle(window);
    }
#endif
#ifdef GDK_WINDOWING_QUARTZ
    if (GDK_IS_QUARTZ_WINDOW(window)) {
        return (wxUIntPtr)gdk_quartz_window_get_nswindow(window);
    }
#endif
#endif

    return 0;
}
