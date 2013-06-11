snippet_normalize (cr, width, height)
cr.set_line_width (0.12)
cr.set_line_cap  (cairo.LINE_CAP_BUTT) #/* default */
cr.move_to (0.25, 0.2); cr.line_to (0.25, 0.8)
cr.stroke ()
cr.set_line_cap  (cairo.LINE_CAP_ROUND)
cr.move_to (0.5, 0.2); cr.line_to (0.5, 0.8)
cr.stroke ()
cr.set_line_cap  (cairo.LINE_CAP_SQUARE)
cr.move_to (0.75, 0.2); cr.line_to (0.75, 0.8)
cr.stroke ()

#/* draw helping lines */
cr.set_source_rgb (1,0.2,0.2)
cr.set_line_width (0.01)
cr.move_to (0.25, 0.2); cr.line_to (0.25, 0.8)
cr.move_to (0.5, 0.2);  cr.line_to (0.5, 0.8)
cr.move_to (0.75, 0.2); cr.line_to (0.75, 0.8)
cr.stroke ()
