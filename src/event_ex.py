# Create some event binders
EVT_SIZE = wx.PyEventBinder( wxEVT_SIZE )
EVT_SIZING = wx.PyEventBinder( wxEVT_SIZING )
EVT_MOVE = wx.PyEventBinder( wxEVT_MOVE )
EVT_MOVING = wx.PyEventBinder( wxEVT_MOVING )
EVT_MOVE_START = wx.PyEventBinder( wxEVT_MOVE_START )
EVT_MOVE_END = wx.PyEventBinder( wxEVT_MOVE_END )
EVT_CLOSE = wx.PyEventBinder( wxEVT_CLOSE_WINDOW )
EVT_END_SESSION = wx.PyEventBinder( wxEVT_END_SESSION )
EVT_QUERY_END_SESSION = wx.PyEventBinder( wxEVT_QUERY_END_SESSION )
EVT_PAINT = wx.PyEventBinder( wxEVT_PAINT )
EVT_NC_PAINT = wx.PyEventBinder( wxEVT_NC_PAINT )
EVT_ERASE_BACKGROUND = wx.PyEventBinder( wxEVT_ERASE_BACKGROUND )
EVT_CHAR = wx.PyEventBinder( wxEVT_CHAR )
EVT_KEY_DOWN = wx.PyEventBinder( wxEVT_KEY_DOWN )
EVT_KEY_UP = wx.PyEventBinder( wxEVT_KEY_UP )
EVT_HOTKEY = wx.PyEventBinder( wxEVT_HOTKEY, 1)
EVT_CHAR_HOOK = wx.PyEventBinder( wxEVT_CHAR_HOOK )
EVT_MENU_OPEN = wx.PyEventBinder( wxEVT_MENU_OPEN )
EVT_MENU_CLOSE = wx.PyEventBinder( wxEVT_MENU_CLOSE )
EVT_MENU_HIGHLIGHT = wx.PyEventBinder( wxEVT_MENU_HIGHLIGHT, 1)
EVT_MENU_HIGHLIGHT_ALL = wx.PyEventBinder( wxEVT_MENU_HIGHLIGHT )
EVT_SET_FOCUS = wx.PyEventBinder( wxEVT_SET_FOCUS )
EVT_KILL_FOCUS = wx.PyEventBinder( wxEVT_KILL_FOCUS )
EVT_CHILD_FOCUS = wx.PyEventBinder( wxEVT_CHILD_FOCUS )
EVT_ACTIVATE = wx.PyEventBinder( wxEVT_ACTIVATE )
EVT_ACTIVATE_APP = wx.PyEventBinder( wxEVT_ACTIVATE_APP )
EVT_HIBERNATE = wx.PyEventBinder( wxEVT_HIBERNATE )
EVT_DROP_FILES = wx.PyEventBinder( wxEVT_DROP_FILES )
EVT_INIT_DIALOG = wx.PyEventBinder( wxEVT_INIT_DIALOG )
EVT_SYS_COLOUR_CHANGED = wx.PyEventBinder( wxEVT_SYS_COLOUR_CHANGED )
EVT_DISPLAY_CHANGED = wx.PyEventBinder( wxEVT_DISPLAY_CHANGED )
EVT_DPI_CHANGED = wx.PyEventBinder( wxEVT_DPI_CHANGED )
EVT_SHOW = wx.PyEventBinder( wxEVT_SHOW )
EVT_MAXIMIZE = wx.PyEventBinder( wxEVT_MAXIMIZE )
EVT_ICONIZE = wx.PyEventBinder( wxEVT_ICONIZE )
EVT_NAVIGATION_KEY = wx.PyEventBinder( wxEVT_NAVIGATION_KEY )
EVT_PALETTE_CHANGED = wx.PyEventBinder( wxEVT_PALETTE_CHANGED )
EVT_QUERY_NEW_PALETTE = wx.PyEventBinder( wxEVT_QUERY_NEW_PALETTE )
EVT_WINDOW_CREATE = wx.PyEventBinder( wxEVT_CREATE )
EVT_WINDOW_DESTROY = wx.PyEventBinder( wxEVT_DESTROY )
EVT_SET_CURSOR = wx.PyEventBinder( wxEVT_SET_CURSOR )
EVT_MOUSE_CAPTURE_CHANGED = wx.PyEventBinder( wxEVT_MOUSE_CAPTURE_CHANGED )
EVT_MOUSE_CAPTURE_LOST = wx.PyEventBinder( wxEVT_MOUSE_CAPTURE_LOST )

