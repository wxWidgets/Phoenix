snippet_normalize (cr, width, height)

cr.select_font_face ("Sans", cairo.FONT_SLANT_NORMAL,
                     cairo.FONT_WEIGHT_NORMAL)
# draw 0.16 glyphs in 0.20 squares, at (0.02, 0.04) from left corner
cr.set_font_size (0.16)

glyphs = []
index = 20
for y in range(5):
    for x in range(5):
        glyphs.append ((index, x/5.0 + 0.02, y/5.0 + 0.16))
        index += 1

cr.glyph_path (glyphs)
cr.set_source_rgb (0.5,0.5,1.0)
cr.fill_preserve ()
cr.set_source_rgb (0,0,0)
cr.set_line_width (0.005)
cr.stroke ()

