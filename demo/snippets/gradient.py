snippet_normalize (cr, width, height)

pat = cairo.LinearGradient (0.0, 0.0,  0.0, 1.0)
pat.add_color_stop_rgba (1, 0, 0, 0, 1)
pat.add_color_stop_rgba (0, 1, 1, 1, 1)
cr.rectangle (0,0,1,1)
cr.set_source (pat)
cr.fill ()

pat = cairo.RadialGradient (0.45, 0.4, 0.1,
                            0.4,  0.4, 0.5)
pat.add_color_stop_rgba (0, 1, 1, 1, 1)
pat.add_color_stop_rgba (1, 0, 0, 0, 1)
cr.set_source (pat)
cr.arc (0.5, 0.5, 0.3, 0, 2 * M_PI)
cr.fill ()