EVT_LEFT_DOWN = wx.PyEventBinder( wxEVT_LEFT_DOWN )
EVT_LEFT_UP = wx.PyEventBinder( wxEVT_LEFT_UP )
EVT_MIDDLE_DOWN = wx.PyEventBinder( wxEVT_MIDDLE_DOWN )
EVT_MIDDLE_UP = wx.PyEventBinder( wxEVT_MIDDLE_UP )
EVT_RIGHT_DOWN = wx.PyEventBinder( wxEVT_RIGHT_DOWN )
EVT_RIGHT_UP = wx.PyEventBinder( wxEVT_RIGHT_UP )
EVT_MOTION = wx.PyEventBinder( wxEVT_MOTION )
EVT_LEFT_DCLICK = wx.PyEventBinder( wxEVT_LEFT_DCLICK )
EVT_MIDDLE_DCLICK = wx.PyEventBinder( wxEVT_MIDDLE_DCLICK )
EVT_RIGHT_DCLICK = wx.PyEventBinder( wxEVT_RIGHT_DCLICK )
EVT_LEAVE_WINDOW = wx.PyEventBinder( wxEVT_LEAVE_WINDOW )
EVT_ENTER_WINDOW = wx.PyEventBinder( wxEVT_ENTER_WINDOW )
EVT_MOUSEWHEEL = wx.PyEventBinder( wxEVT_MOUSEWHEEL )
EVT_MOUSE_AUX1_DOWN = wx.PyEventBinder( wxEVT_AUX1_DOWN )
EVT_MOUSE_AUX1_UP = wx.PyEventBinder( wxEVT_AUX1_UP )
EVT_MOUSE_AUX1_DCLICK = wx.PyEventBinder( wxEVT_AUX1_DCLICK )
EVT_MOUSE_AUX2_DOWN = wx.PyEventBinder( wxEVT_AUX2_DOWN )
EVT_MOUSE_AUX2_UP = wx.PyEventBinder( wxEVT_AUX2_UP )
EVT_MOUSE_AUX2_DCLICK = wx.PyEventBinder( wxEVT_AUX2_DCLICK )

EVT_MOUSE_EVENTS = wx.PyEventBinder([ wxEVT_LEFT_DOWN,
                                      wxEVT_LEFT_UP,
                                      wxEVT_MIDDLE_DOWN,
                                      wxEVT_MIDDLE_UP,
                                      wxEVT_RIGHT_DOWN,
                                      wxEVT_RIGHT_UP,
                                      wxEVT_MOTION,
                                      wxEVT_LEFT_DCLICK,
                                      wxEVT_MIDDLE_DCLICK,
                                      wxEVT_RIGHT_DCLICK,
                                      wxEVT_ENTER_WINDOW,
                                      wxEVT_LEAVE_WINDOW,
                                      wxEVT_MOUSEWHEEL,
                                      wxEVT_AUX1_DOWN,
                                      wxEVT_AUX1_UP,
                                      wxEVT_AUX1_DCLICK,
                                      wxEVT_AUX2_DOWN,
                                      wxEVT_AUX2_UP,
                                      wxEVT_AUX2_DCLICK,
                                     ])
EVT_MAGNIFY = wx.PyEventBinder( wxEVT_MAGNIFY )


# Scrolling from wxWindow (sent to wxScrolledWindow)
EVT_SCROLLWIN = wx.PyEventBinder([ wxEVT_SCROLLWIN_TOP,
                                  wxEVT_SCROLLWIN_BOTTOM,
                                  wxEVT_SCROLLWIN_LINEUP,
                                  wxEVT_SCROLLWIN_LINEDOWN,
                                  wxEVT_SCROLLWIN_PAGEUP,
                                  wxEVT_SCROLLWIN_PAGEDOWN,
                                  wxEVT_SCROLLWIN_THUMBTRACK,
                                  wxEVT_SCROLLWIN_THUMBRELEASE,
                                  ])

