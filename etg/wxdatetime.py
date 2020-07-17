#---------------------------------------------------------------------------
# Name:        etg/datetime.py
# Author:      Robin Dunn
#
# Created:     27-Feb-2012
# Copyright:   (c) 2012-2020 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools

PACKAGE   = "wx"
MODULE    = "_core"
NAME      = "wxdatetime"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script.
ITEMS  = [ "wxDateTime",
           "wxDateSpan",
           "wxTimeSpan",
           #"wxDateTimeHolidayAuthority",
           #"wxDateTimeWorkDays",
           ]

#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)

    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.


    # Lots of the uses of wxDateTime_t have been changed to "unsigned short"
    # in the interface file, so lets go ahead and translate the rest of them
    # too so there will not be any "wxDateTime_t" in Phoenix confusingly
    # mixed with "unsigned short"s.
    #
    # Also add the class scope specifier to nested enum types for parameters
    # and return values.
    for item in module.allItems():
        if isinstance(item, (etgtools.FunctionDef, etgtools.ParamDef, etgtools.VariableDef)):
            typesMap = { 'wxDateTime_t': 'unsigned short',
                         'Month'       : 'wxDateTime::Month',
                         'WeekDay'     : 'wxDateTime::WeekDay',
                         'TZ'          : 'wxDateTime::TZ',
                         'TimeZone'    : 'wxDateTime::TimeZone',
                         'Tm'          : 'wxDateTime::Tm',
                        }
            if item.type in typesMap:
                item.type = typesMap[item.type]


    # ignore the #define and add it as a Python alias instead
    module.find('wxInvalidDateTime').ignore()
    module.addPyCode('InvalidDateTime = DefaultDateTime')
    gs = module.addGlobalStr('wxDefaultDateTimeFormat', module.find('wxInvalidDateTime'))
    module.addGlobalStr('wxDefaultTimeSpanFormat', gs)


    #---------------------------------------------
    # Tweaks for the wxDateTime class
    c = module.find('wxDateTime')
    assert isinstance(c, etgtools.ClassDef)
    c.allowAutoProperties = False
    tools.ignoreAllOperators(c)

    # Ignore ctors with unknown types or that have overload conflicts that
    # can't be distinguished in Python
    ctor = c.find('wxDateTime')
    ctor.findOverload('time_t').ignore()
    ctor.findOverload('struct tm').ignore()
    ctor.findOverload('double jdn').ignore()
    ctor.findOverload('_SYSTEMTIME').ignore()
    ctor.findOverload('hour').ignore() # careful, the one we want to keep has an 'hour' param too

    # Add static factories for some of the ctors we ignored
    c.addCppMethod('wxDateTime*', 'FromTimeT', '(time_t timet)',
        factory=True, isStatic=True,
        doc="Construct a :class:`DateTime` from a C ``time_t`` value, the number of seconds since the epoch.",
        body="return new wxDateTime(timet);")

    c.addCppMethod('wxDateTime*', 'FromJDN', '(double jdn)',
        factory=True, isStatic=True,
        doc="Construct a :class:`DateTime` from a Julian Day Number.\n\n"
            "By definition, the Julian Day Number, usually abbreviated as JDN, of a particular instant is the fractional number of days since 12 hours Universal Coordinated Time (Greenwich mean noon) on January 1 of the year -4712 in the Julian proleptic calendar.",
        body="return new wxDateTime(jdn);")

    c.addCppMethod('wxDateTime*', 'FromHMS',
        """(unsigned short hour,
            unsigned short minute=0,
            unsigned short second=0,
            unsigned short millisecond=0)""",
        factory=True, isStatic=True,
        doc="Construct a :class:`DateTime` equal to :meth:`Today` () with the time set to the supplied parameters.",
        body="return new wxDateTime(hour, minute, second, millisecond);")

    c.addCppMethod('wxDateTime*', 'FromDMY',
        """(unsigned short day,
            wxDateTime::Month month,
            int year = Inv_Year,
            unsigned short hour=0,
            unsigned short minute=0,
            unsigned short second=0,
            unsigned short millisecond=0)""",
        factory=True, isStatic=True,
        doc="Construct a :class:`DateTime` using the supplied parameters.",
        body="return new wxDateTime(day, month, year, hour, minute, second, millisecond);")

    # and give them some simple wrappers for Classic compatibility
    module.addPyFunction('DateTimeFromTimeT', '(timet)',
        doc="Compatibility wrapper for :meth:`DateTime.FromTimeT`",
        body="return DateTime.FromTimeT(timet)",
        deprecated='Use :meth:`DateTime.FromTimeT` instead.')
    module.addPyFunction('DateTimeFromJDN', '(jdn)',
        doc="Compatibility wrapper for :meth:`DateTime.FromJDN`",
        body="return DateTime.FromJDN(jdn)",
        deprecated='Use :meth:`DateTime.FromJDN` instead.')
    module.addPyFunction('DateTimeFromHMS', '(hour, minute=0, second=0, millisecond=0)',
        doc="Compatibility wrapper for :meth:`DateTime.FromHMS`",
        body="return DateTime.FromHMS(hour, minute, second, millisecond)",
        deprecated='Use :meth:`DateTime.FromHMS` instead.')
    module.addPyFunction('DateTimeFromDMY', '(day, month, year=DateTime.Inv_Year, hour=0, minute=0, second=0, millisecond=0)',
        doc="Compatibility wrapper for :meth:`DateTime.FromDMY`",
        body="return DateTime.FromDMY(day, month, year, hour, minute, second, millisecond)",
        deprecated='Use :meth:`DateTime.FromDMY` instead.')


    # Fixup similar conflicts in the Set method overloads
    c.find('Set').findOverload('struct tm').ignore()
    c.find('Set').renameOverload('Tm',         'SetTm')
    c.find('Set').renameOverload('time_t',     'SetTimeT')
    c.find('Set').renameOverload('double jdn', 'SetJDN')
    c.find('Set').renameOverload('hour',       'SetHMS')

    # Unknown parameter and return types
    c.find('SetFromMSWSysTime').ignore()
    c.find('GetAsMSWSysTime').ignore()

    # this overload is static, the other isn't.  Rename it?
    c.find('GetCentury').findOverload('year').ignore()

    c.find('GetNumberOfDays').ignore()
    c.find('GetTmNow').ignore()
    c.find('GetTmNow').ignore()

    # output the am/pm parameter values
    c.find('GetAmPmStrings.am').out = True
    c.find('GetAmPmStrings.pm').out = True


    # remove the const version of the overloaded Add's and Subtract's
    c.find('Add').findOverload('wxDateSpan', isConst=True).ignore()
    c.find('Add').findOverload('wxTimeSpan', isConst=True).ignore()
    c.find('Subtract').findOverload('wxDateSpan', isConst=True).ignore()
    c.find('Subtract').findOverload('wxTimeSpan', isConst=True).ignore()


    # Ignore the end parameter for the Parse*() methods, and provide
    # replacement implementations that don't need them. Change them to be
    # like they were in Classic, returning a -1 on failure, or the number of
    # characters parsed otherwise.
    def fixParseMethod(m, code):
        assert isinstance(m, etgtools.MethodDef)
        m.find('end').ignore()
        m.type = 'int'
        m.setCppCode(code)
        return m


    fixParseMethod(c.find('ParseDate'), """\
        wxString::const_iterator begin = date->begin();
        wxString::const_iterator end;
        if (! self->ParseDate(*date, &end))
            return -1;
        return end - begin;
        """)

    fixParseMethod(c.find('ParseDateTime'), """\
        wxString::const_iterator begin = datetime->begin();
        wxString::const_iterator end;
        if (! self->ParseDateTime(*datetime, &end))
            return -1;
        return end - begin;
        """)

    fixParseMethod(c.find('ParseTime'), """\
        wxString::const_iterator begin = time->begin();
        wxString::const_iterator end;
        if (! self->ParseTime(*time, &end))
            return -1;
        return end - begin;
        """)

    fixParseMethod(c.find('ParseRfc822Date'), """\
        wxString::const_iterator begin = date->begin();
        wxString::const_iterator end;
        if (! self->ParseRfc822Date(*date, &end))
            return -1;
        return end - begin;
        """)


    pf = c.find('ParseFormat')
    pf1 = fixParseMethod(
        pf.findOverload('const wxString &date, const wxString &format, const wxDateTime &dateDef, wxString::'),
        """\
        wxString::const_iterator begin = date->begin();
        wxString::const_iterator end;
        if (! self->ParseFormat(*date, *format, *dateDef, &end))
            return -1;
        return end - begin;
        """)

    pf2 = fixParseMethod(
        pf.findOverload('const wxString &date, const wxString &format, wxString::'),
        """\
        wxString::const_iterator begin = date->begin();
        wxString::const_iterator end;
        if (! self->ParseFormat(*date, *format, &end))
            return -1;
        return end - begin;
        """)

    pf3 = fixParseMethod(
        pf.findOverload('const wxString &date, wxString::'),
        """\
        wxString::const_iterator begin = date->begin();
        wxString::const_iterator end;
        if (! self->ParseFormat(*date, &end))
            return -1;
        return end - begin;
        """)

    # Fiddle with the docstrings for ParseFormat to make them reflect the new
    # reality. The other Parse*() docs refer the reader to this one, so we
    # don't have to change all of them.

    # find the <simplesect kind="return"> node in the last paragraph
    para = pf1.detailedDoc[-1]
    elem = para.find("simplesect[@kind='return']")
    # it has a child paragraph containing the text we need to replace
    elem[0].text = '-1 if the parse failed, the number of characters parsed otherwise.'

    pf2.briefDoc = "This version of the :meth:`ParseFormat` method works the same, but with missing values filled in from :meth:`Today`."
    pf3.briefDoc = "This version uses \"%c\" as the format code, which is the same default used by :meth:`Format`."




    c.addPyMethod('__repr__', '(self)', """\
        from six import PY2
        if self.IsValid():
            f = self.Format()
            if PY2: f = f.encode('utf-8')
            return '<wx.DateTime: "%s">' % f
        else:
            return '<wx.DateTime: \"INVALID\">'
        """)

    c.addPyMethod('__str__', '(self)', """\
        from six import PY2
        if self.IsValid():
            f = self.Format()
            if PY2: f = f.encode('utf-8')
            return f
        else:
            return "INVALID DateTime"
        """)


    # use lowercase to avoid conflicts
    c.addProperty("day GetDay SetDay")
    c.addProperty("month GetMonth SetMonth")
    c.addProperty("year GetYear SetYear")
    c.addProperty("hour GetHour SetHour")
    c.addProperty("minute GetMinute SetMinute")
    c.addProperty("second GetSecond SetSecond")
    c.addProperty("millisecond GetMillisecond SetMillisecond")
    c.addProperty("JDN GetJDN SetJDN")

    c.addProperty("DayOfYear GetDayOfYear")
    c.addProperty("JulianDayNumber GetJulianDayNumber")
    c.addProperty("LastMonthDay GetLastMonthDay")
    c.addProperty("MJD GetMJD")
    c.addProperty("ModifiedJulianDayNumber GetModifiedJulianDayNumber")
    c.addProperty("RataDie GetRataDie")
    c.addProperty("Ticks GetTicks")
    c.addProperty("WeekOfMonth GetWeekOfMonth")
    c.addProperty("WeekOfYear GetWeekOfYear")


    c.addItem(etgtools.WigCode("""\
        bool operator<(const wxDateTime& dt) const;
        bool operator<=(const wxDateTime& dt) const;
        bool operator>(const wxDateTime& dt) const;
        bool operator>=(const wxDateTime& dt) const;
        bool operator==(const wxDateTime& dt) const;
        bool operator!=(const wxDateTime& dt) const;
        wxDateTime& operator+=(const wxTimeSpan& diff);
        wxDateTime operator+(const wxTimeSpan& ts) const;
        wxDateTime& operator-=(const wxTimeSpan& diff);
        wxDateTime operator-(const wxTimeSpan& ts) const;
        wxDateTime& operator+=(const wxDateSpan& diff);
        wxDateTime operator+(const wxDateSpan& ds) const;
        wxDateTime& operator-=(const wxDateSpan& diff);
        wxDateTime operator-(const wxDateSpan& ds) const;
        wxTimeSpan operator-(const wxDateTime& dt2) const;
        """))

    # Add some code (like MappedTypes) to automatically convert from a Python
    # datetime.date or a datetime.datetime object
    c.convertFromPyObject = """\
        // Code to test a PyObject for compatibility with wxDateTime
        if (!sipIsErr) {
            if (sipCanConvertToType(sipPy, sipType_wxDateTime, SIP_NO_CONVERTORS))
                    return TRUE;
            if (wxPyDateTime_Check(sipPy) || wxPyDate_Check(sipPy))
                return TRUE;
            return FALSE;
        }

        // Code to convert a compatible PyObject to a wxDateTime
        if (wxPyDateTime_Check(sipPy)) {
            *sipCppPtr = wxPyDateTime_ToWxDateTime(sipPy);
            return sipGetState(sipTransferObj);
        }
        if (wxPyDate_Check(sipPy)) {
            *sipCppPtr = wxPyDate_ToWxDateTime(sipPy);
            return sipGetState(sipTransferObj);
        }
        // if we get this far then it must already be a wxDateTime instance
        *sipCppPtr = reinterpret_cast<wxDateTime*>(sipConvertToType(
                sipPy, sipType_wxDateTime, sipTransferObj, SIP_NO_CONVERTORS, 0, sipIsErr));

        return 0;  // Not a new instance
        """


    #---------------------------------------------
    # Tweaks for the wxDateSpan class
    c = module.find('wxDateSpan')
    c.allowAutoProperties = False
    tools.ignoreAllOperators(c)

    c.find('Add').findOverload('', isConst=True).ignore()
    c.find('Multiply').findOverload('', isConst=True).ignore()
    c.find('Subtract').findOverload('', isConst=True).ignore()

    c.addItem(etgtools.WigCode("""\
        wxDateSpan& operator+=(const wxDateSpan& other);
        wxDateSpan operator+(const wxDateSpan& ds) const;
        wxDateSpan& operator-=(const wxDateSpan& other);
        wxDateSpan operator-(const wxDateSpan& ds) const;
        wxDateSpan& operator-();
        wxDateSpan& operator*=(int factor);
        wxDateSpan operator*(int n) const;
        bool operator==(const wxDateSpan& ds) const;
        bool operator!=(const wxDateSpan& ds) const;
        """))



    #---------------------------------------------
    # Tweaks for the wxTimeSpan class
    c = module.find('wxTimeSpan')
    c.allowAutoProperties = False
    tools.ignoreAllOperators(c)

    c.find('Add').findOverload('', isConst=True).ignore()
    c.find('Multiply').findOverload('', isConst=True).ignore()
    c.find('Subtract').findOverload('', isConst=True).ignore()

    c.addItem(etgtools.WigCode("""\
        wxTimeSpan& operator+=(const wxTimeSpan& diff);
        wxTimeSpan operator+(const wxTimeSpan& ts) const;
        wxTimeSpan& operator-=(const wxTimeSpan& diff);
        wxTimeSpan operator-(const wxTimeSpan& ts);
        wxTimeSpan& operator*=(int n);
        wxTimeSpan operator*(int n) const;
        wxTimeSpan& operator-();
        bool operator<(const wxTimeSpan &ts) const;
        bool operator<=(const wxTimeSpan &ts) const;
        bool operator>(const wxTimeSpan &ts) const;
        bool operator>=(const wxTimeSpan &ts) const;
        bool operator==(const wxTimeSpan &ts) const;
        bool operator!=(const wxTimeSpan &ts) const;
        """))


    #---------------------------------------------
    # Convert to/from Python date objects
    module.addPyFunction('pydate2wxdate', '(date)',
        doc='Convert a Python date or datetime to a :class:`DateTime` object',
        body="""\
            import datetime
            assert isinstance(date, (datetime.datetime, datetime.date))
            return DateTime(date)  # the built-in typemap will convert it for us
        """)

    module.addPyFunction('wxdate2pydate', '(date)',
        doc='Convert a :class:`DateTime` object to a Python datetime.',
        body="""\
            import datetime
            assert isinstance(date, DateTime)
            if date.IsValid():
                return datetime.datetime(date.year, date.month+1, date.day,
                                         date.hour, date.minute, date.second, date.millisecond*1000)
            else:
                return None
            """)



    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)


#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

