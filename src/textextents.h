//--------------------------------------------------------------------------
// Name:        src/textextents.h
// Purpose:     Make the GetPartialTextExtents results match Python string
//              indexing
//
// Licence:     wxWindows license
//--------------------------------------------------------------------------

#ifndef TEXTEXTENTS_H
#define TEXTEXTENTS_H

// When wxString holds UTF-16 (Windows) the widths array has an entry for each
// half of a surrogate pair, but Python counts the pair as one character. The
// entry for the low surrogate covers the whole character, so drop the other.
template <typename Char, typename Array>
void wxPyMergeSurrogateExtents(const Char* text, size_t len, Array& widths)
{
    if (widths.size() != len)
        return;

    size_t out = 0;
    for (size_t i = 0; i < len; ++i) {
        if ((text[i] & 0xFC00) == 0xD800 && i + 1 < len &&
                (text[i + 1] & 0xFC00) == 0xDC00)
            continue;
        widths[out++] = widths[i];
    }
    if (out < len)
        widths.RemoveAt(out, len - out);
}

template <typename Array>
void wxPyFixPartialExtents(const wxString& text, Array& widths)
{
#if wxUSE_UNICODE_UTF16
    wxPyMergeSurrogateExtents(text.wc_str(), text.length(), widths);
#else
    wxUnusedVar(text);
    wxUnusedVar(widths);
#endif
}

#endif