EVT_SCROLLWIN_TOP = wx.PyEventBinder( wxEVT_SCROLLWIN_TOP )
EVT_SCROLLWIN_BOTTOM = wx.PyEventBinder( wxEVT_SCROLLWIN_BOTTOM )
EVT_SCROLLWIN_LINEUP = wx.PyEventBinder( wxEVT_SCROLLWIN_LINEUP )
EVT_SCROLLWIN_LINEDOWN = wx.PyEventBinder( wxEVT_SCROLLWIN_LINEDOWN )
EVT_SCROLLWIN_PAGEUP = wx.PyEventBinder( wxEVT_SCROLLWIN_PAGEUP )
EVT_SCROLLWIN_PAGEDOWN = wx.PyEventBinder( wxEVT_SCROLLWIN_PAGEDOWN )
EVT_SCROLLWIN_THUMBTRACK = wx.PyEventBinder( wxEVT_SCROLLWIN_THUMBTRACK )
EVT_SCROLLWIN_THUMBRELEASE = wx.PyEventBinder( wxEVT_SCROLLWIN_THUMBRELEASE )

# Scrolling from wx.Slider and wx.ScrollBar
EVT_SCROLL = wx.PyEventBinder([ wxEVT_SCROLL_TOP,
                               wxEVT_SCROLL_BOTTOM,
                               wxEVT_SCROLL_LINEUP,
                               wxEVT_SCROLL_LINEDOWN,
                               wxEVT_SCROLL_PAGEUP,
                               wxEVT_SCROLL_PAGEDOWN,
                               wxEVT_SCROLL_THUMBTRACK,
                               wxEVT_SCROLL_THUMBRELEASE,
                               wxEVT_SCROLL_CHANGED,
                               ])

EVT_SCROLL_TOP = wx.PyEventBinder( wxEVT_SCROLL_TOP )
EVT_SCROLL_BOTTOM = wx.PyEventBinder( wxEVT_SCROLL_BOTTOM )
EVT_SCROLL_LINEUP = wx.PyEventBinder( wxEVT_SCROLL_LINEUP )
EVT_SCROLL_LINEDOWN = wx.PyEventBinder( wxEVT_SCROLL_LINEDOWN )
EVT_SCROLL_PAGEUP = wx.PyEventBinder( wxEVT_SCROLL_PAGEUP )
EVT_SCROLL_PAGEDOWN = wx.PyEventBinder( wxEVT_SCROLL_PAGEDOWN )
EVT_SCROLL_THUMBTRACK = wx.PyEventBinder( wxEVT_SCROLL_THUMBTRACK )
EVT_SCROLL_THUMBRELEASE = wx.PyEventBinder( wxEVT_SCROLL_THUMBRELEASE )
EVT_SCROLL_CHANGED = wx.PyEventBinder( wxEVT_SCROLL_CHANGED )
EVT_SCROLL_ENDSCROLL = EVT_SCROLL_CHANGED

# Scrolling from wx.Slider and wx.ScrollBar, with an id
EVT_COMMAND_SCROLL = wx.PyEventBinder([ wxEVT_SCROLL_TOP,
                                       wxEVT_SCROLL_BOTTOM,
                                       wxEVT_SCROLL_LINEUP,
                                       wxEVT_SCROLL_LINEDOWN,
                                       wxEVT_SCROLL_PAGEUP,
                                       wxEVT_SCROLL_PAGEDOWN,
                                       wxEVT_SCROLL_THUMBTRACK,
                                       wxEVT_SCROLL_THUMBRELEASE,
                                       wxEVT_SCROLL_CHANGED,
                                       ], 1)

EVT_COMMAND_SCROLL_TOP = wx.PyEventBinder( wxEVT_SCROLL_TOP, 1)
EVT_COMMAND_SCROLL_BOTTOM = wx.PyEventBinder( wxEVT_SCROLL_BOTTOM, 1)
EVT_COMMAND_SCROLL_LINEUP = wx.PyEventBinder( wxEVT_SCROLL_LINEUP, 1)
EVT_COMMAND_SCROLL_LINEDOWN = wx.PyEventBinder( wxEVT_SCROLL_LINEDOWN, 1)
EVT_COMMAND_SCROLL_PAGEUP = wx.PyEventBinder( wxEVT_SCROLL_PAGEUP, 1)
EVT_COMMAND_SCROLL_PAGEDOWN = wx.PyEventBinder( wxEVT_SCROLL_PAGEDOWN, 1)
EVT_COMMAND_SCROLL_THUMBTRACK = wx.PyEventBinder( wxEVT_SCROLL_THUMBTRACK, 1)
EVT_COMMAND_SCROLL_THUMBRELEASE = wx.PyEventBinder( wxEVT_SCROLL_THUMBRELEASE, 1)
EVT_COMMAND_SCROLL_CHANGED = wx.PyEventBinder( wxEVT_SCROLL_CHANGED, 1)
EVT_COMMAND_SCROLL_ENDSCROLL = EVT_COMMAND_SCROLL_CHANGED

