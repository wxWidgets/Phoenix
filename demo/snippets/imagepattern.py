import math

snippet_normalize (cr, width, height)

image = cairo.ImageSurface.create_from_png ("data/romedalen.png")
w = image.get_width()
h = image.get_height()

pattern = cairo.SurfacePattern (image)
pattern.set_extend (cairo.EXTEND_REPEAT)

cr.translate (0.5, 0.5)
cr.rotate (M_PI / 4)
cr.scale (1 / math.sqrt (2), 1 / math.sqrt (2))
cr.translate (- 0.5, - 0.5)

matrix = cairo.Matrix(xx=w * 5, yy=h * 5)
pattern.set_matrix (matrix)

cr.set_source (pattern)

cr.rectangle (0, 0, 1.0, 1.0)
cr.fill ()
