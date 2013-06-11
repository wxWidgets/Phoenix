# demo/test for group functions
snippet_normalize (cr, width, height)

cr.rectangle (0.1, 0.1, 0.6, 0.6)
cr.set_line_width (0.03)
cr.set_source_rgb (0.8, 0.8, 0.8)
cr.fill()

cr.push_group()
cr.rectangle (0.3, 0.3, 0.6, 0.6)
cr.set_source (cairo.SolidPattern (1, 0, 0))
cr.fill_preserve()
cr.set_source (cairo.SolidPattern (0, 0, 0))
cr.stroke ()
cr.pop_group_to_source()
cr.paint_with_alpha (0.5)