EVT_BUTTON = wx.PyEventBinder( wxEVT_BUTTON, 1)
EVT_CHECKBOX = wx.PyEventBinder( wxEVT_CHECKBOX, 1)
EVT_CHOICE = wx.PyEventBinder( wxEVT_CHOICE, 1)
EVT_LISTBOX = wx.PyEventBinder( wxEVT_LISTBOX, 1)
EVT_LISTBOX_DCLICK = wx.PyEventBinder( wxEVT_LISTBOX_DCLICK, 1)
EVT_MENU = wx.PyEventBinder( wxEVT_MENU, 1)
EVT_MENU_RANGE = wx.PyEventBinder( wxEVT_MENU, 2)
EVT_SLIDER = wx.PyEventBinder( wxEVT_SLIDER, 1)
EVT_RADIOBOX = wx.PyEventBinder( wxEVT_RADIOBOX, 1)
EVT_RADIOBUTTON = wx.PyEventBinder( wxEVT_RADIOBUTTON, 1)

EVT_SCROLLBAR = wx.PyEventBinder( wxEVT_SCROLLBAR, 1)
EVT_VLBOX = wx.PyEventBinder( wxEVT_VLBOX, 1)
EVT_COMBOBOX = wx.PyEventBinder( wxEVT_COMBOBOX, 1)
EVT_TOOL = wx.PyEventBinder( wxEVT_TOOL, 1)
EVT_TOOL_RANGE = wx.PyEventBinder( wxEVT_TOOL, 2)
EVT_TOOL_RCLICKED = wx.PyEventBinder( wxEVT_TOOL_RCLICKED, 1)
EVT_TOOL_RCLICKED_RANGE = wx.PyEventBinder( wxEVT_TOOL_RCLICKED, 2)
EVT_TOOL_ENTER = wx.PyEventBinder( wxEVT_TOOL_ENTER, 1)
EVT_TOOL_DROPDOWN = wx.PyEventBinder( wxEVT_TOOL_DROPDOWN, 1)
EVT_CHECKLISTBOX = wx.PyEventBinder( wxEVT_CHECKLISTBOX, 1)
EVT_COMBOBOX_DROPDOWN = wx.PyEventBinder( wxEVT_COMBOBOX_DROPDOWN , 1)
EVT_COMBOBOX_CLOSEUP  = wx.PyEventBinder( wxEVT_COMBOBOX_CLOSEUP , 1)

EVT_COMMAND_LEFT_CLICK = wx.PyEventBinder( wxEVT_COMMAND_LEFT_CLICK, 1)
EVT_COMMAND_LEFT_DCLICK = wx.PyEventBinder( wxEVT_COMMAND_LEFT_DCLICK, 1)
EVT_COMMAND_RIGHT_CLICK = wx.PyEventBinder( wxEVT_COMMAND_RIGHT_CLICK, 1)
EVT_COMMAND_RIGHT_DCLICK = wx.PyEventBinder( wxEVT_COMMAND_RIGHT_DCLICK, 1)
EVT_COMMAND_SET_FOCUS = wx.PyEventBinder( wxEVT_COMMAND_SET_FOCUS, 1)
EVT_COMMAND_KILL_FOCUS = wx.PyEventBinder( wxEVT_COMMAND_KILL_FOCUS, 1)
EVT_COMMAND_ENTER = wx.PyEventBinder( wxEVT_COMMAND_ENTER, 1)

EVT_HELP = wx.PyEventBinder( wxEVT_HELP, 1)
EVT_HELP_RANGE = wx.PyEventBinder(  wxEVT_HELP, 2)
EVT_DETAILED_HELP = wx.PyEventBinder( wxEVT_DETAILED_HELP, 1)
EVT_DETAILED_HELP_RANGE = wx.PyEventBinder( wxEVT_DETAILED_HELP, 2)

EVT_IDLE = wx.PyEventBinder( wxEVT_IDLE )

