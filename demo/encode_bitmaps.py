#!/usr/bin/env python

"""
This is a way to save the startup time when running img2py on lots of
files...
"""

import sys
from wx.tools import img2py


command_lines = [
    "   -F -i -n Mondrian bmp_source/mondrian.ico images.py",
    "-a -F -n Background bmp_source/backgrnd.png images.py",
    "-a -F -n TestStar -m #FFFFFF bmp_source/teststar.png images.py",
    "-a -F -n TestStar2 bmp_source/teststar.png images.py",
    "-a -F -n TestMask bmp_source/testmask.bmp images.py",

    "-a -F -n Test2 bmp_source/test2.bmp images.py",
    "-a -F -n Test2m -m #0000FF  bmp_source/test2.bmp images.py",
    "-a -F -n Robin bmp_source/robin.jpg images.py",

    "-a -F -n Bulb1 bmp_source/bulb1.bmp images.py",
    "-a -F -n Bulb2 bmp_source/bulb2.bmp images.py",

    "-a -F -n DbDec bmp_source/DbDec.bmp images.py",
    "-a -F -n Dec bmp_source/Dec.bmp images.py",
    "-a -F -n Pt bmp_source/Pt.bmp images.py",
    "-a -F -n DbInc bmp_source/DbInc.bmp images.py",
    "-a -F -n Inc bmp_source/Inc.bmp images.py",

    "-a -F -n Tog1  -m #C0C0C0 bmp_source/tog1.bmp images.py",
    "-a -F -n Tog2  -m #C0C0C0 bmp_source/tog2.bmp images.py",

    "-a -F -n Smiles -m #FFFFFF bmp_source/smiles2.bmp images.py",

    "-a -F -n GridBG bmp_source/GridBG.gif images.py",

    "-a -F -n SmallUpArrow  -m #0000FF bmp_source/sm_up.bmp images.py",
    "-a -F -n SmallDnArrow  -m #0000FF bmp_source/sm_down.bmp images.py",

    "-a -F -n NoIcon  bmp_source/noicon.png  images.py",

    "-a -F -n WizTest1 bmp_source/wiztest1.bmp images.py",
    "-a -F -n WizTest2 bmp_source/wiztest2.bmp images.py",

    "-a -F -n Vippi bmp_source/Vippi.png images.py",

    "-a -F -n LB01 bmp_source/LB01.png images.py",
    "-a -F -n LB02 bmp_source/LB02.png images.py",
    "-a -F -n LB03 bmp_source/LB03.png images.py",
    "-a -F -n LB04 bmp_source/LB04.png images.py",
    "-a -F -n LB05 bmp_source/LB05.png images.py",
    "-a -F -n LB06 bmp_source/LB06.png images.py",
    "-a -F -n LB07 bmp_source/LB07.png images.py",
    "-a -F -n LB08 bmp_source/LB08.png images.py",
    "-a -F -n LB09 bmp_source/LB09.png images.py",
    "-a -F -n LB10 bmp_source/LB10.png images.py",
    "-a -F -n LB11 bmp_source/LB11.png images.py",
    "-a -F -n LB12 bmp_source/LB12.png images.py",

    "-a -F -n FloatCanvas bmp_source/floatcanvas.png images.py",
    "-a -F -n TheKid bmp_source/thekid.png images.py",

    "-a -F -n Carrot bmp_source/carrot.png images.py",
    "-a -F -n Pointy bmp_source/pointy.png images.py",
    "-a -F -n Pencil bmp_source/pencil.png images.py",

    "-a -F -i -n WXPdemo bmp_source/wxpdemo.ico images.py",

    "-a -F -n _rt_alignleft bmp_source/rt_alignleft.xpm images.py",
    "-a -F -n _rt_alignright bmp_source/rt_alignright.xpm images.py",
    "-a -F -n _rt_bold bmp_source/rt_bold.xpm images.py",
    "-a -F -n _rt_centre bmp_source/rt_centre.xpm images.py",
    "-a -F -n _rt_colour bmp_source/rt_colour.xpm images.py",
    "-a -F -n _rt_copy bmp_source/rt_copy.xpm images.py",
    "-a -F -n _rt_cut bmp_source/rt_cut.xpm images.py",
    "-a -F -n _rt_font bmp_source/rt_font.xpm images.py",
    "-a -F -n _rt_idea bmp_source/rt_idea.xpm images.py",
    "-a -F -n _rt_indentless bmp_source/rt_indentless.xpm images.py",
    "-a -F -n _rt_indentmore bmp_source/rt_indentmore.xpm images.py",
    "-a -F -n _rt_italic bmp_source/rt_italic.xpm images.py",
    "-a -F -n _rt_open bmp_source/rt_open.xpm images.py",
    "-a -F -n _rt_paste bmp_source/rt_paste.xpm images.py",
    "-a -F -n _rt_redo bmp_source/rt_redo.xpm images.py",
    "-a -F -n _rt_sample bmp_source/rt_sample.xpm images.py",
    "-a -F -n _rt_save bmp_source/rt_save.xpm images.py",
    "-a -F -n _rt_smiley bmp_source/rt_smiley.xpm images.py",
    "-a -F -n _rt_underline bmp_source/rt_underline.xpm images.py",
    "-a -F -n _rt_undo bmp_source/rt_undo.xpm images.py",
    "-a -F -n _rt_zebra bmp_source/rt_zebra.xpm images.py",

    "-a -F -n _bp_btn1 bmp_source/bp_btn1.png images.py",
    "-a -F -n _bp_btn2 bmp_source/bp_btn2.png images.py",
    "-a -F -n _bp_btn3 bmp_source/bp_btn3.png images.py",
    "-a -F -n _bp_btn4 bmp_source/bp_btn4.png images.py",

    "-a -F -n _book_red   bmp_source/book_red.png   images.py",
    "-a -F -n _book_green bmp_source/book_green.png images.py",
    "-a -F -n _book_blue  bmp_source/book_blue.png  images.py",

    "-a -F -c bmp_source/book.png              images.py",
    "-a -F -c bmp_source/clipboard.png         images.py",
    "-a -F -c bmp_source/code.png              images.py",
    "-a -F -c bmp_source/core.png              images.py",
    "-a -F -c bmp_source/custom.png            images.py",
    "-a -F -c bmp_source/deleteperspective.png images.py",
    "-a -F -c bmp_source/demo.png              images.py",
    "-a -F -c bmp_source/dialog.png            images.py",
    "-a -F -c bmp_source/exit.png              images.py",
    "-a -F -c bmp_source/expansion.png         images.py",
    "-a -F -c bmp_source/find.png              images.py",
    "-a -F -c bmp_source/findnext.png          images.py",
    "-a -F -c bmp_source/frame.png             images.py",
    "-a -F -c bmp_source/images.png            images.py",
    "-a -F -c bmp_source/inspect.png           images.py",
    "-a -F -c bmp_source/layout.png            images.py",
    "-a -F -c bmp_source/miscellaneous.png     images.py",
    "-a -F -c bmp_source/modifiedexists.png    images.py",
    "-a -F -c bmp_source/morecontrols.png      images.py",
    "-a -F -c bmp_source/moredialog.png        images.py",
    "-a -F -c bmp_source/overview.png          images.py",
    "-a -F -c bmp_source/process.png           images.py",
    "-a -F -c bmp_source/pyshell.png           images.py",
    "-a -F -c bmp_source/recent.png            images.py",
    "-a -F -c bmp_source/saveperspective.png   images.py",
    "-a -F -c bmp_source/customcontrol.png     images.py",

    "-a -F -c bmp_source/deletedocs.png     images.py",

    "-a -F -c -n spinning_nb0 bmp_source/FRM_0.png images.py",
    "-a -F -c -n spinning_nb1 bmp_source/FRM_1.png images.py",
    "-a -F -c -n spinning_nb2 bmp_source/FRM_2.png images.py",
    "-a -F -c -n spinning_nb3 bmp_source/FRM_3.png images.py",
    "-a -F -c -n spinning_nb4 bmp_source/FRM_4.png images.py",
    "-a -F -c -n spinning_nb5 bmp_source/FRM_5.png images.py",
    "-a -F -c -n spinning_nb6 bmp_source/FRM_6.png images.py",
    "-a -F -c -n spinning_nb7 bmp_source/FRM_7.png images.py",
    "-a -F -c -n spinning_nb8 bmp_source/FRM_8.png images.py",

    "   -F -c bmp_source/001.png throbImages.py",
    "-a -F -c bmp_source/002.png throbImages.py",
    "-a -F -c bmp_source/003.png throbImages.py",
    "-a -F -c bmp_source/004.png throbImages.py",
    "-a -F -c bmp_source/005.png throbImages.py",
    "-a -F -c bmp_source/006.png throbImages.py",
    "-a -F -c bmp_source/007.png throbImages.py",
    "-a -F -c bmp_source/008.png throbImages.py",
    "-a -F -c bmp_source/009.png throbImages.py",
    "-a -F -c bmp_source/010.png throbImages.py",
    "-a -F -c bmp_source/011.png throbImages.py",
    "-a -F -c bmp_source/012.png throbImages.py",
    "-a -F -c bmp_source/013.png throbImages.py",
    "-a -F -c bmp_source/014.png throbImages.py",
    "-a -F -c bmp_source/015.png throbImages.py",
    "-a -F -c bmp_source/016.png throbImages.py",
    "-a -F -c bmp_source/017.png throbImages.py",
    "-a -F -c bmp_source/018.png throbImages.py",
    "-a -F -c bmp_source/019.png throbImages.py",
    "-a -F -c bmp_source/020.png throbImages.py",
    "-a -F -c bmp_source/021.png throbImages.py",
    "-a -F -c bmp_source/022.png throbImages.py",
    "-a -F -c bmp_source/023.png throbImages.py",
    "-a -F -c bmp_source/024.png throbImages.py",
    "-a -F -c bmp_source/025.png throbImages.py",
    "-a -F -c bmp_source/026.png throbImages.py",
    "-a -F -c bmp_source/027.png throbImages.py",
    "-a -F -c bmp_source/028.png throbImages.py",
    "-a -F -c bmp_source/029.png throbImages.py",
    "-a -F -c bmp_source/030.png throbImages.py",

    "-a -F -c bmp_source/logo.png    throbImages.py",
    "-a -F -c bmp_source/rest.png    throbImages.py",
    ]


if __name__ == "__main__":
    for line in command_lines:
        args = line.split()
        img2py.main(args)

