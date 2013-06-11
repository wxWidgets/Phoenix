x,  y  = 0.1, 0.5
x1, y1 = 0.4, 0.9
x2, y2 = 0.6, 0.1
x3, y3 = 0.9, 0.5

snippet_normalize (cr, width, height)

cr.move_to (x, y)
cr.curve_to (x1, y1, x2, y2, x3, y3)

cr.stroke ()

cr.set_source_rgba (1,0.2,0.2,0.6)
cr.set_line_width (0.03)
cr.move_to (x,y);   cr.line_to (x1,y1)
cr.move_to (x2,y2); cr.line_to (x3,y3)
cr.stroke ()
