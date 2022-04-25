
                def OnChar(self, event):

                    keycode = event.GetUnicodeKey()

                    if keycode != wx.WXK_NONE:

                        # It's a printable character
                        wx.LogMessage("You pressed '%c'"%keycode)

                    else:

                        # It's a special key, deal with all the known ones:
                        keycode = event.GetKeyCode()
                        if keycode in [wx.WXK_LEFT, wx.WXK_RIGHT]:
                            # move cursor ...
                            MoveCursor()

                        elif keycode == wx.WXK_F1:
                            # give help ...
                            GiveHelp()




