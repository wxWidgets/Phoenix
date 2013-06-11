snippet_normalize(cr, width, height)

dashes = [ 0.10,   # ink
           0.02,   # skip
           0.05,   # ink
           0.02,   # skip
           ]

cr.set_dash(dashes, 0)

cr.move_to(0.5, 0.1)
cr.line_to(0.9, 0.9)
cr.rel_line_to(-0.4, 0.0)
cr.curve_to (0.2, 0.9, 0.2, 0.5, 0.5, 0.5)
cr.close_path()

cr.stroke()