EVT_UPDATE_UI = wx.PyEventBinder( wxEVT_UPDATE_UI, 1)
EVT_UPDATE_UI_RANGE = wx.PyEventBinder( wxEVT_UPDATE_UI, 2)

EVT_CONTEXT_MENU = wx.PyEventBinder( wxEVT_CONTEXT_MENU )

EVT_THREAD = wx.PyEventBinder( wxEVT_THREAD )

EVT_WINDOW_MODAL_DIALOG_CLOSED = wx.PyEventBinder( wxEVT_WINDOW_MODAL_DIALOG_CLOSED )

EVT_JOY_BUTTON_DOWN = wx.PyEventBinder( wxEVT_JOY_BUTTON_DOWN )
EVT_JOY_BUTTON_UP = wx.PyEventBinder( wxEVT_JOY_BUTTON_UP )
EVT_JOY_MOVE = wx.PyEventBinder( wxEVT_JOY_MOVE )
EVT_JOY_ZMOVE = wx.PyEventBinder( wxEVT_JOY_ZMOVE )
EVT_JOYSTICK_EVENTS = wx.PyEventBinder([ wxEVT_JOY_BUTTON_DOWN,
                                        wxEVT_JOY_BUTTON_UP,
                                        wxEVT_JOY_MOVE,
                                        wxEVT_JOY_ZMOVE,
                                        ])

EVT_GESTURE_PAN = wx.PyEventBinder( wxEVT_GESTURE_PAN )
EVT_GESTURE_ZOOM = wx.PyEventBinder( wxEVT_GESTURE_ZOOM )
EVT_GESTURE_ROTATE = wx.PyEventBinder( wxEVT_GESTURE_ROTATE )
EVT_TWO_FINGER_TAP = wx.PyEventBinder( wxEVT_TWO_FINGER_TAP )
EVT_LONG_PRESS = wx.PyEventBinder( wxEVT_LONG_PRESS )
EVT_PRESS_AND_TAP = wx.PyEventBinder( wxEVT_PRESS_AND_TAP )

EVT_CLIPBOARD_CHANGED = wx.PyEventBinder(wxEVT_CLIPBOARD_CHANGED, 1)

EVT_FULLSCREEN = wx.PyEventBinder(wxEVT_FULLSCREEN, 1)

# deprecated wxEVT aliases
wxEVT_COMMAND_BUTTON_CLICKED         = wxEVT_BUTTON
wxEVT_COMMAND_CHECKBOX_CLICKED       = wxEVT_CHECKBOX
wxEVT_COMMAND_CHOICE_SELECTED        = wxEVT_CHOICE
wxEVT_COMMAND_LISTBOX_SELECTED       = wxEVT_LISTBOX
wxEVT_COMMAND_LISTBOX_DOUBLECLICKED  = wxEVT_LISTBOX_DCLICK
wxEVT_COMMAND_CHECKLISTBOX_TOGGLED   = wxEVT_CHECKLISTBOX
wxEVT_COMMAND_MENU_SELECTED          = wxEVT_MENU
wxEVT_COMMAND_TOOL_CLICKED           = wxEVT_TOOL
wxEVT_COMMAND_SLIDER_UPDATED         = wxEVT_SLIDER
wxEVT_COMMAND_RADIOBOX_SELECTED      = wxEVT_RADIOBOX
wxEVT_COMMAND_RADIOBUTTON_SELECTED   = wxEVT_RADIOBUTTON
wxEVT_COMMAND_SCROLLBAR_UPDATED      = wxEVT_SCROLLBAR
wxEVT_COMMAND_VLBOX_SELECTED         = wxEVT_VLBOX
wxEVT_COMMAND_COMBOBOX_SELECTED      = wxEVT_COMBOBOX
wxEVT_COMMAND_TOOL_RCLICKED          = wxEVT_TOOL_RCLICKED
wxEVT_COMMAND_TOOL_DROPDOWN_CLICKED  = wxEVT_TOOL_DROPDOWN
wxEVT_COMMAND_TOOL_ENTER             = wxEVT_TOOL_ENTER
wxEVT_COMMAND_COMBOBOX_DROPDOWN      = wxEVT_COMBOBOX_DROPDOWN
wxEVT_COMMAND_COMBOBOX_CLOSEUP       = wxEVT_COMBOBOX_CLOSEUP
