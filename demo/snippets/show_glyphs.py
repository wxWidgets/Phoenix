snippet_normalize (cr, width, height)

cr.select_font_face ("Sans", cairo.FONT_SLANT_NORMAL,
                     cairo.FONT_WEIGHT_NORMAL)
# draw 0.08 glyphs in 0.10 squares, at (0.01, 0.02) from left corner
cr.set_font_size (0.08)

glyphs = []
index = 0
for y in range(10):
    for x in range(10):
        glyphs.append ((index, x/10.0 + 0.01, y/10.0 + 0.08))
        index += 1

cr.show_glyphs (glyphs)
