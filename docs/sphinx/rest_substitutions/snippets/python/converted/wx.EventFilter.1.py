
        # This class allows to determine the last time the user has worked with
        # this application:
        class LastActivityTimeDetector(wx.EventFilter):

            def __init__(self):

                wx.EventFilter.__init__(self)

                wx.EvtHandler.AddFilter(self)

                self.last = wx.DateTime.Now()


            def __del__(self):

                wx.EvtHandler.RemoveFilter(self)


            def FilterEvent(self, event):

                # Update the last user activity
                t = event.GetEventType()

                if t == wx.EVT_KEY_DOWN.typeId or t == wx.EVT_MOTION.typeId or \
                   t == wx.EVT_LEFT_DOWN.typeId or t == wx.EVT_RIGHT_DOWN.typeId or \
                   t == wx.EVT_MIDDLE_DOWN.typeId:

                    self.last = wx.DateTime.Now()


                # Continue processing the event normally as well.
                return self.Event_Skip


            # This function could be called periodically from some timer to
            # do something (e.g. hide sensitive data or log out from remote
            # server) if the user has been inactive for some time period.
            def IsInactiveFor(self, diff):

                return wx.DateTime.Now() - diff > self.last


