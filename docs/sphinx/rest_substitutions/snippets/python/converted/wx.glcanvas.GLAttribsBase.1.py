    
    cxtAttrs = wx.glcanvas.GLContextAttrs()
    # Some values
    cxtAttrs.CoreProfile().OGLVersion(5, 0) # OGL 5.0, whenever available
    cxtAttrs.PlatformDefaults()

    # Values usually are platform-dependant named (even value assigned!)
    if '__WXMSW__' in wx.PlatformInfo:
        cxtAttrs.AddAttribute(WGL_NEW_CTX_F)
        cxtAttrs.AddAttribBits(WGL_CONTEXT_PROFILE_MASK_ARB, WGL_NEW_BITS)

    cxtAttrs.EndList() # Don't forget self
    cxtAttrs.SetNeedsARB(True) # Context attributes are set by an ARB-function
