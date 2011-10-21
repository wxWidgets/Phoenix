#---------------------------------------------------------------------------
# Name:        etg/image.py
# Author:      Kevin Ollivier
#              Robin Dunn
#
# Created:     25-Aug-2011
# Copyright:   (c) 2011 by Wide Open Technologies
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools

PACKAGE   = "wx"
MODULE    = "_core"
NAME      = "image"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script. 
ITEMS  = [ 'wxImage', 
           'wxImageHistogram',
           #'wxImageHandler',  # TODO
           ]    

#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)
    
    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.

    c = module.find('wxImage')
    assert isinstance(c, etgtools.ClassDef)
    c.find('wxImage').findOverload('(const char *const *xpmData)').ignore()

    c.find('GetHandlers').ignore()
    c.find('AddHandler').ignore()
    c.find('InsertHandler').ignore()
    c.find('RemoveHandler').ignore()
    for m in c.find('FindHandler').all():
        m.ignore()
    c.find('FindHandlerMime').ignore()
    
    
    # TODO: Port the ctors and methods that deal with data buffers for getting
    # and setting the image and alpha data.
    
      
    def setParamsPyInt(name):
        """Set the pyInt flag on 'unsigned char' params"""
        method = c.find(name)
        for m in [method] + method.overloads:
            for p in m.items:
                if p.type == 'unsigned char':
                    p.pyInt = True
                
    setParamsPyInt('Replace')
    setParamsPyInt('ConvertAlphaToMask')
    setParamsPyInt('ConvertToMono')
    setParamsPyInt('ConvertToDisabled')
    setParamsPyInt('IsTransparent')
    setParamsPyInt('SetAlpha')
    setParamsPyInt('SetMaskColour')
    setParamsPyInt('SetMaskFromImage')
    setParamsPyInt('SetRGB')

    c.find('FindFirstUnusedColour').type = 'void'
    c.find('FindFirstUnusedColour.r').pyInt = True
    c.find('FindFirstUnusedColour.g').pyInt = True
    c.find('FindFirstUnusedColour.b').pyInt = True
    c.find('FindFirstUnusedColour.startR').pyInt = True
    c.find('FindFirstUnusedColour.startG').pyInt = True
    c.find('FindFirstUnusedColour.startB').pyInt = True
    c.find('FindFirstUnusedColour.r').out = True
    c.find('FindFirstUnusedColour.g').out = True
    c.find('FindFirstUnusedColour.b').out = True
    
    c.find('GetAlpha').findOverload('int x, int y').pyInt = True
    c.find('GetRed').pyInt = True
    c.find('GetGreen').pyInt = True
    c.find('GetBlue').pyInt = True
    c.find('GetMaskRed').pyInt = True
    c.find('GetMaskGreen').pyInt = True
    c.find('GetMaskBlue').pyInt = True
    
    c.find('GetOrFindMaskColour').type = 'void'
    c.find('GetOrFindMaskColour.r').pyInt = True
    c.find('GetOrFindMaskColour.g').pyInt = True
    c.find('GetOrFindMaskColour.b').pyInt = True
    c.find('GetOrFindMaskColour.r').out = True
    c.find('GetOrFindMaskColour.g').out = True
    c.find('GetOrFindMaskColour.b').out = True
    
    c.find('RGBValue.red').pyInt = True
    c.find('RGBValue.green').pyInt = True
    c.find('RGBValue.blue').pyInt = True
    c.find('RGBValue.RGBValue.r').pyInt = True
    c.find('RGBValue.RGBValue.g').pyInt = True
    c.find('RGBValue.RGBValue.b').pyInt = True
   
   
    c.addCppMethod('int', '__nonzero__', '()', 'return self->IsOk();')

    c.addPyMethod('ConvertToBitmap', '(self, depth=-1)', 
        doc="""\
        ConvertToBitmap(depth=-1) -> Bitmap\n
        Convert the image to a wx.Bitmap.""",
        body="""\
        bmp = wx.Bitmap(self, depth)
        return bmp
        """)
    
    c.addPyMethod('ConvertToMonoBitmap', '(self, red, green, blue)', 
        doc="""\
        ConvertToMonoBitmap(red, green, blue) -> Bitmap\n
        Creates a monochrome version of the image and returns it as a wx.Bitmap.""",
        body="""\
        mono = self.ConvertToMono( red, green, blue )
        bmp = wx.Bitmap( mono, 1 )
        return bmp    
        """)
   

    c.addCppMethod('wxImage*', 'AdjustChannels', 
        '(double factor_red, double factor_green, double factor_blue, double factor_alpha=1.0)',
        doc="""\
        This function muliplies all 4 channels (red, green, blue, alpha) with
        a factor (around 1.0). Useful for gamma correction, colour correction
        and to add a certain amount of transparency to a image (fade in fade
        out effects). If factor_alpha is given but the original image has no
        alpha channel then a alpha channel will be added.
        """,
        body="""\
        wxCHECK_MSG( self->Ok(), NULL, wxT("invalid image") );

        wxImage* dest = new wxImage( self->GetWidth(), self->GetHeight(), false );
        wxCHECK_MSG( dest && dest->IsOk(), NULL, wxT("unable to create image") );

        unsigned rgblen =   3 * self->GetWidth() * self->GetHeight();
        unsigned alphalen = self->GetWidth() * self->GetHeight();
        unsigned char* src_data =  self->GetData();
        unsigned char* src_alpha = self->GetAlpha();
        unsigned char* dst_data =  dest->GetData();
        unsigned char* dst_alpha = NULL;

        // adjust rgb
        if ( factor_red == 1.0 && factor_green == 1.0 && factor_blue == 1.0)
        {
            // nothing to do for RGB
            memcpy(dst_data, src_data, rgblen);
        }
        else
        {
            // rgb pixel for pixel
            for ( unsigned i = 0; i < rgblen; i= i + 3 )
            {
                dst_data[i] =     (unsigned char) wxMin( 255, (int) (factor_red * src_data[i]) );
                dst_data[i + 1] = (unsigned char) wxMin( 255, (int) (factor_green * src_data[i + 1]) );
                dst_data[i + 2] = (unsigned char) wxMin( 255, (int) (factor_blue * src_data[i + 2]) );
            }
        }

        // adjust the mask colour
        if ( self->HasMask() )
        {
            dest->SetMaskColour((unsigned char) wxMin( 255, (int) (factor_red * self->GetMaskRed() ) ),
                                (unsigned char) wxMin( 255, (int) (factor_green * self->GetMaskGreen() ) ),
                                (unsigned char) wxMin( 255, (int) (factor_blue * self->GetMaskBlue() ) ) );
        }

        // adjust the alpha channel
        if ( src_alpha )
        {
            // source image already has alpha information
            dest->SetAlpha(); // create an empty alpha channel (not initialized)
            dst_alpha = dest->GetAlpha();

            wxCHECK_MSG( dst_alpha, NULL, wxT("unable to create alpha data") );

            if ( factor_alpha == 1.0)
            {
                // no need to adjust
                memcpy(dst_alpha, src_alpha, alphalen);
            }
            else
            {
                // alpha value for alpha value
                for ( unsigned i = 0; i < alphalen; ++i )
                {
                    dst_alpha[i] = (unsigned char) wxMin( 255, (int) (factor_alpha * src_alpha[i]) );
                }
            }
        }
        else if ( factor_alpha != 1.0 )
        {
            // no alpha yet but we want to adjust -> create
            dest->SetAlpha(); // create an empty alpha channel (not initialized)
            dst_alpha = dest->GetAlpha();
    
            wxCHECK_MSG( dst_alpha, NULL, wxT("unable to create alpha data") );
    
            for ( unsigned i = 0; i < alphalen; ++i )
            {
                dst_alpha[i] = (unsigned char) wxMin( 255, (int) (factor_alpha * 255) );
            }
        }

        // do we have an alpha channel and a mask in the new image?
        if ( dst_alpha && dest->HasMask() )
        {
            // make the mask transparent honoring the alpha channel
            const unsigned char mr = dest->GetMaskRed();
            const unsigned char mg = dest->GetMaskGreen();
            const unsigned char mb = dest->GetMaskBlue();

            for ( unsigned i = 0; i < alphalen; ++i )
            {
                int n = i * 3;
                dst_alpha[i] = ( dst_data[n] == mr && dst_data[n + 1] == mg && dst_data[n + 2] == mb )
                    ? wxIMAGE_ALPHA_TRANSPARENT
                    : dst_alpha[i];
            }

            // remove the mask now
            dest->SetMask(false);
        }

        return dest;""",
        factory=True)
                               
    c.addProperty('Width GetWidth')
    c.addProperty('Height GetHeight')
    c.addProperty('MaskBlue GetMaskBlue')
    c.addProperty('MaskGreen GetMaskGreen')
    c.addProperty('MaskRed GetMaskRed')
    c.addProperty('Type GetType SetType')


    
    #-------------------------------------------------------
    c = module.find('wxImageHistogram')
    setParamsPyInt('MakeKey')
    c.find('FindFirstUnusedColour').type = 'void'
    c.find('FindFirstUnusedColour.r').pyInt = True
    c.find('FindFirstUnusedColour.g').pyInt = True
    c.find('FindFirstUnusedColour.b').pyInt = True
    c.find('FindFirstUnusedColour.startR').pyInt = True
    c.find('FindFirstUnusedColour.startG').pyInt = True
    c.find('FindFirstUnusedColour.startB').pyInt = True
    c.find('FindFirstUnusedColour.r').out = True
    c.find('FindFirstUnusedColour.g').out = True
    c.find('FindFirstUnusedColour.b').out = True
    

    #-------------------------------------------------------

    module.find('wxIMAGE_ALPHA_TRANSPARENT').pyInt = True
    module.find('wxIMAGE_ALPHA_OPAQUE').pyInt = True
    
    # These are defines for string objects, not integers, so we can't generate
    # code for them the same way as integer values. Since they are #defines we
    # can't just tell SIP that they are global wxString objects because it will
    # then end up taking the address of temporary values when it makes the
    # getters for them. So instead we'll just make some python code to add the
    # .py module and hope that the interface file always has the correct
    # values of these options.
    pycode = ""
    for item in module:
        if 'IMAGE_OPTION' in item.name and isinstance(item, etgtools.DefineDef):
            item.ignore()
            name = tools.removeWxPrefix(item.name)
            value = item.value
            for txt in ['wxString(', 'wxT(', ')']:
                value = value.replace(txt, '')
                
            pycode += '%s = %s\n' % (name, value)
    module.addPyCode(pycode)
    
    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)
    
    
#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

