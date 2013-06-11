snippet_normalize (cr, width, height)
cr.select_font_face ("Sans", cairo.FONT_SLANT_NORMAL,
                     cairo.FONT_WEIGHT_BOLD)
cr.set_font_size (0.35)

cr.move_to (0.04, 0.53)
cr.show_text ("Hello")

cr.move_to (0.27, 0.65)
cr.text_path ("void")
cr.set_source_rgb (0.5,0.5,1)
cr.fill_preserve ()
cr.set_source_rgb (0,0,0)
cr.set_line_width (0.01)
cr.stroke ()

#/* draw helping lines */
cr.set_source_rgba (1,0.2,0.2, 0.6)
cr.arc (0.04, 0.53, 0.02, 0, 2*M_PI)
cr.arc (0.27, 0.65, 0.02, 0, 2*M_PI)
cr.fill ()

