utf8 = "cairo"

snippet_normalize (cr, width, height)

cr.select_font_face ("Sans",
                     cairo.FONT_SLANT_NORMAL,
                     cairo.FONT_WEIGHT_NORMAL)

cr.set_font_size (0.2)
x_bearing, y_bearing, width, height, x_advance, y_advance = cr.text_extents (utf8)
x = 0.5-(width/2 + x_bearing)
y = 0.5-(height/2 + y_bearing)

cr.move_to (x, y)
cr.show_text (utf8)

#/* draw helping lines */
cr.set_source_rgba (1,0.2,0.2,0.6)
cr.arc (x, y, 0.05, 0, 2*M_PI)
cr.fill ()
cr.move_to (0.5, 0)
cr.rel_line_to (0, 1)
cr.move_to (0, 0.5)
cr.rel_line_to (1, 0)
cr.stroke ()

