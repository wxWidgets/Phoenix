snippet_normalize (cr, width, height)

cr.arc (0.5, 0.5, 0.3, 0, 2*M_PI)
cr.clip ()

image = cairo.ImageSurface.create_from_png ("data/romedalen.png")
w = image.get_width()
h = image.get_height()

cr.scale (1.0/w, 1.0/h)

cr.set_source_surface (image, 0, 0)
cr.paint ()
