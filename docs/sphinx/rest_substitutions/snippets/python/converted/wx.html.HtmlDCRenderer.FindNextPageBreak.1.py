
    pages = []
    while pos != wx.NOT_FOUND:
        pos = renderer.FindNextPageBreak(pos)
        pages.append(pos)

    # "pages" now contains all page break positions and, in
    # particular, its size is the number of pages
