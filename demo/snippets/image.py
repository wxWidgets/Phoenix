snippet_normalize (cr, width, height)

image = cairo.ImageSurface.create_from_png ("data/romedalen.png")
w = image.get_width()
h = image.get_height()

cr.translate (0.5, 0.5)
cr.rotate (45* M_PI/180)
cr.scale  (1.0/w, 1.0/h)
cr.translate (-0.5*w, -0.5*h)

cr.set_source_surface (image, 0, 0)
cr.paint ()

