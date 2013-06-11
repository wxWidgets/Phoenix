snippet_normalize(cr, width, height)

def path_ellipse(cr, x, y, width, height, angle=0):
    """
    x      - center x
    y      - center y
    width  - width of ellipse  (in x direction when angle=0)
    height - height of ellipse (in y direction when angle=0)
    angle  - angle in radians to rotate, clockwise
    """
    cr.save()
    cr.translate(x, y)
    cr.rotate(angle)
    cr.scale(width / 2.0, height / 2.0)
    cr.arc(0.0, 0.0, 1.0, 0.0, 2.0 * M_PI)
    cr.restore()


path_ellipse(cr, 0.5, 0.5, 1.0, 0.3, M_PI/4.0)

# fill
cr.set_source_rgba(1,0,0,1)
cr.fill_preserve()

# stroke
# reset identity matrix so line_width is a constant
# width in device-space, not user-space
cr.save()
cr.identity_matrix()
cr.set_source_rgba(0,0,0,1)
cr.set_line_width(3)
cr.stroke()
cr.restore()
