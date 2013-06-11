snippet_normalize (cr, width, height)
cr.set_line_width (0.16)
cr.move_to (0.3, 0.33)
cr.rel_line_to (0.2, -0.2)
cr.rel_line_to (0.2, 0.2)
cr.set_line_join (cairo.LINE_JOIN_MITER) #/* default */
cr.stroke ()

cr.move_to (0.3, 0.63)
cr.rel_line_to (0.2, -0.2)
cr.rel_line_to (0.2, 0.2)
cr.set_line_join (cairo.LINE_JOIN_BEVEL)
cr.stroke ()

cr.move_to (0.3, 0.93)
cr.rel_line_to (0.2, -0.2)
cr.rel_line_to (0.2, 0.2)
cr.set_line_join (cairo.LINE_JOIN_ROUND)
cr.stroke ()


