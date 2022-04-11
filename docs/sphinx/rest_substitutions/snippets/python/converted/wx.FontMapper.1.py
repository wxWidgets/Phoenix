
    if not wx.FontMapper.Get().IsEncodingAvailable(enc, facename):
        success, alt = wx.FontMapper.Get().GetAltForEncoding(enc, facename, False)
        if success:
            convFrom = wx.FontMapper.Get().GetEncodingName(enc)
            convTo   = wx.FontMapper.Get().GetEncodingName(alt)
            text = text.decode(convFrom).encode(convTo)

        else:
            # ...failure (or we may try iso8859-1/7bit ASCII)...
            pass

    # ...display text...
