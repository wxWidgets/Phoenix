#!/usr/bin/env python

import wx
import wx.html
import wx.grid

import os
import sys
import time

from wx.lib.embeddedimage import PyEmbeddedImage

try:
    dirName = os.path.dirname(os.path.abspath(__file__))
except:
    dirName = os.path.dirname(os.path.abspath(sys.argv[0]))

sys.path.append(os.path.split(dirName)[0])

try:
    from agw import aui
    from agw.aui import aui_switcherdialog as ASD
except ImportError: # if it's not there locally, try the wxPython lib.
    import wx.lib.agw.aui as aui
    from wx.lib.agw.aui import aui_switcherdialog as ASD

import random
import images

ArtIDs = [ "wx.ART_ADD_BOOKMARK",
           "wx.ART_DEL_BOOKMARK",
           "wx.ART_HELP_SIDE_PANEL",
           "wx.ART_HELP_SETTINGS",
           "wx.ART_HELP_BOOK",
           "wx.ART_HELP_FOLDER",
           "wx.ART_HELP_PAGE",
           "wx.ART_GO_BACK",
           "wx.ART_GO_FORWARD",
           "wx.ART_GO_UP",
           "wx.ART_GO_DOWN",
           "wx.ART_GO_TO_PARENT",
           "wx.ART_GO_HOME",
           "wx.ART_FILE_OPEN",
           "wx.ART_PRINT",
           "wx.ART_HELP",
           "wx.ART_TIP",
           "wx.ART_REPORT_VIEW",
           "wx.ART_LIST_VIEW",
           "wx.ART_NEW_DIR",
           "wx.ART_HARDDISK",
           "wx.ART_FLOPPY",
           "wx.ART_CDROM",
           "wx.ART_REMOVABLE",
           "wx.ART_FOLDER",
           "wx.ART_FOLDER_OPEN",
           "wx.ART_GO_DIR_UP",
           "wx.ART_EXECUTABLE_FILE",
           "wx.ART_NORMAL_FILE",
           "wx.ART_TICK_MARK",
           "wx.ART_CROSS_MARK",
           "wx.ART_ERROR",
           "wx.ART_QUESTION",
           "wx.ART_WARNING",
           "wx.ART_INFORMATION",
           "wx.ART_MISSING_IMAGE",
           ]

# Custom pane button bitmaps
#----------------------------------------------------------------------
close = PyEmbeddedImage(
    b"iVBORw0KGgoAAAANSUhEUgAAAA0AAAANCAYAAABy6+R8AAAABHNCSVQICAgIfAhkiAAAAh9J"
    b"REFUKJFl0s1LFGEAx/HvMzO7M9vmrrSuThJIhslmaSZqFgZLdSqKjr147VB/Qn9Af0GXTiIU"
    b"vVAQdRAKqkuColaiiyiKr7FKL7u6OzM78zxPh6igfvcvv8tHCMMEoHAxr/35AlpK/p0wTZz2"
    b"HLlXbwWABTBzrk83DnSRvjWE4Tj/Rcr3KU1/Zsav6GNvxoU1cSGvmwZ7SZ3Oo5MpIiuGrvl/"
    b"X+IOIgpJndmPNONM2Elt7KyuU9/djySCbBNGo4ssriA3FlHfNjAaXchkiSKf+u5+ykvLGHLP"
    b"XlQiSS0SqLoMosHF6DwJdfWIXC+iwUWls4TaQtkJQtPC8gIPo1pldvQlanGNnqs3iLktyOwB"
    b"TNMk9AMmnzzEmHjHiVOD7AQBVjUI0JUdDqaTzLwfZS6VovPSFUytQUrmXjynfO8uR9MWyrEJ"
    b"/QCrFkrU9leM5QVysoa044jSD9AAmoxjk6GKtbqNaukglAojCHyi8Q8Ec7PsO3sZt/UQ3uYG"
    b"3+cLeF82cdsOk719hyjlIis+Na0wlJRExSJe23EitwW5VWRqZJjHQ9eYGhlGbhWJmlvxOvqp"
    b"lXeRSmM57TnWSx4/ltZZsR5hOAlKz57St1tmbWSYscou0vNIfJwlyGRIHOlACMPkwUCPzsmQ"
    b"aswi8Hza/ICYgFDDgmMTd2ySkaRgxrg+NinEb3v3z+f15qdpQt/DQvwREaGJOQmau7q5+fqX"
    b"vZ+3DPNuDe9/tAAAAABJRU5ErkJggg==")

#----------------------------------------------------------------------
close_inactive = PyEmbeddedImage(
    b"iVBORw0KGgoAAAANSUhEUgAAAA0AAAANCAYAAABy6+R8AAAABHNCSVQICAgIfAhkiAAAAh5J"
    b"REFUKJFl0stLVFEAgPHv3Htn7lzNGW1GZzSNtJI0fFZjQkQPqV0U0SJmnZugP6B9/0O4cZNE"
    b"ZFAQUdBrlZBYoJmGOYSPSUvRRp25r3NOi8iN3/7b/YQwTAAuDn7VM3kXqdiTaUBbS4w3Q+0C"
    b"QAjDpD83qfuPNdDZEicWMfZMbqCYzBcZmy0wNtIprIFb4/pUa4bzfXHiVRAxFWVP7w6OLQgk"
    b"NDTFsWOKyopxbSyubpPtShB6mroaQTolWFiQzM9LCsuadEpQWw1uSZHtSpBfKmLscySVFRpM"
    b"j+R+SaZWcLrXoDoBJ7shUydIJRVW1MeJaSwzxHLLJUqu4PnLaZYKity1Hg42RjhQb2CaAs/z"
    b"efjsM+/GDM6e6cErF7Hc8g5bO5rKqmZevJ8iXjXL1csdaC2QoeDpq1nu3S8SiXZgJxWe72NJ"
    b"6bO+rZhbNvDDdqKOZHMHtBYARJ0UrkyysGRyfEuhVIDhej4fpkO+5H2uXKqm5VCawi+fbz82"
    b"+fnb4+jhNHdvp8jUh7ihRMkAQ0rF6oaku73EwfqQlbWQ4dEJbt55xPDoBCtrIc2NIX3dZbbd"
    b"AK0k4lzugS5HT7C+vkG2tYxjmzx++4eiaiJuLHLjQoKSKxmfc0gma3D8iX8istdHtG+3YVHC"
    b"dX28yBEQEdABdvAd244iRQVRb4aPT3JC/Lc3kBvSn6YKlL0AYVi7IrQKcewIvR0NvB4ZFAB/"
    b"Aa4X7YpTOtu/AAAAAElFTkSuQmCC")

#----------------------------------------------------------------------
maximize = PyEmbeddedImage(
    b"iVBORw0KGgoAAAANSUhEUgAAAA0AAAANCAYAAABy6+R8AAAABHNCSVQICAgIfAhkiAAAAJZJ"
    b"REFUKJG9kj0OwjAMRp8D6hDUExDmrr0dEkOHXgXuAMfIBl1yCwaMMAyoIJQWqUu/yZa/5x/J"
    b"Im7BVLnJBLDsg2vbPC3G8e51zapp5QeyGLHzBYbWtcfwJFlv8Nsdrqpypuu4HfY5hHPgPVKW"
    b"+STv3/XeOnrEH80HfW9SxVIaNFlKoJpDEgL30xGKIqdUkRA+qcz2Ri8+yyNzplbFQwAAAABJ"
    b"RU5ErkJggg==")

#----------------------------------------------------------------------
maximize_inactive = PyEmbeddedImage(
    b"iVBORw0KGgoAAAANSUhEUgAAAA0AAAANCAYAAABy6+R8AAAABHNCSVQICAgIfAhkiAAAAJhJ"
    b"REFUKJFjZGRiZiAVMJGsg4GBgQXGaGz7+v/CxX84FRroMzHUV3Ezomi6cPEfw/Vb/xiYsbj2"
    b"718cNsnKMDJUlnAwqKthuvjmrX8MS1b8xtTEyMTAwMXFyMDLw4ihiYuLkYERySyyAoJ+muB+"
    b"+v2bgeHeA+xBfu/BP4bfiHBAaJKWYmTYsfsPAysrpqbfvyHyMMBIt2QEAFPtI359ud6yAAAA"
    b"AElFTkSuQmCC")

#----------------------------------------------------------------------
minimize = PyEmbeddedImage(
    b"iVBORw0KGgoAAAANSUhEUgAAAA0AAAANCAYAAABy6+R8AAAABHNCSVQICAgIfAhkiAAAAMlJ"
    b"REFUKJGdkrsNwkAQRN/eWohPByYkQaIKSqAJhBAF0AdExGRUQwoioAREAth3S2BjWzLIwER7"
    b"oxntzOpEnPIrotcQ1lvjeIbbHXjkpAczkAf0OjAc4GZTQZwiTrHNzhoxX5g4xRU7U9+c654A"
    b"VEzY150qpuQLedY1qvFJCqrgX3ENQp5C7IMp9eAEQsjEIWQXVC3UpckSWK5gfwCRnKv0nIwL"
    b"vrLJQDzomytGEXRb5bOYLhfotyEeASk1xfUEcT+r9s83cs2SOp6D2FytkDyOCgAAAABJRU5E"
    b"rkJggg==")

#----------------------------------------------------------------------
minimize_inactive = PyEmbeddedImage(
    b"iVBORw0KGgoAAAANSUhEUgAAAA0AAAANCAYAAABy6+R8AAAABHNCSVQICAgIfAhkiAAAANRJ"
    b"REFUKJGdkj1OgkEQhp/ZJSCF0VBYmUBPixfwAtzRS2DvCShMvAGRUJCQkMjOjwV8CwT1C77V"
    b"zGaevO9MViRlrlWnKd7el7HaKGpgpQDg7ng4rkY3Bw/3PZ4nI6lQzpnp0+BPh5fXDwBS8+DR"
    b"HquonUNEOxWHmaOTWSvk6sDJIRqZO0kEO8nrAUmEiN8gC8iCHyBvYqdU01RIizKbr1msy4/R"
    b"xo/9uvbRKYIIJewSSgIderWv0PZrRzcrw9tAVeulwvd7fC62DO5uAJD/fKPUPnKpbzVEY0DN"
    b"U2N1AAAAAElFTkSuQmCC")

#----------------------------------------------------------------------
restore = PyEmbeddedImage(
    b"iVBORw0KGgoAAAANSUhEUgAAAA0AAAANCAYAAABy6+R8AAAABHNCSVQICAgIfAhkiAAAAUlJ"
    b"REFUKJGd0j9LW1EYBvDfvUkM1iaGkohaKJRQv0XJ5FCKg1PnoogUHCwOjnVTx67d2n6Cgq2O"
    b"7oXupdKhUIOQqMRSE733djiXNkoXPcvhvO/z530fThTFBTc9RUjfvM2020zeC5VS3i3kiBg/"
    b"ulQa4oXnUREcd9nZ5fAnvQ5nHaKEYkY14w4eNHm6+M9JfTwQHs5w2WdjHSkRBj2W5uge8Ghi"
    b"iBQl/O6RXDA9gUvWXnJ8xIdPYdQIpXiIVMJpm433tB4H0OcvLMwHxyzoSIeCUEB5QJywvUm/"
    b"T6vFk2dUavxC5Vp6RlDLya+3ODnBK4p3ebfC4D+RK2AM/TP29slSqjVerPJxJ/RG/6LzK00p"
    b"Y2UuqF7gHD2Mo5ELX3H62uZ+k85BWDbJF6/nIZUx1eR7d4hUnWR2mZn61eHztEQp344oN8Lz"
    b"Nn/vD5FAXWAC04u0AAAAAElFTkSuQmCC")

#----------------------------------------------------------------------
restore_inactive = PyEmbeddedImage(
    b"iVBORw0KGgoAAAANSUhEUgAAAA0AAAANCAYAAABy6+R8AAAABHNCSVQICAgIfAhkiAAAAYxJ"
    b"REFUKJGdkr2PTGEUh5/z3ntndmYXIyODiI8oVyGRLTUitpToNCRCJdv7B2gkOrV6Q4hWp6JV"
    b"jXILhWKHeMfcmXvfj3MUk7jbcqrTPPk9J+cn4gr+dUqAz9OFzWth0CtJCiEaWUHNiMnIahQ0"
    b"TEYF16+OpARYto6v35SZj/gaZnNj2UIblZlX6lXg8thzf/dYl7RRFfyYK2fHjskI9m6XZIWs"
    b"4Gtj72VkerAk5SEADiBEWKwEVeHEphASvPoQefq65fRJAdaqmHVQG43vP5XdawX3blZcueh4"
    b"/qjPqeMQsxEUytKoSu30YjZmXlkFeP8p0URj+0LBrZ2KrYGjpiBlR1bpoDYYhz6Ts7H/MTJv"
    b"4O4NWIhj/03AZ0hBCNl1UMjCrxr80nj2oI8qbA2FJ28j774oMQnWGqpH/qQ5s2paHr6IbPSg"
    b"KoTWCYfZcMGhvqHQjGAd5Ehsn/FMD35Ti6NXClnWOiFCkRI7lxKD/pGbzk96PL4zJoUhhvyt"
    b"S7L1bmpUpXBusgmA/E/3/gASuMtl4Uj5YAAAAABJRU5ErkJggg==")

#----------------------------------------------------------------------

fullscreen = PyEmbeddedImage(
    b"iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABHNCSVQICAgIfAhkiAAAActJ"
    b"REFUOI2dk09I02EYx7/v+/7+DDRRYg4EWWYUKAjDSxBhJKuEUUJslwi8BXoaEaIdhpchddgt"
    b"CKIgCIbeYmXaTHboEigZ5GENdCCKfyZKTrf5+72Pp7nf9Lcf4gPP5fl+3i9feJ8HcKrghPD4"
    b"X9c5IdxJvHq4PFKvy3dOjKgltN4f71QU/lGo4kZD250/u5nZtB3H7IY9PRElW6f/ApgPAIiw"
    b"YZpax+rM8x2nNBeqSoLghMBkyIzFYptSSrcdzDnfCofDzd3db9X5+WdHAKAAQEt/9LKaz3zI"
    b"Ag+llG7f7UeQks4YLP787AaAnGdn2PsgupD9NvpVaeuLXmeGMkcwm8rg2tYe4tOLVY+D/i5L"
    b"EtYoQQlvIDqoEKgfoGbGmVEGHt/tQOBWe5WBrut4k05VTAQHA4b4ytTLVyAMSML/smgYBorF"
    b"YlUbxok/TEkmZ/zHfkHc5ACw/GX4E0B+q4GmaVVtNYBEPOPL39v4/iJ/Zg/O8wvWme0iIRLh"
    b"3t9osI6u7GI/lRozTqP2t7DUyVjJlWQlV46VXDl+5FpIX4Jmm8rWYDJkEmNPhSoKqqYUJKcn"
    b"64mxAzu05jHt/UtuN17rJSL6u5IYeV+LOwbQBrHjq9vsKwAAAABJRU5ErkJggg==")

#----------------------------------------------------------------------
reload = PyEmbeddedImage(
    b"iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABHNCSVQICAgIfAhkiAAAApFJ"
    b"REFUOI11k72LXFUUwH/n3vvmvbzZnZnNl7sWI0mIISaIIKYJ2AmbznQWKezSiOm0NaXpAjZu"
    b"kQTMHyBC0JBOCwmyWBrXHaMmuopLdt7Ox3vz3r33WMyyCJscOBwOnPPjfAovEFWEr2kBcIla"
    b"BH1enBxI/Golb7ZGb/kZb6vXkyCI4VeX8G3iFn+Qq1vTFwL0886pcqofNSXvgh41qEGEqBJR"
    b"tl3Gl2ZBbhy6ujs4ACjXuidiET7zDauuhRFnidky0gwxfkz0gq+JJuEbl9kPDn1YPAYwAHqT"
    b"VEfhmq9ZdS4aJBIWThNeuUQ4fpEgbbAGk3dMbMxqqMI1vUkK4AAa8vN+ppdj96ypj59DJv+g"
    b"+TJiFtDuq2iIUO1A1sM8/c7Epr48Nd0voFifAxpzAQ0rdPuEi5/M+6rHaLkDf3yPWzqLOAfT"
    b"f8G20KZeCT5cANaNKoJKX4RExluIr5B8CXp9aCrsbHvuJ2201SGaNiKaaJS+KmJE0KjRIwZm"
    b"BZTP5gvXiHRWiJ3+vFObQdqD7AiIQIxeBHUAorqh1lWiIWP3TyiHkPXgpdfg5Dv4jXvY0S9g"
    b"LGoyRGyFbzb2hxiCfWgdA2M5J5v3sVRodpQg78GRU5B2MX89BT9Bmm1i1MFM7cP9NXZmo83Q"
    b"hNvEokzKAdZaEuNxjx8gj+6RDB9h8iWME/DDMlbh9jFGm/sAuU7UkbsVxuM1KX+fGgokzUlS"
    b"S1o9wbUMRgvYHUxDsbsmtbsl14kHTvnZx0td0vqKW2y/b7vLZ6R9LAfQyfY0DLd+nhWTO9a3"
    b"7h7+dKd43i8I0Hp5kYUrr7vTbyzzZq8tJwB2xvrbj09Yv/uT3/x7zBiYwcEKBEiBfM/aPQUI"
    b"ewk1MPk/4D/OAyg6YvZkywAAAABJRU5ErkJggg==")

#----------------------------------------------------------------------
remove = PyEmbeddedImage(
    b"iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABHNCSVQICAgIfAhkiAAAApVJ"
    b"REFUOI2lkUtIVHEUxr//vf9778x4J8d8DDaODjo+mBzLKFJJJbVWFdmiVaEtehBYi2hVENXK"
    b"XS0iC6JNFkbkInwVQeoiiLAHtlAhW6TjTPnA9DreO/d/WjjOIkiDDnxwFuc7fOd3gP8s+bmD"
    b"118+UPGmiagsNL88UJqb62gLhTrP1tVdmY5G334zjOiGG574XF00/IjmHt6lO+mujvvb/J1L"
    b"3d1k9vRQk9fbsWkCX9ya/DIxUdVQ2+gt9Obt3lG1N6ykp+NGe/vnl5OT15aEiGx6x03g4GBl"
    b"IEGX2ojaLlBXeflKXWbm/n9i8BTILivgV4vkuXC0/x0W3n9C3tYMnsjOXpmyrMEfhmFutIC7"
    b"s3C9Jpw4vjAO3Ha6zS2Ki11cNZXz+fnnXkUiMbuy8l6OrreYpikxxgVRQmKMyaqa9mJo6PUH"
    b"PhTc6Q9gDvM1u1BxuFVxKRK+9/UhOjaOiCzL24uLHzcfOlLvcGoAGDRNgSxz9PcPnIrHf9Xy"
    b"r6FqHm85gXBFCNUeDwMAo7EB77uewdHxIBLI85c3HzsKp9MJxhgYYwCAmZmZwOjoWBp3EbJz"
    b"SoPQPR5YpglbCLhcaQgEg/Do6XsWF1elkZGPUFUVkiRB0zTouo7p6Rh03bOPBwKBUIbbDQAg"
    b"AIwxmKYJb1YWTp9pPckkSYrFfoKIUgKAkpIgDMO6xX0+n+R0OSGESJG1LAv5BX4UBQulRCIB"
    b"y7Jg2zaEsGHbAkQCmqZifn7JwYlk+vM1jDEIIWAYBoQQSbNIiYggxCqEYDZXFDVlWge03v9N"
    b"azMEzjm4qqp83STLUvJGAmMEYM1AxFLpkgggSYCiaDKPRhenenuHddNM0BokgMhODq+DQyo6"
    b"QLBtgiwzNju7svwbnlAlxKIQCyQAAAAASUVORK5CYII=")

#----------------------------------------------------------------------
sort = PyEmbeddedImage(
    b"iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABHNCSVQICAgIfAhkiAAAAMdJ"
    b"REFUOI2VklEOgyAMhv+iR1jmdfQWHt1dQXA+dI9K97BpaIFE/4SQAv36UwC5BukAROxaOl7T"
    b"pPYdbmpZVxUrgMRNyLUkcZMqIIQ64IpCWMqAo6qdrbyfVdymAbmWLDAH+LKDq6oC0uql+FDw"
    b"uonnFWLcM8vONRkkLBWATSgBAeBt/gH9fp9WjLvY6t3zIZIiCZjnQFkTS8kA0PcDmBn8YTAz"
    b"hn7IHdSSD0lyLfqfOx3Y5FIPxnFUs3Jw9RUk7kLJerGJd/QF7eJxBTVIT38AAAAASUVORK5C"
    b"YII=")

#----------------------------------------------------------------------
superscript = PyEmbeddedImage(
    b"iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABHNCSVQICAgIfAhkiAAAAYFJ"
    b"REFUOI3VkTtPAlEQhUfW4INCxMpigcTEVhMbCxO2NDZgg6UUJpSIzZZS+AO201gYaa1MbEy2"
    b"EAosbCQxxFdUsKLjIffOndl1sTBYiEFjYzzVmWTmy8wZgH+voZ82ru0+RfWpkeOJUV/04lpY"
    b"J+ZMDgDA91NAwD9s3T9Q4vyqZS3Mjm//Ytl3pfZr5Y2D52qvHu4Z0zQLrusCEQEzAxGllFKH"
    b"iAiICLZtGzGzkhPoQvUWE725jxMcx7GYeV4pFSOicj6fr0opC1LKKjOnlrYqCZ8G0bvHtsHk"
    b"BOfWL6MAn0JMp9OGUuqMmaHT6WSVUgnbtg0AgJWdm4I+PRZzX7vwIl9bR5szwT4AAEAymbQc"
    b"x8kIIYCIJovFYnNQJn1fIKKcEAI8z4N2u537LtQ+gJTyWAiRRUTodruZSCRiDAJoPROPx4O6"
    b"ru8hYqFUKlmBQGDS7/cvNpvNVU3TTomoPhAQDodPETEopVShUKgupUw1Go0aM9eZeRkAyp7n"
    b"fQn5W70BAIHMJSEYEtgAAAAASUVORK5CYII=")
#----------------------------------------------------------------------

# Custom pane bitmaps reference
#                      bitmap  button id       active  maximize
CUSTOM_PANE_BITMAPS = [(close, aui.AUI_BUTTON_CLOSE, True, False),
                       (close_inactive, aui.AUI_BUTTON_CLOSE, False, False),
                       (minimize, aui.AUI_BUTTON_MINIMIZE, True, False),
                       (minimize_inactive, aui.AUI_BUTTON_MINIMIZE, False, False),
                       (maximize, aui.AUI_BUTTON_MAXIMIZE_RESTORE, True, True),
                       (maximize_inactive, aui.AUI_BUTTON_MAXIMIZE_RESTORE, False, True),
                       (restore, aui.AUI_BUTTON_MAXIMIZE_RESTORE, True, False),
                       (restore_inactive, aui.AUI_BUTTON_MAXIMIZE_RESTORE, False, False)]

#----------------------------------------------------------------------
# Custom buttons in tab area
#
CUSTOM_TAB_BUTTONS = {"Left": [(sort, aui.AUI_BUTTON_CUSTOM1),
                               (superscript, aui.AUI_BUTTON_CUSTOM2)],
                      "Right": [(fullscreen, aui.AUI_BUTTON_CUSTOM3),
                                (remove, aui.AUI_BUTTON_CUSTOM4),
                                (reload, aui.AUI_BUTTON_CUSTOM5)]
                      }

#----------------------------------------------------------------------

# Define a translation function
_ = wx.GetTranslation


ID_CreateTree = wx.ID_HIGHEST + 1
ID_CreateGrid = ID_CreateTree + 1
ID_CreateText = ID_CreateTree + 2
ID_CreateHTML = ID_CreateTree + 3
ID_CreateNotebook = ID_CreateTree + 4
ID_CreateSizeReport = ID_CreateTree + 5
ID_GridContent = ID_CreateTree + 6
ID_TextContent = ID_CreateTree + 7
ID_TreeContent = ID_CreateTree + 8
ID_HTMLContent = ID_CreateTree + 9
ID_NotebookContent = ID_CreateTree + 10
ID_SizeReportContent = ID_CreateTree + 11
ID_SwitchPane = ID_CreateTree + 12
ID_CreatePerspective = ID_CreateTree + 13
ID_CopyPerspectiveCode = ID_CreateTree + 14
ID_CreateNBPerspective = ID_CreateTree + 15
ID_CopyNBPerspectiveCode = ID_CreateTree + 16
ID_AllowFloating = ID_CreateTree + 17
ID_AllowActivePane = ID_CreateTree + 18
ID_TransparentHint = ID_CreateTree + 19
ID_VenetianBlindsHint = ID_CreateTree + 20
ID_RectangleHint = ID_CreateTree + 21
ID_NoHint = ID_CreateTree + 22
ID_HintFade = ID_CreateTree + 23
ID_NoVenetianFade = ID_CreateTree + 24
ID_TransparentDrag = ID_CreateTree + 25
ID_NoGradient = ID_CreateTree + 26
ID_VerticalGradient = ID_CreateTree + 27
ID_HorizontalGradient = ID_CreateTree + 28
ID_LiveUpdate = ID_CreateTree + 29
ID_AnimateFrames = ID_CreateTree + 30
ID_PaneIcons = ID_CreateTree + 31
ID_TransparentPane = ID_CreateTree + 32
ID_DefaultDockArt = ID_CreateTree + 33
ID_ModernDockArt = ID_CreateTree + 34
ID_SnapToScreen = ID_CreateTree + 35
ID_SnapPanes = ID_CreateTree + 36
ID_FlyOut = ID_CreateTree + 37
ID_CustomPaneButtons = ID_CreateTree + 38
ID_Settings = ID_CreateTree + 39
ID_CustomizeToolbar = ID_CreateTree + 40
ID_DropDownToolbarItem = ID_CreateTree + 41
ID_MinimizePosSmart = ID_CreateTree + 42
ID_MinimizePosTop = ID_CreateTree + 43
ID_MinimizePosLeft = ID_CreateTree + 44
ID_MinimizePosRight = ID_CreateTree + 45
ID_MinimizePosBottom = ID_CreateTree + 46
ID_MinimizeCaptSmart = ID_CreateTree + 47
ID_MinimizeCaptHorz = ID_CreateTree + 48
ID_MinimizeCaptHide = ID_CreateTree + 49
ID_NotebookNoCloseButton = ID_CreateTree + 50
ID_NotebookCloseButton = ID_CreateTree + 51
ID_NotebookCloseButtonAll = ID_CreateTree + 52
ID_NotebookCloseButtonActive = ID_CreateTree + 53
ID_NotebookCloseOnLeft = ID_CreateTree + 54
ID_NotebookAllowTabMove = ID_CreateTree + 55
ID_NotebookAllowTabExternalMove = ID_CreateTree + 56
ID_NotebookAllowTabSplit = ID_CreateTree + 57
ID_NotebookTabFloat = ID_CreateTree + 58
ID_NotebookTabDrawDnd = ID_CreateTree + 59
ID_NotebookDclickUnsplit = ID_CreateTree + 60
ID_NotebookWindowList = ID_CreateTree + 61
ID_NotebookScrollButtons = ID_CreateTree + 62
ID_NotebookTabFixedWidth = ID_CreateTree + 63
ID_NotebookArtGloss = ID_CreateTree + 64
ID_NotebookArtSimple = ID_CreateTree + 65
ID_NotebookArtVC71 = ID_CreateTree + 66
ID_NotebookArtFF2 = ID_CreateTree + 67
ID_NotebookArtVC8 = ID_CreateTree + 68
ID_NotebookArtChrome = ID_CreateTree + 69
ID_NotebookAlignTop = ID_CreateTree + 70
ID_NotebookAlignBottom = ID_CreateTree + 71
ID_NotebookHideSingle = ID_CreateTree + 72
ID_NotebookSmartTab = ID_CreateTree + 73
ID_NotebookUseImagesDropDown = ID_CreateTree + 74
ID_NotebookCustomButtons = ID_CreateTree + 75
ID_NotebookMinMaxWidth = ID_CreateTree + 76

ID_SampleItem = ID_CreateTree + 77
ID_StandardGuides = ID_CreateTree + 78
ID_AeroGuides = ID_CreateTree + 79
ID_WhidbeyGuides = ID_CreateTree + 80
ID_NotebookPreview = ID_CreateTree + 81
ID_PreviewMinimized = ID_CreateTree + 82

ID_SmoothDocking = ID_CreateTree + 83
ID_NativeMiniframes = ID_CreateTree + 84

ID_FirstPerspective = ID_CreatePerspective + 1000
ID_FirstNBPerspective = ID_CreateNBPerspective + 10000

ID_PaneBorderSize = ID_SampleItem + 100
ID_SashSize = ID_PaneBorderSize + 2
ID_CaptionSize = ID_PaneBorderSize + 3
ID_BackgroundColour = ID_PaneBorderSize + 4
ID_SashColour = ID_PaneBorderSize + 5
ID_InactiveCaptionColour = ID_PaneBorderSize + 6
ID_InactiveCaptionGradientColour = ID_PaneBorderSize + 7
ID_InactiveCaptionTextColour = ID_PaneBorderSize + 8
ID_ActiveCaptionColour = ID_PaneBorderSize + 9
ID_ActiveCaptionGradientColour = ID_PaneBorderSize + 10
ID_ActiveCaptionTextColour = ID_PaneBorderSize + 11
ID_BorderColour = ID_PaneBorderSize + 12
ID_GripperColour = ID_PaneBorderSize + 13
ID_SashGrip = ID_PaneBorderSize + 14
ID_HintColour = ID_PaneBorderSize + 15

ID_VetoTree = ID_PaneBorderSize + 16
ID_VetoText = ID_PaneBorderSize + 17
ID_NotebookMultiLine = ID_PaneBorderSize + 18

# -- SizeReportCtrl --
# (a utility control that always reports it's client size)

class SizeReportCtrl(wx.Control):

    def __init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition,
                size=wx.DefaultSize, mgr=None):

        wx.Control.__init__(self, parent, id, pos, size, style=wx.NO_BORDER)
        self._mgr = mgr

        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground)
        self.Bind(wx.EVT_SIZE, self.OnSize)


    def OnPaint(self, event):

        dc = wx.PaintDC(self)
        size = self.GetClientSize()

        s = "Size: %d x %d"%(size.x, size.y)

        dc.SetFont(wx.NORMAL_FONT)
        w, height = dc.GetTextExtent(s)
        height += 3
        dc.SetBrush(wx.WHITE_BRUSH)
        dc.SetPen(wx.WHITE_PEN)
        dc.DrawRectangle(0, 0, size.x, size.y)
        dc.SetPen(wx.LIGHT_GREY_PEN)
        dc.DrawLine(0, 0, size.x, size.y)
        dc.DrawLine(0, size.y, size.x, 0)
        dc.DrawText(s, (size.x-w)/2, (size.y-height*5)/2)

        if self._mgr:

            pi = self._mgr.GetPane(self)

            s = "Layer: %d"%pi.dock_layer
            w, h = dc.GetTextExtent(s)
            dc.DrawText(s, (size.x-w)/2, ((size.y-(height*5))/2)+(height*1))

            s = "Dock: %d Row: %d"%(pi.dock_direction, pi.dock_row)
            w, h = dc.GetTextExtent(s)
            dc.DrawText(s, (size.x-w)/2, ((size.y-(height*5))/2)+(height*2))

            s = "Position: %d"%pi.dock_pos
            w, h = dc.GetTextExtent(s)
            dc.DrawText(s, (size.x-w)/2, ((size.y-(height*5))/2)+(height*3))

            s = "Proportion: %d"%pi.dock_proportion
            w, h = dc.GetTextExtent(s)
            dc.DrawText(s, (size.x-w)/2, ((size.y-(height*5))/2)+(height*4))


    def OnEraseBackground(self, event):

        pass


    def OnSize(self, event):

        self.Refresh()


class SettingsPanel(wx.Panel):

    def __init__(self, parent, frame):

        wx.Panel.__init__(self, parent)
        self._frame = frame

        s1 = wx.BoxSizer(wx.HORIZONTAL)
        self._border_size = wx.SpinCtrl(self, ID_PaneBorderSize, "%d"%frame.GetDockArt().GetMetric(aui.AUI_DOCKART_PANE_BORDER_SIZE),
                                        wx.DefaultPosition, wx.Size(50, 20), wx.SP_ARROW_KEYS, 0, 100,
                                        frame.GetDockArt().GetMetric(aui.AUI_DOCKART_PANE_BORDER_SIZE))
        s1.Add((1, 1), 1, wx.EXPAND)
        s1.Add(wx.StaticText(self, -1, "Pane Border Size:"))
        s1.Add(self._border_size)
        s1.Add((1, 1), 1, wx.EXPAND)
        s1.SetItemMinSize(1, (180, 20))

        s2 = wx.BoxSizer(wx.HORIZONTAL)
        self._sash_size = wx.SpinCtrl(self, ID_SashSize, "%d"%frame.GetDockArt().GetMetric(aui.AUI_DOCKART_SASH_SIZE), wx.DefaultPosition,
                                      wx.Size(50, 20), wx.SP_ARROW_KEYS, 0, 100, frame.GetDockArt().GetMetric(aui.AUI_DOCKART_SASH_SIZE))
        s2.Add((1, 1), 1, wx.EXPAND)
        s2.Add(wx.StaticText(self, -1, "Sash Size:"))
        s2.Add(self._sash_size)
        s2.Add((1, 1), 1, wx.EXPAND)
        s2.SetItemMinSize(1, (180, 20))

        s3 = wx.BoxSizer(wx.HORIZONTAL)
        self._caption_size = wx.SpinCtrl(self, ID_CaptionSize, "%d"%frame.GetDockArt().GetMetric(aui.AUI_DOCKART_CAPTION_SIZE),
                                         wx.DefaultPosition, wx.Size(50, 20), wx.SP_ARROW_KEYS, 0, 100, frame.GetDockArt().GetMetric(aui.AUI_DOCKART_CAPTION_SIZE))
        s3.Add((1, 1), 1, wx.EXPAND)
        s3.Add(wx.StaticText(self, -1, "Caption Size:"))
        s3.Add(self._caption_size)
        s3.Add((1, 1), 1, wx.EXPAND)
        s3.SetItemMinSize(1, (180, 20))

        b = self.CreateColourBitmap(wx.BLACK)

        s4 = wx.BoxSizer(wx.HORIZONTAL)
        self._background_colour = wx.BitmapButton(self, ID_BackgroundColour, b, wx.DefaultPosition, wx.Size(50, 25))
        s4.Add((1, 1), 1, wx.EXPAND)
        s4.Add(wx.StaticText(self, -1, "Background Colour:"))
        s4.Add(self._background_colour)
        s4.Add((1, 1), 1, wx.EXPAND)
        s4.SetItemMinSize(1, (180, 20))

        s5 = wx.BoxSizer(wx.HORIZONTAL)
        self._sash_colour = wx.BitmapButton(self, ID_SashColour, b, wx.DefaultPosition, wx.Size(50, 25))
        s5.Add((1, 1), 1, wx.EXPAND)
        s5.Add(wx.StaticText(self, -1, "Sash Colour:"))
        s5.Add(self._sash_colour)
        s5.Add((1, 1), 1, wx.EXPAND)
        s5.SetItemMinSize(1, (180, 20))

        s6 = wx.BoxSizer(wx.HORIZONTAL)
        self._inactive_caption_colour = wx.BitmapButton(self, ID_InactiveCaptionColour, b, wx.DefaultPosition, wx.Size(50, 25))
        s6.Add((1, 1), 1, wx.EXPAND)
        s6.Add(wx.StaticText(self, -1, "Normal Caption:"))
        s6.Add(self._inactive_caption_colour)
        s6.Add((1, 1), 1, wx.EXPAND)
        s6.SetItemMinSize(1, (180, 20))

        s7 = wx.BoxSizer(wx.HORIZONTAL)
        self._inactive_caption_gradient_colour = wx.BitmapButton(self, ID_InactiveCaptionGradientColour, b, wx.DefaultPosition, wx.Size(50, 25))
        s7.Add((1, 1), 1, wx.EXPAND)
        s7.Add(wx.StaticText(self, -1, "Normal Caption Gradient:"))
        s7.Add(self._inactive_caption_gradient_colour)
        s7.Add((1, 1), 1, wx.EXPAND)
        s7.SetItemMinSize(1, (180, 20))

        s8 = wx.BoxSizer(wx.HORIZONTAL)
        self._inactive_caption_text_colour = wx.BitmapButton(self, ID_InactiveCaptionTextColour, b, wx.DefaultPosition, wx.Size(50, 25))
        s8.Add((1, 1), 1, wx.EXPAND)
        s8.Add(wx.StaticText(self, -1, "Normal Caption Text:"))
        s8.Add(self._inactive_caption_text_colour)
        s8.Add((1, 1), 1, wx.EXPAND)
        s8.SetItemMinSize(1, (180, 20))

        s9 = wx.BoxSizer(wx.HORIZONTAL)
        self._active_caption_colour = wx.BitmapButton(self, ID_ActiveCaptionColour, b, wx.DefaultPosition, wx.Size(50, 25))
        s9.Add((1, 1), 1, wx.EXPAND)
        s9.Add(wx.StaticText(self, -1, "Active Caption:"))
        s9.Add(self._active_caption_colour)
        s9.Add((1, 1), 1, wx.EXPAND)
        s9.SetItemMinSize(1, (180, 20))

        s10 = wx.BoxSizer(wx.HORIZONTAL)
        self._active_caption_gradient_colour = wx.BitmapButton(self, ID_ActiveCaptionGradientColour, b, wx.DefaultPosition, wx.Size(50, 25))
        s10.Add((1, 1), 1, wx.EXPAND)
        s10.Add(wx.StaticText(self, -1, "Active Caption Gradient:"))
        s10.Add(self._active_caption_gradient_colour)
        s10.Add((1, 1), 1, wx.EXPAND)
        s10.SetItemMinSize(1, (180, 20))

        s11 = wx.BoxSizer(wx.HORIZONTAL)
        self._active_caption_text_colour = wx.BitmapButton(self, ID_ActiveCaptionTextColour, b, wx.DefaultPosition, wx.Size(50, 25))
        s11.Add((1, 1), 1, wx.EXPAND)
        s11.Add(wx.StaticText(self, -1, "Active Caption Text:"))
        s11.Add(self._active_caption_text_colour)
        s11.Add((1, 1), 1, wx.EXPAND)
        s11.SetItemMinSize(1, (180, 20))

        s12 = wx.BoxSizer(wx.HORIZONTAL)
        self._border_colour = wx.BitmapButton(self, ID_BorderColour, b, wx.DefaultPosition, wx.Size(50, 25))
        s12.Add((1, 1), 1, wx.EXPAND)
        s12.Add(wx.StaticText(self, -1, "Border Colour:"))
        s12.Add(self._border_colour)
        s12.Add((1, 1), 1, wx.EXPAND)
        s12.SetItemMinSize(1, (180, 20))

        s13 = wx.BoxSizer(wx.HORIZONTAL)
        self._gripper_colour = wx.BitmapButton(self, ID_GripperColour, b, wx.DefaultPosition, wx.Size(50,25))
        s13.Add((1, 1), 1, wx.EXPAND)
        s13.Add(wx.StaticText(self, -1, "Gripper Colour:"))
        s13.Add(self._gripper_colour)
        s13.Add((1, 1), 1, wx.EXPAND)
        s13.SetItemMinSize(1, (180, 20))

        s14 = wx.BoxSizer(wx.HORIZONTAL)
        self._sash_grip = wx.CheckBox(self, ID_SashGrip, "", wx.DefaultPosition, wx.Size(50,20))
        s14.Add((1, 1), 1, wx.EXPAND)
        s14.Add(wx.StaticText(self, -1, "Draw Sash Grip:"))
        s14.Add(self._sash_grip)
        s14.Add((1, 1), 1, wx.EXPAND)
        s14.SetItemMinSize(1, (180, 20))

        s15 = wx.BoxSizer(wx.HORIZONTAL)
        self._hint_colour = wx.BitmapButton(self, ID_HintColour, b, wx.DefaultPosition, wx.Size(50,25))
        s15.Add((1, 1), 1, wx.EXPAND)
        s15.Add(wx.StaticText(self, -1, "Hint Window Colour:"))
        s15.Add(self._hint_colour)
        s15.Add((1, 1), 1, wx.EXPAND)
        s15.SetItemMinSize(1, (180, 20))

        grid_sizer = wx.GridSizer(rows=0, cols=2, vgap=5, hgap=5)
        grid_sizer.SetHGap(5)
        grid_sizer.Add(s1)
        grid_sizer.Add(s4)
        grid_sizer.Add(s2)
        grid_sizer.Add(s5)
        grid_sizer.Add(s3)
        grid_sizer.Add(s13)
        grid_sizer.Add(s14)
        grid_sizer.Add((1, 1))
        grid_sizer.Add(s12)
        grid_sizer.Add(s6)
        grid_sizer.Add(s9)
        grid_sizer.Add(s7)
        grid_sizer.Add(s10)
        grid_sizer.Add(s8)
        grid_sizer.Add(s11)
        grid_sizer.Add(s15)

        cont_sizer = wx.BoxSizer(wx.VERTICAL)
        cont_sizer.Add(grid_sizer, 1, wx.EXPAND | wx.ALL, 5)
        self.SetSizer(cont_sizer)
        self.GetSizer().SetSizeHints(self)

        self._border_size.SetValue(frame.GetDockArt().GetMetric(aui.AUI_DOCKART_PANE_BORDER_SIZE))
        self._sash_size.SetValue(frame.GetDockArt().GetMetric(aui.AUI_DOCKART_SASH_SIZE))
        self._caption_size.SetValue(frame.GetDockArt().GetMetric(aui.AUI_DOCKART_CAPTION_SIZE))
        self._sash_grip.SetValue(frame.GetDockArt().GetMetric(aui.AUI_DOCKART_DRAW_SASH_GRIP))

        self.UpdateColours()

        self.Bind(wx.EVT_SPINCTRL, self.OnPaneBorderSize, id=ID_PaneBorderSize)
        self.Bind(wx.EVT_SPINCTRL, self.OnSashSize, id=ID_SashSize)
        self.Bind(wx.EVT_SPINCTRL, self.OnCaptionSize, id=ID_CaptionSize)
        self.Bind(wx.EVT_CHECKBOX, self.OnDrawSashGrip, id=ID_SashGrip)
        self.Bind(wx.EVT_BUTTON, self.OnSetColour, id=ID_BackgroundColour)
        self.Bind(wx.EVT_BUTTON, self.OnSetColour, id=ID_SashColour)
        self.Bind(wx.EVT_BUTTON, self.OnSetColour, id=ID_InactiveCaptionColour)
        self.Bind(wx.EVT_BUTTON, self.OnSetColour, id=ID_InactiveCaptionGradientColour)
        self.Bind(wx.EVT_BUTTON, self.OnSetColour, id=ID_InactiveCaptionTextColour)
        self.Bind(wx.EVT_BUTTON, self.OnSetColour, id=ID_ActiveCaptionColour)
        self.Bind(wx.EVT_BUTTON, self.OnSetColour, id=ID_ActiveCaptionGradientColour)
        self.Bind(wx.EVT_BUTTON, self.OnSetColour, id=ID_ActiveCaptionTextColour)
        self.Bind(wx.EVT_BUTTON, self.OnSetColour, id=ID_BorderColour)
        self.Bind(wx.EVT_BUTTON, self.OnSetColour, id=ID_GripperColour)
        self.Bind(wx.EVT_BUTTON, self.OnSetColour, id=ID_HintColour)


    def CreateColourBitmap(self, c):

        image = wx.Image(25, 14)
        for x in range(25):
            for y in range(14):
                pixcol = c
                if x == 0 or x == 24 or y == 0 or y == 13:
                    pixcol = wx.BLACK

                image.SetRGB(wx.Rect(wx.Size(25, 14)), pixcol.Red(), pixcol.Green(), pixcol.Blue())

        return image.ConvertToBitmap()


    def UpdateColours(self):

        bk = self._frame.GetDockArt().GetColour(aui.AUI_DOCKART_BACKGROUND_COLOUR)
        self._background_colour.SetBitmapLabel(self.CreateColourBitmap(bk))

        cap = self._frame.GetDockArt().GetColour(aui.AUI_DOCKART_INACTIVE_CAPTION_COLOUR)
        self._inactive_caption_colour.SetBitmapLabel(self.CreateColourBitmap(cap))

        capgrad = self._frame.GetDockArt().GetColour(aui.AUI_DOCKART_INACTIVE_CAPTION_GRADIENT_COLOUR)
        self._inactive_caption_gradient_colour.SetBitmapLabel(self.CreateColourBitmap(capgrad))

        captxt = self._frame.GetDockArt().GetColour(aui.AUI_DOCKART_INACTIVE_CAPTION_TEXT_COLOUR)
        self._inactive_caption_text_colour.SetBitmapLabel(self.CreateColourBitmap(captxt))

        acap = self._frame.GetDockArt().GetColour(aui.AUI_DOCKART_ACTIVE_CAPTION_COLOUR)
        self._active_caption_colour.SetBitmapLabel(self.CreateColourBitmap(acap))

        acapgrad = self._frame.GetDockArt().GetColour(aui.AUI_DOCKART_ACTIVE_CAPTION_GRADIENT_COLOUR)
        self._active_caption_gradient_colour.SetBitmapLabel(self.CreateColourBitmap(acapgrad))

        acaptxt = self._frame.GetDockArt().GetColour(aui.AUI_DOCKART_ACTIVE_CAPTION_TEXT_COLOUR)
        self._active_caption_text_colour.SetBitmapLabel(self.CreateColourBitmap(acaptxt))

        sash = self._frame.GetDockArt().GetColour(aui.AUI_DOCKART_SASH_COLOUR)
        self._sash_colour.SetBitmapLabel(self.CreateColourBitmap(sash))

        border = self._frame.GetDockArt().GetColour(aui.AUI_DOCKART_BORDER_COLOUR)
        self._border_colour.SetBitmapLabel(self.CreateColourBitmap(border))

        gripper = self._frame.GetDockArt().GetColour(aui.AUI_DOCKART_GRIPPER_COLOUR)
        self._gripper_colour.SetBitmapLabel(self.CreateColourBitmap(gripper))

        hint = self._frame.GetDockArt().GetColour(aui.AUI_DOCKART_HINT_WINDOW_COLOUR)
        self._hint_colour.SetBitmapLabel(self.CreateColourBitmap(hint))


    def OnPaneBorderSize(self, event):

        self._frame.GetDockArt().SetMetric(aui.AUI_DOCKART_PANE_BORDER_SIZE,
                                           event.GetInt())
        self._frame.DoUpdate()


    def OnSashSize(self, event):

        self._frame.GetDockArt().SetMetric(aui.AUI_DOCKART_SASH_SIZE,
                                           event.GetInt())
        self._frame.DoUpdate()


    def OnCaptionSize(self, event):

        self._frame.GetDockArt().SetMetric(aui.AUI_DOCKART_CAPTION_SIZE,
                                           event.GetInt())
        self._frame.DoUpdate()


    def OnDrawSashGrip(self, event):

        self._frame.GetDockArt().SetMetric(aui.AUI_DOCKART_DRAW_SASH_GRIP,
                                           event.GetInt())
        self._frame.DoUpdate()


    def OnSetColour(self, event):

        dlg = wx.ColourDialog(self._frame)
        dlg.SetTitle("Colour Picker")

        if dlg.ShowModal() != wx.ID_OK:
            return

        evId = event.GetId()
        if evId == ID_BackgroundColour:
            var = aui.AUI_DOCKART_BACKGROUND_COLOUR
        elif evId == ID_SashColour:
            var = aui.AUI_DOCKART_SASH_COLOUR
        elif evId == ID_InactiveCaptionColour:
            var = aui.AUI_DOCKART_INACTIVE_CAPTION_COLOUR
        elif evId == ID_InactiveCaptionGradientColour:
            var = aui.AUI_DOCKART_INACTIVE_CAPTION_GRADIENT_COLOUR
        elif evId == ID_InactiveCaptionTextColour:
            var = aui.AUI_DOCKART_INACTIVE_CAPTION_TEXT_COLOUR
        elif evId == ID_ActiveCaptionColour:
            var = aui.AUI_DOCKART_ACTIVE_CAPTION_COLOUR
        elif evId == ID_ActiveCaptionGradientColour:
            var = aui.AUI_DOCKART_ACTIVE_CAPTION_GRADIENT_COLOUR
        elif evId == ID_ActiveCaptionTextColour:
            var = aui.AUI_DOCKART_ACTIVE_CAPTION_TEXT_COLOUR
        elif evId == ID_BorderColour:
            var = aui.AUI_DOCKART_BORDER_COLOUR
        elif evId == ID_GripperColour:
            var = aui.AUI_DOCKART_GRIPPER_COLOUR
        elif evId == ID_HintColour:
            var = aui.AUI_DOCKART_HINT_WINDOW_COLOUR
        else:
            return

        self._frame.GetDockArt().SetColour(var, dlg.GetColourData().GetColour())
        self._frame.DoUpdate()
        self.UpdateColours()


# ---------------------------------------------------------------------------- #
# Class ProgressGauge
# ---------------------------------------------------------------------------- #

class ProgressGauge(wx.Window):
    """ This class provides a visual alternative for wx.Gauge."""

    def __init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition, size=(-1,30)):
        """ Default class constructor. """

        wx.Window.__init__(self, parent, id, pos, size, style=wx.BORDER_NONE)

        self._value = 0
        self._steps = 16
        self._pos = 0
        self._current = 0
        self._gaugeproportion = 0.4
        self._startTime = time.time()

        self._bottomStartColour = wx.GREEN
        rgba = self._bottomStartColour.Red(), self._bottomStartColour.Green(), \
               self._bottomStartColour.Blue(), self._bottomStartColour.Alpha()
        self._bottomEndColour = self.LightColour(self._bottomStartColour, 30)
        self._topStartColour = self.LightColour(self._bottomStartColour, 80)
        self._topEndColour = self.LightColour(self._bottomStartColour, 40)

        self._background = wx.Brush(wx.WHITE, wx.BRUSHSTYLE_SOLID)

        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground)


    def OnEraseBackground(self, event):
        """ Handles the wx.EVT_ERASE_BACKGROUND event for ProgressGauge. """

        pass


    def OnPaint(self, event):
        """ Handles the wx.EVT_PAINT event for ProgressGauge. """

        dc = wx.BufferedPaintDC(self)
        dc.SetBackground(self._background)
        dc.SetBackground(wx.WHITE_BRUSH)
        dc.Clear()

        xsize, ysize = self.GetClientSize()
        interval = xsize/float(self._steps)

        self._pos = interval*self._value

        status = self._current/(self._steps - int((self._gaugeproportion*xsize/interval)))

        if status%2 == 0:
            increment = 1
        else:
            increment = -1

        self._value = self._value + increment
        self._current = self._current + 1

        self.DrawProgress(dc, xsize, ysize, increment)

        dc.SetBrush(wx.TRANSPARENT_BRUSH)
        dc.SetPen(wx.Pen(wx.SystemSettings.GetColour(wx.SYS_COLOUR_GRADIENTINACTIVECAPTION)))
        dc.DrawRectangle(self.GetClientRect())


    def LightColour(self, colour, percent):
        """
        Return light contrast of colour. The colour returned is from the scale of
        colour -> white. The percent determines how light the colour will be.
        Percent = 100 return white, percent = 0 returns colour.
        """

        end_colour = wx.WHITE
        rd = end_colour.Red() - colour.Red()
        gd = end_colour.Green() - colour.Green()
        bd = end_colour.Blue() - colour.Blue()
        high = 100

        # We take the percent way of the colour from colour -> white
        i = percent
        r = colour.Red() + ((i*rd*100)/high)/100
        g = colour.Green() + ((i*gd*100)/high)/100
        b = colour.Blue() + ((i*bd*100)/high)/100

        return wx.Colour(r, g, b)


    def DrawProgress(self, dc, xsize, ysize, increment):
        """ Actually draws the sliding bar. """

        interval = self._gaugeproportion*xsize
        gc = wx.GraphicsContext.Create(dc)

        clientRect = self.GetClientRect()
        gradientRect = wx.Rect(*clientRect)

        x, y, width, height = clientRect
        x, width = self._pos, interval

        gradientRect.SetHeight(gradientRect.GetHeight()/2)
        topStart, topEnd = self._topStartColour, self._topEndColour

        rc1 = wx.Rect(x, y, width, height/2)
        path1 = self.GetPath(gc, rc1, 8)
        br1 = gc.CreateLinearGradientBrush(x, y, x, y+height/2, topStart, topEnd)
        gc.SetBrush(br1)
        gc.FillPath(path1) #draw main

        path4 = gc.CreatePath()
        path4.AddRectangle(x, y+height/2-8, width, 8)
        path4.CloseSubpath()
        gc.SetBrush(br1)
        gc.FillPath(path4)

        gradientRect.Offset((0, gradientRect.GetHeight()))

        bottomStart, bottomEnd = self._bottomStartColour, self._bottomEndColour

        rc3 = wx.Rect(x, y+height/2, width, height/2)
        path3 = self.GetPath(gc, rc3, 8)
        br3 = gc.CreateLinearGradientBrush(x, y+height/2, x, y+height, bottomStart, bottomEnd)
        gc.SetBrush(br3)
        gc.FillPath(path3) #draw main

        path4 = gc.CreatePath()
        path4.AddRectangle(x, y+height/2, width, 8)
        path4.CloseSubpath()
        gc.SetBrush(br3)
        gc.FillPath(path4)


    def GetPath(self, gc, rc, r):
        """ Returns a rounded GraphicsPath. """

        x, y, w, h = rc
        path = gc.CreatePath()
        path.AddRoundedRectangle(x, y, w, h, r)
        path.CloseSubpath()
        return path



    def Pulse(self):
        """ Updates the gauge with a new value. """

        self.Refresh()


class AuiFrame(wx.Frame):

    def __init__(self, parent, id=wx.ID_ANY, title="", pos= wx.DefaultPosition,
                 size=wx.DefaultSize, style=wx.DEFAULT_FRAME_STYLE|wx.SUNKEN_BORDER, log=None):

        wx.Frame.__init__(self, parent, id, title, pos, size, style)

        self._mgr = aui.AuiManager()

        # tell AuiManager to manage this frame
        self._mgr.SetManagedWindow(self)

        # set frame icon
        self.SetIcon(images.Mondrian.GetIcon())

        # set up default notebook style
        self._notebook_style = aui.AUI_NB_DEFAULT_STYLE | aui.AUI_NB_TAB_EXTERNAL_MOVE | wx.NO_BORDER
        self._notebook_theme = 0
        # Attributes
        self._textCount = 1
        self._transparency = 255
        self._snapped = False
        self._custom_pane_buttons = False
        self._custom_tab_buttons = False
        self._pane_icons = False
        self._veto_tree = self._veto_text = False

        self.log = log

        self.CreateStatusBar()
        self.GetStatusBar().SetStatusText("Ready")

        self.BuildPanes()
        self.CreateMenuBar()
        self.BindEvents()


    def CreateMenuBar(self):

        # create menu
        mb = wx.MenuBar()

        file_menu = wx.Menu()
        file_menu.Append(wx.ID_EXIT, "Exit")

        view_menu = wx.Menu()
        view_menu.Append(ID_CreateText, "Create Text Control")
        view_menu.Append(ID_CreateHTML, "Create HTML Control")
        view_menu.Append(ID_CreateTree, "Create Tree")
        view_menu.Append(ID_CreateGrid, "Create Grid")
        view_menu.Append(ID_CreateNotebook, "Create Notebook")
        view_menu.Append(ID_CreateSizeReport, "Create Size Reporter")
        view_menu.AppendSeparator()
        view_menu.Append(ID_GridContent, "Use a Grid for the Content Pane")
        view_menu.Append(ID_TextContent, "Use a Text Control for the Content Pane")
        view_menu.Append(ID_HTMLContent, "Use an HTML Control for the Content Pane")
        view_menu.Append(ID_TreeContent, "Use a Tree Control for the Content Pane")
        view_menu.Append(ID_NotebookContent, "Use a AuiNotebook control for the Content Pane")
        view_menu.Append(ID_SizeReportContent, "Use a Size Reporter for the Content Pane")
        view_menu.AppendSeparator()

##        if wx.Platform == "__WXMAC__":
##            switcherAccel = "Alt+Tab"
##        elif wx.Platform == "__WXGTK__":
##            switcherAccel = "Ctrl+/"
##        else:
##            switcherAccel = "Ctrl+Tab"
##
##        view_menu.Append(ID_SwitchPane, _("S&witch Window...") + "\t" + switcherAccel)

        options_menu = wx.Menu()
        options_menu.AppendRadioItem(ID_TransparentHint, "Transparent Hint")
        options_menu.AppendRadioItem(ID_VenetianBlindsHint, "Venetian Blinds Hint")
        options_menu.AppendRadioItem(ID_RectangleHint, "Rectangle Hint")
        options_menu.AppendRadioItem(ID_NoHint, "No Hint")
        options_menu.AppendSeparator()
        options_menu.AppendCheckItem(ID_HintFade, "Hint Fade-in")
        options_menu.AppendCheckItem(ID_AllowFloating, "Allow Floating")
        options_menu.AppendCheckItem(ID_NoVenetianFade, "Disable Venetian Blinds Hint Fade-in")
        options_menu.AppendCheckItem(ID_TransparentDrag, "Transparent Drag")
        options_menu.AppendCheckItem(ID_AllowActivePane, "Allow Active Pane")
        options_menu.AppendCheckItem(ID_LiveUpdate, "Live Resize Update")
        options_menu.AppendCheckItem(ID_NativeMiniframes, "Use Native wx.MiniFrames")
        options_menu.AppendSeparator()
        options_menu.AppendRadioItem(ID_MinimizePosSmart, "Minimize in Smart mode").Check()
        options_menu.AppendRadioItem(ID_MinimizePosTop, "Minimize on Top")
        options_menu.AppendRadioItem(ID_MinimizePosLeft, "Minimize on the Left")
        options_menu.AppendRadioItem(ID_MinimizePosRight, "Minimize on the Right")
        options_menu.AppendRadioItem(ID_MinimizePosBottom, "Minimize at the Bottom")
        options_menu.AppendSeparator()
        options_menu.AppendRadioItem(ID_MinimizeCaptSmart, "Smart Minimized Caption")
        options_menu.AppendRadioItem(ID_MinimizeCaptHorz, "Horizontal Minimized Caption")
        options_menu.AppendRadioItem(ID_MinimizeCaptHide, "Hidden Minimized Caption").Check()
        options_menu.AppendSeparator()
        options_menu.AppendCheckItem(ID_PaneIcons, "Set Icons On Panes")
        options_menu.AppendCheckItem(ID_AnimateFrames, "Animate Dock/Close/Minimize Of Floating Panes")
        options_menu.AppendCheckItem(ID_SmoothDocking, "Smooth Docking Effects (PyQT Style)")
        options_menu.AppendSeparator()
        options_menu.Append(ID_TransparentPane, "Set Floating Panes Transparency")
        options_menu.AppendSeparator()
        options_menu.AppendRadioItem(ID_DefaultDockArt, "Default DockArt")
        options_menu.AppendRadioItem(ID_ModernDockArt, "Modern Dock Art")
        options_menu.AppendSeparator()
        options_menu.Append(ID_SnapToScreen, "Snap To Screen")
        options_menu.AppendCheckItem(ID_SnapPanes, "Snap Panes To Managed Window")
        options_menu.AppendCheckItem(ID_FlyOut, "Use Fly-Out Floating Panes")
        options_menu.AppendSeparator()
        options_menu.AppendCheckItem(ID_CustomPaneButtons, "Set Custom Pane Button Bitmaps")
        options_menu.AppendSeparator()
        options_menu.AppendRadioItem(ID_NoGradient, "No Caption Gradient")
        options_menu.AppendRadioItem(ID_VerticalGradient, "Vertical Caption Gradient")
        options_menu.AppendRadioItem(ID_HorizontalGradient, "Horizontal Caption Gradient")
        options_menu.AppendSeparator()
        options_menu.AppendCheckItem(ID_PreviewMinimized, "Preview Minimized Panes")
        options_menu.AppendSeparator()
        options_menu.Append(ID_Settings, "Settings Pane")

        notebook_menu = wx.Menu()
        notebook_menu.AppendRadioItem(ID_NotebookArtGloss, "Glossy Theme (Default)")
        notebook_menu.AppendRadioItem(ID_NotebookArtSimple, "Simple Theme")
        notebook_menu.AppendRadioItem(ID_NotebookArtVC71, "VC71 Theme")
        notebook_menu.AppendRadioItem(ID_NotebookArtFF2, "Firefox 2 Theme")
        notebook_menu.AppendRadioItem(ID_NotebookArtVC8, "VC8 Theme")
        notebook_menu.AppendRadioItem(ID_NotebookArtChrome, "Chrome Theme")
        notebook_menu.AppendSeparator()
        notebook_menu.AppendRadioItem(ID_NotebookNoCloseButton, "No Close Button")
        notebook_menu.AppendRadioItem(ID_NotebookCloseButton, "Close Button At Right")
        notebook_menu.AppendRadioItem(ID_NotebookCloseButtonAll, "Close Button On All Tabs")
        notebook_menu.AppendRadioItem(ID_NotebookCloseButtonActive, "Close Button On Active Tab")
        notebook_menu.AppendSeparator()
        notebook_menu.AppendCheckItem(ID_NotebookCloseOnLeft, "Close Button On The Left Of Tabs")
        notebook_menu.AppendSeparator()
        notebook_menu.AppendRadioItem(ID_NotebookAlignTop, "Tab Top Alignment")
        notebook_menu.AppendRadioItem(ID_NotebookAlignBottom, "Tab Bottom Alignment")
        notebook_menu.AppendSeparator()
        notebook_menu.AppendCheckItem(ID_NotebookAllowTabMove, "Allow Tab Move")
        notebook_menu.AppendCheckItem(ID_NotebookAllowTabExternalMove, "Allow External Tab Move")
        notebook_menu.AppendCheckItem(ID_NotebookAllowTabSplit, "Allow Notebook Split")
        notebook_menu.AppendCheckItem(ID_NotebookTabFloat, "Allow Single Tab Floating")
        notebook_menu.AppendSeparator()
        notebook_menu.AppendCheckItem(ID_NotebookDclickUnsplit, "Unsplit On Sash Double-Click")
        notebook_menu.AppendCheckItem(ID_NotebookTabDrawDnd, "Draw Tab Image On Drag 'n' Drop")
        notebook_menu.AppendSeparator()
        notebook_menu.AppendCheckItem(ID_NotebookScrollButtons, "Scroll Buttons Visible")
        notebook_menu.AppendCheckItem(ID_NotebookWindowList, "Window List Button Visible")
        notebook_menu.AppendCheckItem(ID_NotebookTabFixedWidth, "Fixed-Width Tabs")
        notebook_menu.AppendSeparator()
        notebook_menu.AppendCheckItem(ID_NotebookHideSingle, "Hide On Single Tab")
        notebook_menu.AppendCheckItem(ID_NotebookSmartTab, "Use Smart Tabbing")
        notebook_menu.AppendCheckItem(ID_NotebookUseImagesDropDown, "Use Tab Images In Dropdown Menu")
        notebook_menu.AppendCheckItem(ID_NotebookCustomButtons, "Show Custom Buttons In Tab Area")
        notebook_menu.AppendSeparator()
        notebook_menu.Append(ID_NotebookMinMaxWidth, "Set Min/Max Tab Widths")
        notebook_menu.Append(ID_NotebookMultiLine, "Add A Multi-Line Label Tab")
        notebook_menu.AppendSeparator()
        notebook_menu.Append(ID_NotebookPreview, "Preview Of All Notebook Pages")

        perspectives_menu = wx.Menu()

        self._perspectives_menu = wx.Menu()
        self._perspectives_menu.Append(ID_CreatePerspective, "Create Perspective")
        self._perspectives_menu.Append(ID_CopyPerspectiveCode, "Copy Perspective Data To Clipboard")
        self._perspectives_menu.AppendSeparator()
        self._perspectives_menu.Append(ID_FirstPerspective+0, "Default Startup")
        self._perspectives_menu.Append(ID_FirstPerspective+1, "All Panes")

        self._nb_perspectives_menu = wx.Menu()
        self._nb_perspectives_menu.Append(ID_CreateNBPerspective, "Create Perspective")
        self._nb_perspectives_menu.Append(ID_CopyNBPerspectiveCode, "Copy Perspective Data To Clipboard")
        self._nb_perspectives_menu.AppendSeparator()
        self._nb_perspectives_menu.Append(ID_FirstNBPerspective+0, "Default Startup")

        guides_menu = wx.Menu()
        guides_menu.AppendRadioItem(ID_StandardGuides, "Standard Docking Guides")
        guides_menu.AppendRadioItem(ID_AeroGuides, "Aero-Style Docking Guides")
        guides_menu.AppendRadioItem(ID_WhidbeyGuides, "Whidbey-Style Docking Guides")

        perspectives_menu.Append(wx.ID_ANY, "Frame Perspectives", self._perspectives_menu)
        perspectives_menu.Append(wx.ID_ANY, "AuiNotebook Perspectives", self._nb_perspectives_menu)
        perspectives_menu.AppendSeparator()
        perspectives_menu.Append(wx.ID_ANY, "Docking Guides", guides_menu)

        action_menu = wx.Menu()
        action_menu.AppendCheckItem(ID_VetoTree, "Veto Floating Of Tree Pane")
        action_menu.AppendCheckItem(ID_VetoText, "Veto Docking Of Fixed Pane")
        action_menu.AppendSeparator()

        attention_menu = wx.Menu()

        self._requestPanes = {}
        for indx, pane in enumerate(self._mgr.GetAllPanes()):
            if pane.IsToolbar():
                continue
            if not pane.caption or not pane.name:
                continue
            ids = wx.ID_HIGHEST + 12345 + indx
            self._requestPanes[ids] = pane.name
            attention_menu.Append(ids, pane.caption)

        action_menu.Append(wx.ID_ANY, "Request User Attention For", attention_menu)

        help_menu = wx.Menu()
        help_menu.Append(wx.ID_ABOUT, "About...")

        mb.Append(file_menu, "&File")
        mb.Append(view_menu, "&View")
        mb.Append(perspectives_menu, "&Perspectives")
        mb.Append(options_menu, "&Options")
        mb.Append(notebook_menu, "&Notebook")
        mb.Append(action_menu, "&Actions")
        mb.Append(help_menu, "&Help")

        self.SetMenuBar(mb)


    def BuildPanes(self):

        # min size for the frame itself isn't completely done.
        # see the end up AuiManager.Update() for the test
        # code. For now, just hard code a frame minimum size
        self.SetMinSize(wx.Size(400, 300))

        # prepare a few custom overflow elements for the toolbars' overflow buttons

        prepend_items, append_items = [], []
        item = aui.AuiToolBarItem()

        item.SetKind(wx.ITEM_SEPARATOR)
        append_items.append(item)

        item = aui.AuiToolBarItem()
        item.SetKind(wx.ITEM_NORMAL)
        item.SetId(ID_CustomizeToolbar)
        item.SetLabel("Customize...")
        append_items.append(item)


        # create some toolbars
        tb1 = aui.AuiToolBar(self, -1, wx.DefaultPosition, wx.DefaultSize,
                             agwStyle=aui.AUI_TB_DEFAULT_STYLE | aui.AUI_TB_OVERFLOW)
        tb1.SetToolBitmapSize(wx.Size(48, 48))
        tb1.AddSimpleTool(ID_SampleItem+1, "Test", wx.ArtProvider.GetBitmap(wx.ART_ERROR))
        tb1.AddSeparator()
        tb1.AddSimpleTool(ID_SampleItem+2, "Test", wx.ArtProvider.GetBitmap(wx.ART_QUESTION))
        tb1.AddSimpleTool(ID_SampleItem+3, "Test", wx.ArtProvider.GetBitmap(wx.ART_INFORMATION))
        tb1.AddSimpleTool(ID_SampleItem+4, "Test", wx.ArtProvider.GetBitmap(wx.ART_WARNING))
        tb1.AddSimpleTool(ID_SampleItem+5, "Test", wx.ArtProvider.GetBitmap(wx.ART_MISSING_IMAGE))
        tb1.SetCustomOverflowItems(prepend_items, append_items)
        tb1.Realize()

        tb2 = aui.AuiToolBar(self, -1, wx.DefaultPosition, wx.DefaultSize,
                             agwStyle=aui.AUI_TB_DEFAULT_STYLE | aui.AUI_TB_OVERFLOW)
        tb2.SetToolBitmapSize(wx.Size(16, 16))

        tb2_bmp1 = wx.ArtProvider.GetBitmap(wx.ART_QUESTION, wx.ART_OTHER, wx.Size(16, 16))
        tb2.AddSimpleTool(ID_SampleItem+6, "Test", tb2_bmp1)
        tb2.AddSimpleTool(ID_SampleItem+7, "Test", tb2_bmp1)
        tb2.AddSimpleTool(ID_SampleItem+8, "Test", tb2_bmp1)
        tb2.AddSimpleTool(ID_SampleItem+9, "Test", tb2_bmp1)
        tb2.AddSeparator()
        tb2.AddSimpleTool(ID_SampleItem+10, "Test", tb2_bmp1)
        tb2.AddSimpleTool(ID_SampleItem+11, "Test", tb2_bmp1)
        tb2.AddSeparator()
        tb2.AddSimpleTool(ID_SampleItem+12, "Test", tb2_bmp1)
        tb2.AddSimpleTool(ID_SampleItem+13, "Test", tb2_bmp1)
        tb2.AddSimpleTool(ID_SampleItem+14, "Test", tb2_bmp1)
        tb2.AddSimpleTool(ID_SampleItem+15, "Test", tb2_bmp1)
        tb2.SetCustomOverflowItems(prepend_items, append_items)
        tb2.Realize()

        tb3 = aui.AuiToolBar(self, -1, wx.DefaultPosition, wx.DefaultSize,
                             agwStyle=aui.AUI_TB_DEFAULT_STYLE | aui.AUI_TB_OVERFLOW)
        tb3.SetToolBitmapSize(wx.Size(16, 16))
        tb3_bmp1 = wx.ArtProvider.GetBitmap(wx.ART_FOLDER, wx.ART_OTHER, wx.Size(16, 16))
        tb3.AddSimpleTool(ID_SampleItem+16, "Check 1", tb3_bmp1, "Check 1", aui.ITEM_CHECK)
        tb3.AddSimpleTool(ID_SampleItem+17, "Check 2", tb3_bmp1, "Check 2", aui.ITEM_CHECK)
        tb3.AddSimpleTool(ID_SampleItem+18, "Check 3", tb3_bmp1, "Check 3", aui.ITEM_CHECK)
        tb3.AddSimpleTool(ID_SampleItem+19, "Check 4", tb3_bmp1, "Check 4", aui.ITEM_CHECK)
        tb3.AddSeparator()
        tb3.AddSimpleTool(ID_SampleItem+20, "Radio 1", tb3_bmp1, "Radio 1", aui.ITEM_RADIO)
        tb3.AddSimpleTool(ID_SampleItem+21, "Radio 2", tb3_bmp1, "Radio 2", aui.ITEM_RADIO)
        tb3.AddSimpleTool(ID_SampleItem+22, "Radio 3", tb3_bmp1, "Radio 3", aui.ITEM_RADIO)
        tb3.AddSeparator()
        tb3.AddSimpleTool(ID_SampleItem+23, "Radio 1 (Group 2)", tb3_bmp1, "Radio 1 (Group 2)", aui.ITEM_RADIO)
        tb3.AddSimpleTool(ID_SampleItem+24, "Radio 2 (Group 2)", tb3_bmp1, "Radio 2 (Group 2)", aui.ITEM_RADIO)
        tb3.AddSimpleTool(ID_SampleItem+25, "Radio 3 (Group 2)", tb3_bmp1, "Radio 3 (Group 2)", aui.ITEM_RADIO)

        tb3.SetCustomOverflowItems(prepend_items, append_items)
        tb3.Realize()

        tb4 = aui.AuiToolBar(self, -1, wx.DefaultPosition, wx.DefaultSize,
                             agwStyle=aui.AUI_TB_OVERFLOW | aui.AUI_TB_TEXT | aui.AUI_TB_HORZ_TEXT)
        tb4.SetToolBitmapSize(wx.Size(16, 16))
        tb4_bmp1 = wx.ArtProvider.GetBitmap(wx.ART_NORMAL_FILE, wx.ART_OTHER, wx.Size(16, 16))
        tb4.AddSimpleTool(ID_DropDownToolbarItem, "Item 1", tb4_bmp1)
        tb4.AddSimpleTool(ID_SampleItem+23, "Item 2", tb4_bmp1)
        tb4.AddSimpleTool(ID_SampleItem+24, "Item 3", tb4_bmp1)
        tb4.AddSimpleTool(ID_SampleItem+25, "Item 4", tb4_bmp1)
        tb4.AddSeparator()
        tb4.AddSimpleTool(ID_SampleItem+26, "Item 5", tb4_bmp1)
        tb4.AddSimpleTool(ID_SampleItem+27, "Item 6", tb4_bmp1)
        tb4.AddSimpleTool(ID_SampleItem+28, "Item 7", tb4_bmp1)
        tb4.AddSimpleTool(ID_SampleItem+29, "Item 8", tb4_bmp1)

        choice = wx.Choice(tb4, -1, choices=["One choice", "Another choice"])
        tb4.AddControl(choice)

        tb4.SetToolDropDown(ID_DropDownToolbarItem, True)
        tb4.Realize()

        tb5 = aui.AuiToolBar(self, -1, wx.DefaultPosition, wx.DefaultSize,
                             agwStyle=aui.AUI_TB_OVERFLOW | aui.AUI_TB_VERTICAL)

        tb5.SetToolBitmapSize(wx.Size(48, 48))
        tb5.AddSimpleTool(ID_SampleItem+30, "Test", wx.ArtProvider.GetBitmap(wx.ART_ERROR))
        tb5.AddSeparator()
        tb5.AddSimpleTool(ID_SampleItem+31, "Test", wx.ArtProvider.GetBitmap(wx.ART_QUESTION))
        tb5.AddSimpleTool(ID_SampleItem+32, "Test", wx.ArtProvider.GetBitmap(wx.ART_INFORMATION))
        tb5.AddSimpleTool(ID_SampleItem+33, "Test", wx.ArtProvider.GetBitmap(wx.ART_WARNING))
        tb5.AddSimpleTool(ID_SampleItem+34, "Test", wx.ArtProvider.GetBitmap(wx.ART_MISSING_IMAGE))
        tb5.SetCustomOverflowItems(prepend_items, append_items)
        tb5.Realize()

        tb6 = aui.AuiToolBar(self, -1, wx.DefaultPosition, wx.DefaultSize,
                             agwStyle=aui.AUI_TB_OVERFLOW | aui.AUI_TB_VERT_TEXT)
        tb6.SetToolBitmapSize(wx.Size(48, 48))
        tb6.AddSimpleTool(ID_SampleItem+35, "Clockwise 1", wx.ArtProvider.GetBitmap(wx.ART_ERROR, wx.ART_OTHER, wx.Size(16, 16)))
        tb6.AddSeparator()
        tb6.AddSimpleTool(ID_SampleItem+36, "Clockwise 2", wx.ArtProvider.GetBitmap(wx.ART_QUESTION, wx.ART_OTHER, wx.Size(16, 16)))
        tb6.AddSimpleTool(ID_DropDownToolbarItem, "Clockwise 3", wx.ArtProvider.GetBitmap(wx.ART_WARNING, wx.ART_OTHER, wx.Size(16, 16)))
        tb6.SetCustomOverflowItems(prepend_items, append_items)
        tb6.SetToolDropDown(ID_DropDownToolbarItem, True)
        tb6.Realize()

        # add a bunch of panes
        self._mgr.AddPane(self.CreateSizeReportCtrl(), aui.AuiPaneInfo().
                          Name("test1").Caption("Pane Caption").Top().MinimizeButton(True))

        self._mgr.AddPane(self.CreateSizeReportCtrl(), aui.AuiPaneInfo().
                          Name("test2").Caption("Client Size Reporter").
                          Bottom().Position(1).CloseButton(True).MaximizeButton(True).
                          MinimizeButton(True).CaptionVisible(True, left=True))

        self._mgr.AddPane(self.CreateSizeReportCtrl(), aui.AuiPaneInfo().
                          Name("test3").Caption("Client Size Reporter").
                          Bottom().CloseButton(True).MaximizeButton(True).MinimizeButton(True).
                          CaptionVisible(True, left=True))

        self._mgr.AddPane(self.CreateSizeReportCtrl(), aui.AuiPaneInfo().
                          Name("test4").Caption("Pane Caption").Left())

        self._mgr.AddPane(self.CreateSizeReportCtrl(), aui.AuiPaneInfo().
                          Name("test5").Caption("No Close Button").Right().CloseButton(False))

        self._mgr.AddPane(self.CreateSizeReportCtrl(), aui.AuiPaneInfo().
                          Name("test6").Caption("Client Size Reporter").Right().Row(1).
                          CloseButton(True).MaximizeButton(True).MinimizeButton(True))

        self._mgr.AddPane(self.CreateSizeReportCtrl(), aui.AuiPaneInfo().
                          Name("test7").Caption("Client Size Reporter").Left().Layer(1).
                          CloseButton(True).MaximizeButton(True).MinimizeButton(True))

        self._mgr.AddPane(self.CreateTreeCtrl(), aui.AuiPaneInfo().Name("test8").Caption("Tree Pane").
                          Left().Layer(1).Position(1).CloseButton(True).MaximizeButton(True).
                          MinimizeButton(True))

        self._mgr.AddPane(self.CreateSizeReportCtrl(), aui.AuiPaneInfo().
                          Name("test9").Caption("Min Size 200x100").
                          BestSize(wx.Size(200,100)).MinSize(wx.Size(200,100)).Bottom().Layer(1).
                          CloseButton(True).MaximizeButton(True).MinimizeButton(True))

        self._mgr.AddPane(self.CreateTreeCtrl(), aui.AuiPaneInfo().
                          Name("autonotebook").Caption("Auto NB").
                          Bottom().Layer(1).Position(1).MinimizeButton(True))

        wnd10 = self.CreateTextCtrl("This pane will prompt the user before hiding.")
        self._mgr.AddPane(wnd10, aui.AuiPaneInfo().
                          Name("test10").Caption("Text Pane with Hide Prompt").
                          Bottom().MinimizeButton(True), target=self._mgr.GetPane("autonotebook"))

        self._mgr.AddPane(self.CreateTreeCtrl(), aui.AuiPaneInfo().
                          Name("thirdauto").Caption("A Third Auto-NB Pane").
                          Bottom().MinimizeButton(True), target=self._mgr.GetPane("autonotebook"))

        self._mgr.AddPane(self.CreateSizeReportCtrl(), aui.AuiPaneInfo().
                          Name("test11").Caption("Fixed Pane").
                          Bottom().Layer(1).Position(2).Fixed().MinimizeButton(True))

        self._mgr.AddPane(SettingsPanel(self,self), aui.AuiPaneInfo().
                          Name("settings").Caption("Dock Manager Settings").
                          Dockable(False).Float().Hide().MinimizeButton(True))

        # create some center panes

        self._mgr.AddPane(self.CreateGrid(), aui.AuiPaneInfo().Name("grid_content").
                          CenterPane().Hide().MinimizeButton(True))

        self._mgr.AddPane(self.CreateTreeCtrl(), aui.AuiPaneInfo().Name("tree_content").
                          CenterPane().Hide().MinimizeButton(True))

        self._mgr.AddPane(self.CreateSizeReportCtrl(), aui.AuiPaneInfo().Name("sizereport_content").
                          CenterPane().Hide().MinimizeButton(True))

        self._mgr.AddPane(self.CreateTextCtrl(), aui.AuiPaneInfo().Name("text_content").
                          CenterPane().Hide().MinimizeButton(True))

        self._mgr.AddPane(self.CreateHTMLCtrl(), aui.AuiPaneInfo().Name("html_content").
                          CenterPane().Hide().MinimizeButton(True))

        self._mgr.AddPane(self.CreateNotebook(), aui.AuiPaneInfo().Name("notebook_content").
                          CenterPane().PaneBorder(False))

        # add the toolbars to the manager
        self._mgr.AddPane(tb1, aui.AuiPaneInfo().Name("tb1").Caption("Big Toolbar").
                          ToolbarPane().Top())

        self._mgr.AddPane(tb2, aui.AuiPaneInfo().Name("tb2").Caption("Toolbar 2").
                          ToolbarPane().Top().Row(1))

        self._mgr.AddPane(tb3, aui.AuiPaneInfo().Name("tb3").Caption("Toolbar 3").
                          ToolbarPane().Top().Row(1).Position(1))

        self._mgr.AddPane(tb4, aui.AuiPaneInfo().Name("tb4").Caption("Sample Bookmark Toolbar").
                          ToolbarPane().Top().Row(2))

        self._mgr.AddPane(tb5, aui.AuiPaneInfo().Name("tb5").Caption("Sample Vertical Toolbar").
                          ToolbarPane().Left().GripperTop())

        self._mgr.AddPane(tb6, aui.AuiPaneInfo().
                          Name("tb6").Caption("Sample Vertical Clockwise Rotated Toolbar").
                          ToolbarPane().Right().GripperTop().TopDockable(False).BottomDockable(False));

        self._mgr.AddPane(wx.Button(self, -1, "Test Button"),
                          aui.AuiPaneInfo().Name("tb7").ToolbarPane().Top().Row(2).Position(1))

        # Show how to add a control inside a tab
        notebook = self._mgr.GetPane("notebook_content").window
        self.gauge = ProgressGauge(notebook, size=(55, 15))
        notebook.AddControlToPage(4, self.gauge)

        self._main_notebook = notebook

        # make some default perspectives
        perspective_all = self._mgr.SavePerspective()

        all_panes = self._mgr.GetAllPanes()
        for pane in all_panes:
            if not pane.IsToolbar():
                pane.Hide()

        self._mgr.GetPane("tb1").Hide()
        self._mgr.GetPane("tb7").Hide()

        self._mgr.GetPane("test8").Show().Left().Layer(0).Row(0).Position(0)
        self._mgr.GetPane("__notebook_%d"%self._mgr.GetPane("test10").notebook_id).Show().Bottom().Layer(0).Row(0).Position(0)
        self._mgr.GetPane("autonotebook").Show()
        self._mgr.GetPane("thirdauto").Show()
        self._mgr.GetPane("test10").Show()
        self._mgr.GetPane("notebook_content").Show()

        perspective_default = self._mgr.SavePerspective()

        self._perspectives = []
        self._perspectives.append(perspective_default)
        self._perspectives.append(perspective_all)

        self._nb_perspectives = []
        auibook = self._mgr.GetPane("notebook_content").window
        nb_perspective_default = auibook.SavePerspective()
        self._nb_perspectives.append(nb_perspective_default)

        self._mgr.LoadPerspective(perspective_default)

        # Show how to get a custom minimizing behaviour, i.e., to minimize a pane
        # inside an existing AuiToolBar
        tree = self._mgr.GetPane("test8")
        tree.MinimizeMode(aui.AUI_MINIMIZE_POS_TOOLBAR)
        toolbarPane = self._mgr.GetPane(tb4)
        tree.MinimizeTarget(toolbarPane)

        # "commit" all changes made to AuiManager
        self._mgr.Update()


    def BindEvents(self):

        self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground)
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_MENU, self.OnCreateTree, id=ID_CreateTree)
        self.Bind(wx.EVT_MENU, self.OnCreateGrid, id=ID_CreateGrid)
        self.Bind(wx.EVT_MENU, self.OnCreateText, id=ID_CreateText)
        self.Bind(wx.EVT_MENU, self.OnCreateHTML, id=ID_CreateHTML)
        self.Bind(wx.EVT_MENU, self.OnCreateSizeReport, id=ID_CreateSizeReport)
        self.Bind(wx.EVT_MENU, self.OnCreateNotebook, id=ID_CreateNotebook)
##        self.Bind(wx.EVT_MENU, self.OnSwitchPane, id=ID_SwitchPane)
        self.Bind(wx.EVT_MENU, self.OnCreatePerspective, id=ID_CreatePerspective)
        self.Bind(wx.EVT_MENU, self.OnCopyPerspectiveCode, id=ID_CopyPerspectiveCode)
        self.Bind(wx.EVT_MENU, self.OnCreateNBPerspective, id=ID_CreateNBPerspective)
        self.Bind(wx.EVT_MENU, self.OnCopyNBPerspectiveCode, id=ID_CopyNBPerspectiveCode)
        self.Bind(wx.EVT_MENU, self.OnGuides, id=ID_StandardGuides)
        self.Bind(wx.EVT_MENU, self.OnGuides, id=ID_AeroGuides)
        self.Bind(wx.EVT_MENU, self.OnGuides, id=ID_WhidbeyGuides)
        self.Bind(wx.EVT_MENU, self.OnManagerFlag, id=ID_AllowFloating)
        self.Bind(wx.EVT_MENU, self.OnManagerFlag, id=ID_TransparentHint)
        self.Bind(wx.EVT_MENU, self.OnManagerFlag, id=ID_VenetianBlindsHint)
        self.Bind(wx.EVT_MENU, self.OnManagerFlag, id=ID_RectangleHint)
        self.Bind(wx.EVT_MENU, self.OnManagerFlag, id=ID_NoHint)
        self.Bind(wx.EVT_MENU, self.OnManagerFlag, id=ID_HintFade)
        self.Bind(wx.EVT_MENU, self.OnManagerFlag, id=ID_NoVenetianFade)
        self.Bind(wx.EVT_MENU, self.OnManagerFlag, id=ID_TransparentDrag)
        self.Bind(wx.EVT_MENU, self.OnManagerFlag, id=ID_LiveUpdate)
        self.Bind(wx.EVT_MENU, self.OnManagerFlag, id=ID_SmoothDocking)
        self.Bind(wx.EVT_MENU, self.OnManagerFlag, id=ID_NativeMiniframes)
        self.Bind(wx.EVT_MENU, self.OnMinimizePosition, id=ID_MinimizePosSmart)
        self.Bind(wx.EVT_MENU, self.OnMinimizePosition, id=ID_MinimizePosTop)
        self.Bind(wx.EVT_MENU, self.OnMinimizePosition, id=ID_MinimizePosLeft)
        self.Bind(wx.EVT_MENU, self.OnMinimizePosition, id=ID_MinimizePosRight)
        self.Bind(wx.EVT_MENU, self.OnMinimizePosition, id=ID_MinimizePosBottom)
        self.Bind(wx.EVT_MENU, self.OnMinimizeCaption, id=ID_MinimizeCaptSmart)
        self.Bind(wx.EVT_MENU, self.OnMinimizeCaption, id=ID_MinimizeCaptHorz)
        self.Bind(wx.EVT_MENU, self.OnMinimizeCaption, id=ID_MinimizeCaptHide)
        self.Bind(wx.EVT_MENU, self.OnManagerFlag, id=ID_AnimateFrames)
        self.Bind(wx.EVT_MENU, self.OnSetIconsOnPanes, id=ID_PaneIcons)
        self.Bind(wx.EVT_MENU, self.OnTransparentPane, id=ID_TransparentPane)
        self.Bind(wx.EVT_MENU, self.OnDockArt, id=ID_DefaultDockArt)
        self.Bind(wx.EVT_MENU, self.OnDockArt, id=ID_ModernDockArt)
        self.Bind(wx.EVT_MENU, self.OnSnapToScreen, id=ID_SnapToScreen)
        self.Bind(wx.EVT_MENU, self.OnSnapPanes, id=ID_SnapPanes)
        self.Bind(wx.EVT_MENU, self.OnFlyOut, id=ID_FlyOut)
        self.Bind(wx.EVT_MENU, self.OnCustomPaneButtons, id=ID_CustomPaneButtons)
        self.Bind(wx.EVT_MENU, self.OnManagerFlag, id=ID_AllowActivePane)
        self.Bind(wx.EVT_MENU, self.OnNotebookFlag, id=ID_NotebookTabFixedWidth)
        self.Bind(wx.EVT_MENU, self.OnNotebookFlag, id=ID_NotebookNoCloseButton)
        self.Bind(wx.EVT_MENU, self.OnNotebookFlag, id=ID_NotebookCloseButton)
        self.Bind(wx.EVT_MENU, self.OnNotebookFlag, id=ID_NotebookCloseButtonAll)
        self.Bind(wx.EVT_MENU, self.OnNotebookFlag, id=ID_NotebookCloseButtonActive)
        self.Bind(wx.EVT_MENU, self.OnNotebookFlag, id=ID_NotebookAllowTabMove)
        self.Bind(wx.EVT_MENU, self.OnNotebookFlag, id=ID_NotebookAllowTabExternalMove)
        self.Bind(wx.EVT_MENU, self.OnNotebookFlag, id=ID_NotebookAllowTabSplit)
        self.Bind(wx.EVT_MENU, self.OnNotebookFlag, id=ID_NotebookTabFloat)
        self.Bind(wx.EVT_MENU, self.OnNotebookFlag, id=ID_NotebookDclickUnsplit)
        self.Bind(wx.EVT_MENU, self.OnNotebookFlag, id=ID_NotebookTabDrawDnd)
        self.Bind(wx.EVT_MENU, self.OnNotebookFlag, id=ID_NotebookScrollButtons)
        self.Bind(wx.EVT_MENU, self.OnNotebookFlag, id=ID_NotebookWindowList)
        self.Bind(wx.EVT_MENU, self.OnNotebookFlag, id=ID_NotebookArtGloss)
        self.Bind(wx.EVT_MENU, self.OnNotebookFlag, id=ID_NotebookArtSimple)
        self.Bind(wx.EVT_MENU, self.OnNotebookFlag, id=ID_NotebookArtVC71)
        self.Bind(wx.EVT_MENU, self.OnNotebookFlag, id=ID_NotebookArtFF2)
        self.Bind(wx.EVT_MENU, self.OnNotebookFlag, id=ID_NotebookArtVC8)
        self.Bind(wx.EVT_MENU, self.OnNotebookFlag, id=ID_NotebookArtChrome)
        self.Bind(wx.EVT_MENU, self.OnNotebookFlag, id=ID_NotebookHideSingle)
        self.Bind(wx.EVT_MENU, self.OnNotebookFlag, id=ID_NotebookSmartTab)
        self.Bind(wx.EVT_MENU, self.OnNotebookFlag, id=ID_NotebookUseImagesDropDown)
        self.Bind(wx.EVT_MENU, self.OnNotebookFlag, id=ID_NotebookCloseOnLeft)
        self.Bind(wx.EVT_MENU, self.OnTabAlignment, id=ID_NotebookAlignTop)
        self.Bind(wx.EVT_MENU, self.OnTabAlignment, id=ID_NotebookAlignBottom)
        self.Bind(wx.EVT_MENU, self.OnCustomTabButtons, id=ID_NotebookCustomButtons)
        self.Bind(wx.EVT_MENU, self.OnMinMaxTabWidth, id=ID_NotebookMinMaxWidth)
        self.Bind(wx.EVT_MENU, self.OnPreview, id=ID_NotebookPreview)
        self.Bind(wx.EVT_MENU, self.OnAddMultiLine, id=ID_NotebookMultiLine)

        self.Bind(wx.EVT_MENU, self.OnGradient, id=ID_NoGradient)
        self.Bind(wx.EVT_MENU, self.OnGradient, id=ID_VerticalGradient)
        self.Bind(wx.EVT_MENU, self.OnGradient, id=ID_HorizontalGradient)
        self.Bind(wx.EVT_MENU, self.OnSettings, id=ID_Settings)
        self.Bind(wx.EVT_MENU, self.OnPreviewMinimized, id=ID_PreviewMinimized)
        self.Bind(wx.EVT_MENU, self.OnCustomizeToolbar, id=ID_CustomizeToolbar)
        self.Bind(wx.EVT_MENU, self.OnChangeContentPane, id=ID_GridContent)
        self.Bind(wx.EVT_MENU, self.OnChangeContentPane, id=ID_TreeContent)
        self.Bind(wx.EVT_MENU, self.OnChangeContentPane, id=ID_TextContent)
        self.Bind(wx.EVT_MENU, self.OnChangeContentPane, id=ID_SizeReportContent)
        self.Bind(wx.EVT_MENU, self.OnChangeContentPane, id=ID_HTMLContent)
        self.Bind(wx.EVT_MENU, self.OnChangeContentPane, id=ID_NotebookContent)
        self.Bind(wx.EVT_MENU, self.OnVetoTree, id=ID_VetoTree)
        self.Bind(wx.EVT_MENU, self.OnVetoText, id=ID_VetoText)

        for ids in self._requestPanes:
            self.Bind(wx.EVT_MENU, self.OnRequestUserAttention, id=ids)

        self.Bind(wx.EVT_MENU, self.OnExit, id=wx.ID_EXIT)
        self.Bind(wx.EVT_MENU, self.OnAbout, id=wx.ID_ABOUT)

        self.Bind(wx.EVT_MENU_RANGE, self.OnRestorePerspective, id=ID_FirstPerspective,
                  id2=ID_FirstPerspective+1000)
        self.Bind(wx.EVT_MENU_RANGE, self.OnRestoreNBPerspective, id=ID_FirstNBPerspective,
                  id2=ID_FirstNBPerspective+1000)

        self.Bind(wx.EVT_UPDATE_UI, self.OnUpdateUI, id=ID_AllowFloating)
        self.Bind(wx.EVT_UPDATE_UI, self.OnUpdateUI, id=ID_TransparentHint)
        self.Bind(wx.EVT_UPDATE_UI, self.OnUpdateUI, id=ID_HintFade)
        self.Bind(wx.EVT_UPDATE_UI, self.OnUpdateUI, id=ID_TransparentDrag)
        self.Bind(wx.EVT_UPDATE_UI, self.OnUpdateUI, id=ID_NoGradient)
        self.Bind(wx.EVT_UPDATE_UI, self.OnUpdateUI, id=ID_VerticalGradient)
        self.Bind(wx.EVT_UPDATE_UI, self.OnUpdateUI, id=ID_HorizontalGradient)
        self.Bind(wx.EVT_UPDATE_UI, self.OnUpdateUI, id=ID_VenetianBlindsHint)
        self.Bind(wx.EVT_UPDATE_UI, self.OnUpdateUI, id=ID_RectangleHint)
        self.Bind(wx.EVT_UPDATE_UI, self.OnUpdateUI, id=ID_NoHint)
        self.Bind(wx.EVT_UPDATE_UI, self.OnUpdateUI, id=ID_NoVenetianFade)
        self.Bind(wx.EVT_UPDATE_UI, self.OnUpdateUI, id=ID_LiveUpdate)
        self.Bind(wx.EVT_UPDATE_UI, self.OnUpdateUI, id=ID_PaneIcons)
        self.Bind(wx.EVT_UPDATE_UI, self.OnUpdateUI, id=ID_AnimateFrames)
        self.Bind(wx.EVT_UPDATE_UI, self.OnUpdateUI, id=ID_DefaultDockArt)
        self.Bind(wx.EVT_UPDATE_UI, self.OnUpdateUI, id=ID_ModernDockArt)
        self.Bind(wx.EVT_UPDATE_UI, self.OnUpdateUI, id=ID_SnapPanes)
        self.Bind(wx.EVT_UPDATE_UI, self.OnUpdateUI, id=ID_FlyOut)
        self.Bind(wx.EVT_UPDATE_UI, self.OnUpdateUI, id=ID_CustomPaneButtons)

        self.Bind(wx.EVT_UPDATE_UI, self.OnUpdateUI, id=ID_NotebookTabFixedWidth)
        self.Bind(wx.EVT_UPDATE_UI, self.OnUpdateUI, id=ID_NotebookNoCloseButton)
        self.Bind(wx.EVT_UPDATE_UI, self.OnUpdateUI, id=ID_NotebookCloseButton)
        self.Bind(wx.EVT_UPDATE_UI, self.OnUpdateUI, id=ID_NotebookCloseButtonAll)
        self.Bind(wx.EVT_UPDATE_UI, self.OnUpdateUI, id=ID_NotebookCloseButtonActive)
        self.Bind(wx.EVT_UPDATE_UI, self.OnUpdateUI, id=ID_NotebookAllowTabMove)
        self.Bind(wx.EVT_UPDATE_UI, self.OnUpdateUI, id=ID_NotebookAllowTabExternalMove)
        self.Bind(wx.EVT_UPDATE_UI, self.OnUpdateUI, id=ID_NotebookAllowTabSplit)
        self.Bind(wx.EVT_UPDATE_UI, self.OnUpdateUI, id=ID_NotebookTabFloat)
        self.Bind(wx.EVT_UPDATE_UI, self.OnUpdateUI, id=ID_NotebookDclickUnsplit)
        self.Bind(wx.EVT_UPDATE_UI, self.OnUpdateUI, id=ID_NotebookTabDrawDnd)
        self.Bind(wx.EVT_UPDATE_UI, self.OnUpdateUI, id=ID_NotebookScrollButtons)
        self.Bind(wx.EVT_UPDATE_UI, self.OnUpdateUI, id=ID_NotebookWindowList)
        self.Bind(wx.EVT_UPDATE_UI, self.OnUpdateUI, id=ID_NotebookHideSingle)
        self.Bind(wx.EVT_UPDATE_UI, self.OnUpdateUI, id=ID_NotebookSmartTab)
        self.Bind(wx.EVT_UPDATE_UI, self.OnUpdateUI, id=ID_NotebookUseImagesDropDown)
        self.Bind(wx.EVT_UPDATE_UI, self.OnUpdateUI, id=ID_NotebookCustomButtons)
        self.Bind(wx.EVT_UPDATE_UI, self.OnUpdateUI, id=ID_VetoTree)
        self.Bind(wx.EVT_UPDATE_UI, self.OnUpdateUI, id=ID_VetoText)
        self.Bind(wx.EVT_UPDATE_UI, self.OnUpdateUI, id=ID_StandardGuides)
        self.Bind(wx.EVT_UPDATE_UI, self.OnUpdateUI, id=ID_AeroGuides)
        self.Bind(wx.EVT_UPDATE_UI, self.OnUpdateUI, id=ID_WhidbeyGuides)

        for ids in self._requestPanes:
            self.Bind(wx.EVT_UPDATE_UI, self.OnUpdateUI, id=ids)

        self.Bind(aui.EVT_AUITOOLBAR_TOOL_DROPDOWN, self.OnDropDownToolbarItem, id=ID_DropDownToolbarItem)
        self.Bind(aui.EVT_AUI_PANE_CLOSE, self.OnPaneClose)
        self.Bind(aui.EVT_AUINOTEBOOK_ALLOW_DND, self.OnAllowNotebookDnD)
        self.Bind(aui.EVT_AUINOTEBOOK_PAGE_CLOSE, self.OnNotebookPageClose)

        self.Bind(aui.EVT_AUI_PANE_FLOATING, self.OnFloatDock)
        self.Bind(aui.EVT_AUI_PANE_FLOATED, self.OnFloatDock)
        self.Bind(aui.EVT_AUI_PANE_DOCKING, self.OnFloatDock)
        self.Bind(aui.EVT_AUI_PANE_DOCKED, self.OnFloatDock)

        self.Bind(wx.EVT_CLOSE, self.OnClose)

        self.Bind(wx.EVT_TIMER, self.TimerHandler)
        self.timer = wx.Timer(self)
        self.timer.Start(100)


    def __del__(self):

        self.timer.Stop()


    def OnClose(self, event):

        self.timer.Stop()
        self._mgr.UnInit()
        event.Skip()


    def TimerHandler(self, event):

        try:
            self.gauge.Pulse()
        except:
            self.timer.Stop()


    def GetDockArt(self):

        return self._mgr.GetArtProvider()


    def DoUpdate(self):

        self._mgr.Update()
        self.Refresh()


    def OnEraseBackground(self, event):

        event.Skip()


    def OnSize(self, event):

        event.Skip()


    def OnSettings(self, event):

        # show the settings pane, and float it
        floating_pane = self._mgr.GetPane("settings").Float().Show()

        if floating_pane.floating_pos == wx.DefaultPosition:
            floating_pane.FloatingPosition(self.GetStartPosition())

        self._mgr.Update()


    def OnPreviewMinimized(self, event):

        checked = event.IsChecked()
        agwFlags = self._mgr.GetAGWFlags()

        if event.IsChecked():
            agwFlags ^= aui.AUI_MGR_PREVIEW_MINIMIZED_PANES
        else:
            agwFlags &= ~aui.AUI_MGR_PREVIEW_MINIMIZED_PANES

        self._mgr.SetAGWFlags(agwFlags)


    def OnSetIconsOnPanes(self, event):

        panes = self._mgr.GetAllPanes()
        checked = event.IsChecked()
        self._pane_icons = checked

        for pane in panes:
            if checked:
                randimage = random.randint(0, len(ArtIDs) - 1)
                bmp = wx.ArtProvider.GetBitmap(eval(ArtIDs[randimage]), wx.ART_OTHER, (16, 16))
            else:
                bmp = None

            pane.Icon(bmp)

        self._mgr.Update()


    def OnTransparentPane(self, event):

        dlg = wx.TextEntryDialog(self, "Enter a transparency value (0-255):", "Pane transparency")

        dlg.SetValue("%d"%self._transparency)
        if dlg.ShowModal() != wx.ID_OK:
            return

        transparency = int(dlg.GetValue())
        dlg.Destroy()
        try:
            transparency = int(transparency)
        except:
            dlg = wx.MessageDialog(self, 'Invalid transparency value. Transparency' \
                                   ' should be an integer between 0 and 255.',
                                   'Error',
                                   wx.OK | wx.ICON_ERROR)
            dlg.ShowModal()
            dlg.Destroy()
            return

        if transparency < 0 or transparency > 255:
            dlg = wx.MessageDialog(self, 'Invalid transparency value. Transparency' \
                                   ' should be an integer between 0 and 255.',
                                   'Error',
                                   wx.OK | wx.ICON_ERROR)
            dlg.ShowModal()
            dlg.Destroy()
            return

        self._transparency = transparency
        panes = self._mgr.GetAllPanes()
        for pane in panes:
            pane.Transparent(self._transparency)

        self._mgr.Update()


    def OnDockArt(self, event):

        if event.GetId() == ID_DefaultDockArt:
            self._mgr.SetArtProvider(aui.AuiDefaultDockArt())
        else:
            if self._mgr.CanUseModernDockArt():
                self._mgr.SetArtProvider(aui.ModernDockArt(self))

        self._mgr.Update()
        self.Refresh()


    def OnSnapToScreen(self, event):

        self._mgr.SnapToScreen(True, monitor=0, hAlign=wx.RIGHT, vAlign=wx.TOP)


    def OnSnapPanes(self, event):

        allPanes = self._mgr.GetAllPanes()

        if not self._snapped:
            self._captions = {}
            for pane in allPanes:
                self._captions[pane.name] = pane.caption

        toSnap = not self._snapped

        if toSnap:
            for pane in allPanes:
                if pane.IsToolbar() or isinstance(pane.window, aui.AuiNotebook):
                    continue

                snap = random.randint(0, 4)
                if snap == 0:
                    # Snap everywhere
                    pane.Caption(pane.caption + " (Snap Everywhere)")
                    pane.Snappable(True)
                elif snap == 1:
                    # Snap left
                    pane.Caption(pane.caption + " (Snap Left)")
                    pane.LeftSnappable(True)
                elif snap == 2:
                    # Snap right
                    pane.Caption(pane.caption + " (Snap Right)")
                    pane.RightSnappable(True)
                elif snap == 3:
                    # Snap top
                    pane.Caption(pane.caption + " (Snap Top)")
                    pane.TopSnappable(True)
                elif snap == 4:
                    # Snap bottom
                    pane.Caption(pane.caption + " (Snap Bottom)")
                    pane.BottomSnappable(True)

        else:

            for pane in allPanes:
                if pane.IsToolbar() or isinstance(pane.window, aui.AuiNotebook):
                    continue

                pane.Caption(self._captions[pane.name])
                pane.Snappable(False)

        self._snapped = toSnap
        self._mgr.Update()
        self.Refresh()


    def OnFlyOut(self, event):

        checked = event.IsChecked()
        pane = self._mgr.GetPane("test8")

        if checked:
            dlg = wx.MessageDialog(self, 'The tree pane will have fly-out' \
                                   ' behaviour when floating.',
                                   'Message',
                                   wx.OK | wx.ICON_INFORMATION)
            dlg.ShowModal()
            dlg.Destroy()
            pane.FlyOut(True)
        else:
            pane.FlyOut(False)

        self._mgr.Update()


    def OnCustomPaneButtons(self, event):

        self._custom_pane_buttons = checked = event.IsChecked()
        art = self._mgr.GetArtProvider()

        if not checked:
            art.SetDefaultPaneBitmaps(wx.Platform == "__WXMAC__")
        else:
            for bmp, button, active, maximize in CUSTOM_PANE_BITMAPS:
                art.SetCustomPaneBitmap(bmp.GetBitmap(), button, active, maximize)

        self._mgr.Update()
        self.Refresh()


    def OnCustomizeToolbar(self, event):

        wx.MessageBox("Customize Toolbar clicked", "AUI Test")


    def OnGradient(self, event):

        evId = event.GetId()
        if evId == ID_NoGradient:
            gradient = aui.AUI_GRADIENT_NONE
        elif evId == ID_VerticalGradient:
            gradient = aui.AUI_GRADIENT_VERTICAL
        elif evId == ID_HorizontalGradient:
            gradient = aui.AUI_GRADIENT_HORIZONTAL

        self._mgr.GetArtProvider().SetMetric(aui.AUI_DOCKART_GRADIENT_TYPE, gradient)
        self._mgr.Update()


    def OnManagerFlag(self, event):

        flag = 0
        evId = event.GetId()

        if evId in [ID_TransparentHint, ID_VenetianBlindsHint, ID_RectangleHint, ID_NoHint]:

            agwFlags = self._mgr.GetAGWFlags()
            agwFlags &= ~aui.AUI_MGR_TRANSPARENT_HINT
            agwFlags &= ~aui.AUI_MGR_VENETIAN_BLINDS_HINT
            agwFlags &= ~aui.AUI_MGR_RECTANGLE_HINT
            self._mgr.SetAGWFlags(agwFlags)

        if evId == ID_AllowFloating:
            flag = aui.AUI_MGR_ALLOW_FLOATING
        elif evId == ID_TransparentDrag:
            flag = aui.AUI_MGR_TRANSPARENT_DRAG
        elif evId == ID_HintFade:
            flag = aui.AUI_MGR_HINT_FADE
        elif evId == ID_NoVenetianFade:
            flag = aui.AUI_MGR_NO_VENETIAN_BLINDS_FADE
        elif evId == ID_AllowActivePane:
            flag = aui.AUI_MGR_ALLOW_ACTIVE_PANE
        elif evId == ID_TransparentHint:
            flag = aui.AUI_MGR_TRANSPARENT_HINT
        elif evId == ID_VenetianBlindsHint:
            flag = aui.AUI_MGR_VENETIAN_BLINDS_HINT
        elif evId == ID_RectangleHint:
            flag = aui.AUI_MGR_RECTANGLE_HINT
        elif evId == ID_LiveUpdate:
            flag = aui.AUI_MGR_LIVE_RESIZE
        elif evId == ID_AnimateFrames:
            flag = aui.AUI_MGR_ANIMATE_FRAMES
        elif evId == ID_SmoothDocking:
            flag = aui.AUI_MGR_SMOOTH_DOCKING
        elif evId == ID_NativeMiniframes:
            flag = aui.AUI_MGR_USE_NATIVE_MINIFRAMES

        if flag:
            self._mgr.SetAGWFlags(self._mgr.GetAGWFlags() ^ flag)

        self._mgr.Update()


    def OnMinimizePosition(self, event):

        minize_mode = 0
        evId = event.GetId()

        if evId == ID_MinimizePosSmart:
            minize_mode |= aui.AUI_MINIMIZE_POS_SMART
        elif evId == ID_MinimizePosTop:
            minize_mode |= aui.AUI_MINIMIZE_POS_TOP
        elif evId == ID_MinimizePosLeft:
            minize_mode |= aui.AUI_MINIMIZE_POS_LEFT
        elif evId == ID_MinimizePosRight:
            minize_mode |= aui.AUI_MINIMIZE_POS_RIGHT
        elif evId == ID_MinimizePosBottom:
            minize_mode |= aui.AUI_MINIMIZE_POS_BOTTOM

        all_panes = self._mgr.GetAllPanes()
        for pane in all_panes:
            if pane.name != "test8":
                pane.MinimizeMode(minize_mode | (pane.GetMinimizeMode() & aui.AUI_MINIMIZE_CAPT_MASK))


    def OnMinimizeCaption(self, event):

        minize_mode = 0
        evId = event.GetId()

        if evId == ID_MinimizeCaptSmart:
            minize_mode |= aui.AUI_MINIMIZE_CAPT_SMART
        elif evId == ID_MinimizeCaptHorz:
            minize_mode |= aui.AUI_MINIMIZE_CAPT_HORZ
        elif evId == ID_MinimizeCaptHide:
            minize_mode |= aui.AUI_MINIMIZE_CAPT_HIDE

        all_panes = self._mgr.GetAllPanes()
        for pane in all_panes:
            pane.MinimizeMode(minize_mode | (pane.GetMinimizeMode() & aui.AUI_MINIMIZE_POS_MASK))


    def OnNotebookFlag(self, event):

        evId = event.GetId()
        unsplit = None

        if evId in [ID_NotebookNoCloseButton, ID_NotebookCloseButton, ID_NotebookCloseButtonAll, \
                    ID_NotebookCloseButtonActive]:

            self._notebook_style &= ~(aui.AUI_NB_CLOSE_BUTTON |
                                      aui.AUI_NB_CLOSE_ON_ACTIVE_TAB |
                                      aui.AUI_NB_CLOSE_ON_ALL_TABS)

            if evId == ID_NotebookCloseButton:
                self._notebook_style ^= aui.AUI_NB_CLOSE_BUTTON
            elif evId == ID_NotebookCloseButtonAll:
                self._notebook_style ^= aui.AUI_NB_CLOSE_ON_ALL_TABS
            elif evId == ID_NotebookCloseButtonActive:
                self._notebook_style ^= aui.AUI_NB_CLOSE_ON_ACTIVE_TAB

        if evId == ID_NotebookAllowTabMove:
            self._notebook_style ^= aui.AUI_NB_TAB_MOVE

        if evId == ID_NotebookAllowTabExternalMove:
            self._notebook_style ^= aui.AUI_NB_TAB_EXTERNAL_MOVE

        elif evId == ID_NotebookAllowTabSplit:
            self._notebook_style ^= aui.AUI_NB_TAB_SPLIT

        elif evId == ID_NotebookTabFloat:
            self._notebook_style ^= aui.AUI_NB_TAB_FLOAT

        elif evId == ID_NotebookTabDrawDnd:
            self._notebook_style ^= aui.AUI_NB_DRAW_DND_TAB

        elif evId == ID_NotebookWindowList:
            self._notebook_style ^= aui.AUI_NB_WINDOWLIST_BUTTON

        elif evId == ID_NotebookScrollButtons:
            self._notebook_style ^= aui.AUI_NB_SCROLL_BUTTONS

        elif evId == ID_NotebookTabFixedWidth:
            self._notebook_style ^= aui.AUI_NB_TAB_FIXED_WIDTH

        elif evId == ID_NotebookHideSingle:
            self._notebook_style ^= aui.AUI_NB_HIDE_ON_SINGLE_TAB

        elif evId == ID_NotebookSmartTab:
            self._notebook_style ^= aui.AUI_NB_SMART_TABS

        elif evId == ID_NotebookUseImagesDropDown:
            self._notebook_style ^= aui.AUI_NB_USE_IMAGES_DROPDOWN

        elif evId == ID_NotebookCloseOnLeft:
            self._notebook_style ^= aui.AUI_NB_CLOSE_ON_TAB_LEFT

        all_panes = self._mgr.GetAllPanes()

        for pane in all_panes:

            if isinstance(pane.window, aui.AuiNotebook):
                nb = pane.window

                if evId == ID_NotebookArtGloss:

                    nb.SetArtProvider(aui.AuiDefaultTabArt())
                    self._notebook_theme = 0

                elif evId == ID_NotebookArtSimple:
                    nb.SetArtProvider(aui.AuiSimpleTabArt())
                    self._notebook_theme = 1

                elif evId == ID_NotebookArtVC71:
                    nb.SetArtProvider(aui.VC71TabArt())
                    self._notebook_theme = 2

                elif evId == ID_NotebookArtFF2:
                    nb.SetArtProvider(aui.FF2TabArt())
                    self._notebook_theme = 3

                elif evId == ID_NotebookArtVC8:
                    nb.SetArtProvider(aui.VC8TabArt())
                    self._notebook_theme = 4

                elif evId == ID_NotebookArtChrome:
                    nb.SetArtProvider(aui.ChromeTabArt())
                    self._notebook_theme = 5

                if nb.GetAGWWindowStyleFlag() & aui.AUI_NB_BOTTOM == 0:
                    nb.SetAGWWindowStyleFlag(self._notebook_style)

                if evId == ID_NotebookCloseButtonAll:
                    # Demonstrate how to remove a close button from a tab
                    nb.SetCloseButton(2, False)
                elif evId == ID_NotebookDclickUnsplit:
                    nb.SetSashDClickUnsplit(event.IsChecked())

                nb.Refresh()
                nb.Update()


    def OnUpdateUI(self, event):

        agwFlags = self._mgr.GetAGWFlags()
        evId = event.GetId()

        if evId == ID_NoGradient:
            event.Check(self._mgr.GetArtProvider().GetMetric(aui.AUI_DOCKART_GRADIENT_TYPE) == aui.AUI_GRADIENT_NONE)

        elif evId == ID_VerticalGradient:
            event.Check(self._mgr.GetArtProvider().GetMetric(aui.AUI_DOCKART_GRADIENT_TYPE) == aui.AUI_GRADIENT_VERTICAL)

        elif evId == ID_HorizontalGradient:
            event.Check(self._mgr.GetArtProvider().GetMetric(aui.AUI_DOCKART_GRADIENT_TYPE) == aui.AUI_GRADIENT_HORIZONTAL)

        elif evId == ID_AllowFloating:
            event.Check((agwFlags & aui.AUI_MGR_ALLOW_FLOATING) != 0)

        elif evId == ID_TransparentDrag:
            event.Check((agwFlags & aui.AUI_MGR_TRANSPARENT_DRAG) != 0)

        elif evId == ID_TransparentHint:
            event.Check((agwFlags & aui.AUI_MGR_TRANSPARENT_HINT) != 0)

        elif evId == ID_LiveUpdate:
            event.Check(aui.AuiManager_HasLiveResize(self._mgr))

        elif evId == ID_VenetianBlindsHint:
            event.Check((agwFlags & aui.AUI_MGR_VENETIAN_BLINDS_HINT) != 0)

        elif evId == ID_RectangleHint:
            event.Check((agwFlags & aui.AUI_MGR_RECTANGLE_HINT) != 0)

        elif evId == ID_NoHint:
            event.Check(((aui.AUI_MGR_TRANSPARENT_HINT |
                              aui.AUI_MGR_VENETIAN_BLINDS_HINT |
                              aui.AUI_MGR_RECTANGLE_HINT) & agwFlags) == 0)

        elif evId == ID_HintFade:
            event.Check((agwFlags & aui.AUI_MGR_HINT_FADE) != 0)

        elif evId == ID_NoVenetianFade:
            event.Check((agwFlags & aui.AUI_MGR_NO_VENETIAN_BLINDS_FADE) != 0)

        elif evId == ID_NativeMiniframes:
            event.Check(aui.AuiManager_UseNativeMiniframes(self._mgr))

        elif evId == ID_PaneIcons:
            event.Check(self._pane_icons)

        elif evId == ID_SmoothDocking:
            event.Check((agwFlags & aui.AUI_MGR_SMOOTH_DOCKING) != 0)

        elif evId == ID_AnimateFrames:
            event.Check((agwFlags & aui.AUI_MGR_ANIMATE_FRAMES) != 0)

        elif evId == ID_DefaultDockArt:
            event.Check(isinstance(self._mgr.GetArtProvider(), aui.AuiDefaultDockArt))

        elif evId == ID_ModernDockArt:
            event.Check(isinstance(self._mgr.GetArtProvider(), aui.ModernDockArt))

        elif evId == ID_SnapPanes:
            event.Check(self._snapped)

        elif evId == ID_FlyOut:
            pane = self._mgr.GetPane("test8")
            event.Check(pane.IsFlyOut())

        elif evId == ID_AeroGuides:
            event.Check(agwFlags & aui.AUI_MGR_AERO_DOCKING_GUIDES != 0)

        elif evId == ID_WhidbeyGuides:
            event.Check(agwFlags & aui.AUI_MGR_WHIDBEY_DOCKING_GUIDES != 0)

        elif evId == ID_StandardGuides:
            event.Check((agwFlags & aui.AUI_MGR_AERO_DOCKING_GUIDES == 0) and (agwFlags & aui.AUI_MGR_WHIDBEY_DOCKING_GUIDES == 0))

        elif evId == ID_CustomPaneButtons:
            event.Check(self._custom_pane_buttons)

        elif evId == ID_PreviewMinimized:
            event.Check(agwFlags & aui.AUI_MGR_PREVIEW_MINIMIZED_PANES)

        elif evId == ID_NotebookNoCloseButton:
            event.Check((self._notebook_style & (aui.AUI_NB_CLOSE_BUTTON|aui.AUI_NB_CLOSE_ON_ALL_TABS|aui.AUI_NB_CLOSE_ON_ACTIVE_TAB)) != 0)

        elif evId == ID_NotebookCloseButton:
            event.Check((self._notebook_style & aui.AUI_NB_CLOSE_BUTTON) != 0)

        elif evId == ID_NotebookCloseButtonAll:
            event.Check((self._notebook_style & aui.AUI_NB_CLOSE_ON_ALL_TABS) != 0)

        elif evId == ID_NotebookCloseButtonActive:
            event.Check((self._notebook_style & aui.AUI_NB_CLOSE_ON_ACTIVE_TAB) != 0)

        elif evId == ID_NotebookAllowTabSplit:
            event.Check((self._notebook_style & aui.AUI_NB_TAB_SPLIT) != 0)

        elif evId == ID_NotebookTabFloat:
            event.Check((self._notebook_style & aui.AUI_NB_TAB_FLOAT) != 0)

        elif evId == ID_NotebookDclickUnsplit:
            event.Check(self._main_notebook.GetSashDClickUnsplit())

        elif evId == ID_NotebookTabDrawDnd:
            event.Check((self._notebook_style & aui.AUI_NB_DRAW_DND_TAB) != 0)

        elif evId == ID_NotebookAllowTabMove:
            event.Check((self._notebook_style & aui.AUI_NB_TAB_MOVE) != 0)

        elif evId == ID_NotebookAllowTabExternalMove:
            event.Check((self._notebook_style & aui.AUI_NB_TAB_EXTERNAL_MOVE) != 0)

        elif evId == ID_NotebookScrollButtons:
            event.Check((self._notebook_style & aui.AUI_NB_SCROLL_BUTTONS) != 0)

        elif evId == ID_NotebookWindowList:
            event.Check((self._notebook_style & aui.AUI_NB_WINDOWLIST_BUTTON) != 0)

        elif evId == ID_NotebookTabFixedWidth:
            event.Check((self._notebook_style & aui.AUI_NB_TAB_FIXED_WIDTH) != 0)

        elif evId == ID_NotebookHideSingle:
            event.Check((self._notebook_style & aui.AUI_NB_HIDE_ON_SINGLE_TAB) != 0)

        elif evId == ID_NotebookSmartTab:
            event.Check((self._notebook_style & aui.AUI_NB_SMART_TABS) != 0)

        elif evId == ID_NotebookUseImagesDropDown:
            event.Check((self._notebook_style & aui.AUI_NB_USE_IMAGES_DROPDOWN) != 0)

        elif evId == ID_NotebookCloseOnLeft:
            event.Check((self._notebook_style & aui.AUI_NB_CLOSE_ON_TAB_LEFT) != 0)

        elif evId == ID_NotebookCustomButtons:
            event.Check(self._custom_tab_buttons)

        elif evId == ID_NotebookArtGloss:
            event.Check(self._notebook_theme == 0)

        elif evId == ID_NotebookArtSimple:
            event.Check(self._notebook_theme == 1)

        elif evId == ID_NotebookArtVC71:
            event.Check(self._notebook_theme == 2)

        elif evId == ID_NotebookArtFF2:
            event.Check(self._notebook_theme == 3)

        elif evId == ID_NotebookArtVC8:
            event.Check(self._notebook_theme == 4)

        elif evId == ID_NotebookArtChrome:
            event.Check(self._notebook_theme == 5)

        elif evId == ID_VetoTree:
            event.Check(self._veto_tree)

        elif evId == ID_VetoText:
            event.Check(self._veto_text)

        else:
            for ids in self._requestPanes:
                if evId == ids:
                    paneName = self._requestPanes[ids]
                    pane = self._mgr.GetPane(paneName)
                    event.Enable(pane.IsShown())


    def OnPaneClose(self, event):

        if event.pane.name == "test10":

            msg = "Are you sure you want to "
            if event.GetEventType() == aui.wxEVT_AUI_PANE_MINIMIZE:
                msg += "minimize "
            else:
                msg += "close/hide "

            res = wx.MessageBox(msg + "this pane?", "AUI", wx.YES_NO, self)
            if res != wx.YES:
                event.Veto()


    def OnCreatePerspective(self, event):

        dlg = wx.TextEntryDialog(self, "Enter a name for the new perspective:", "AUI Test")

        dlg.SetValue("Perspective %u"%(len(self._perspectives) + 1))
        if dlg.ShowModal() != wx.ID_OK:
            return

        if len(self._perspectives) == 0:
            self._perspectives_menu.AppendSeparator()

        self._perspectives_menu.Append(ID_FirstPerspective + len(self._perspectives), dlg.GetValue())
        self._perspectives.append(self._mgr.SavePerspective())


    def OnCopyPerspectiveCode(self, event):

        s = self._mgr.SavePerspective()

        if wx.TheClipboard.Open():

            wx.TheClipboard.SetData(wx.TextDataObject(s))
            wx.TheClipboard.Close()


    def OnRestorePerspective(self, event):

        self._mgr.LoadPerspective(self._perspectives[event.GetId() - ID_FirstPerspective])


    def OnCreateNBPerspective(self, event):

        dlg = wx.TextEntryDialog(self, "Enter a name for the new perspective:", "AUI Test")

        dlg.SetValue("Perspective %u"%(len(self._nb_perspectives) + 1))
        if dlg.ShowModal() != wx.ID_OK:
            return

        if len(self._nb_perspectives) == 0:
            self._nb_perspectives_menu.AppendSeparator()

        auibook = self._mgr.GetPane("notebook_content").window
        self._nb_perspectives_menu.Append(ID_FirstNBPerspective + len(self._nb_perspectives), dlg.GetValue())
        self._nb_perspectives.append(auibook.SavePerspective())


    def OnCopyNBPerspectiveCode(self, event):

        auibook = self._mgr.GetPane("notebook_content").window
        s = auibook.SavePerspective()

        if wx.TheClipboard.Open():

            wx.TheClipboard.SetData(wx.TextDataObject(s))
            wx.TheClipboard.Close()


    def OnRestoreNBPerspective(self, event):

        auibook = self._mgr.GetPane("notebook_content").window
        auibook.LoadPerspective(self._nb_perspectives[event.GetId() - ID_FirstNBPerspective])


    def OnGuides(self, event):

        useAero = event.GetId() == ID_AeroGuides
        useWhidbey = event.GetId() == ID_WhidbeyGuides
        agwFlags = self._mgr.GetAGWFlags()

        if useAero:
            agwFlags ^= aui.AUI_MGR_AERO_DOCKING_GUIDES
            agwFlags &= ~aui.AUI_MGR_WHIDBEY_DOCKING_GUIDES
        elif useWhidbey:
            agwFlags ^= aui.AUI_MGR_WHIDBEY_DOCKING_GUIDES
            agwFlags &= ~aui.AUI_MGR_AERO_DOCKING_GUIDES
        else:
            agwFlags &= ~aui.AUI_MGR_AERO_DOCKING_GUIDES
            agwFlags &= ~aui.AUI_MGR_WHIDBEY_DOCKING_GUIDES

        self._mgr.SetAGWFlags(agwFlags)


    def OnNotebookPageClose(self, event):

        ctrl = event.GetEventObject()
        if isinstance(ctrl.GetPage(event.GetSelection()), wx.html.HtmlWindow):

            res = wx.MessageBox("Are you sure you want to close/hide this notebook page?",
                                "AUI", wx.YES_NO, self)
            if res != wx.YES:
                event.Veto()


    def OnAllowNotebookDnD(self, event):

        # for the purpose of this test application, explicitly
        # allow all noteboko drag and drop events
        event.Allow()


    def GetStartPosition(self):

        x = 20
        pt = self.ClientToScreen(wx.Point(0, 0))
        return wx.Point(pt.x + x, pt.y + x)


    def OnCreateTree(self, event):

        self._mgr.AddPane(self.CreateTreeCtrl(), aui.AuiPaneInfo().
                          Caption("Tree Control").
                          Float().FloatingPosition(self.GetStartPosition()).
                          FloatingSize(wx.Size(150, 300)).MinimizeButton(True))
        self._mgr.Update()


    def OnCreateGrid(self, event):

        self._mgr.AddPane(self.CreateGrid(), aui.AuiPaneInfo().
                          Caption("Grid").
                          Float().FloatingPosition(self.GetStartPosition()).
                          FloatingSize(wx.Size(300, 200)).MinimizeButton(True))
        self._mgr.Update()


    def OnCreateHTML(self, event):

        self._mgr.AddPane(self.CreateHTMLCtrl(), aui.AuiPaneInfo().
                          Caption("HTML Control").
                          Float().FloatingPosition(self.GetStartPosition()).
                          FloatingSize(wx.Size(300, 200)).MinimizeButton(True))
        self._mgr.Update()


    def OnCreateNotebook(self, event):

        self._mgr.AddPane(self.CreateNotebook(), aui.AuiPaneInfo().
                          Caption("Notebook").
                          Float().FloatingPosition(self.GetStartPosition()).
                          CloseButton(True).MaximizeButton(True).MinimizeButton(True))
        self._mgr.Update()


    def OnCreateText(self, event):

        self._mgr.AddPane(self.CreateTextCtrl(), aui.AuiPaneInfo().
                          Caption("Text Control").
                          Float().FloatingPosition(self.GetStartPosition()).
                          MinimizeButton(True))
        self._mgr.Update()


    def OnCreateSizeReport(self, event):

        self._mgr.AddPane(self.CreateSizeReportCtrl(), aui.AuiPaneInfo().
                          Caption("Client Size Reporter").
                          Float().FloatingPosition(self.GetStartPosition()).
                          CloseButton(True).MaximizeButton(True).MinimizeButton(True))
        self._mgr.Update()


    def OnChangeContentPane(self, event):

        self._mgr.GetPane("grid_content").Show(event.GetId() == ID_GridContent)
        self._mgr.GetPane("text_content").Show(event.GetId() == ID_TextContent)
        self._mgr.GetPane("tree_content").Show(event.GetId() == ID_TreeContent)
        self._mgr.GetPane("sizereport_content").Show(event.GetId() == ID_SizeReportContent)
        self._mgr.GetPane("html_content").Show(event.GetId() == ID_HTMLContent)
        self._mgr.GetPane("notebook_content").Show(event.GetId() == ID_NotebookContent)
        self._mgr.Update()


    def OnVetoTree(self, event):

        self._veto_tree = event.IsChecked()


    def OnVetoText(self, event):

        self._veto_text = event.IsChecked()


    def OnRequestUserAttention(self, event):

        ids = event.GetId()
        if ids not in self._requestPanes:
            return

        paneName = self._requestPanes[ids]
        pane = self._mgr.GetPane(paneName)
        self._mgr.RequestUserAttention(pane.window)


    def OnDropDownToolbarItem(self, event):

        if event.IsDropDownClicked():

            tb = event.GetEventObject()
            tb.SetToolSticky(event.GetId(), True)

            # create the popup menu
            menuPopup = wx.Menu()
            bmp = wx.ArtProvider.GetBitmap(wx.ART_QUESTION, wx.ART_OTHER, wx.Size(16, 16))

            m1 =  wx.MenuItem(menuPopup, 10001, "Drop Down Item 1")
            m1.SetBitmap(bmp)
            menuPopup.Append(m1)

            m2 =  wx.MenuItem(menuPopup, 10002, "Drop Down Item 2")
            m2.SetBitmap(bmp)
            menuPopup.Append(m2)

            m3 =  wx.MenuItem(menuPopup, 10003, "Drop Down Item 3")
            m3.SetBitmap(bmp)
            menuPopup.Append(m3)

            m4 =  wx.MenuItem(menuPopup, 10004, "Drop Down Item 4")
            m4.SetBitmap(bmp)
            menuPopup.Append(m4)

            self.PopupMenu(menuPopup)

            # make sure the button is "un-stuck"
            tb.SetToolSticky(event.GetId(), False)


    def OnTabAlignment(self, event):

        for pane in self._mgr.GetAllPanes():

            if isinstance(pane.window, aui.AuiNotebook):

                nb = pane.window
                style = nb.GetAGWWindowStyleFlag()

                if event.GetId() == ID_NotebookAlignTop:
                    style &= ~aui.AUI_NB_BOTTOM
                    style ^= aui.AUI_NB_TOP
                    nb.SetAGWWindowStyleFlag(style)
                elif event.GetId() == ID_NotebookAlignBottom:
                    style &= ~aui.AUI_NB_TOP
                    style ^= aui.AUI_NB_BOTTOM
                    nb.SetAGWWindowStyleFlag(style)

                self._notebook_style = style
                nb.Update()
                nb.Refresh()


    def OnCustomTabButtons(self, event):

        checked = event.IsChecked()
        self._custom_tab_buttons = checked
        auibook = self._mgr.GetPane("notebook_content").window

        left = CUSTOM_TAB_BUTTONS["Left"]
        for btn, ids in left:
            if checked:
                auibook.AddTabAreaButton(ids, wx.LEFT, btn.GetBitmap())
            else:
                auibook.RemoveTabAreaButton(ids)

        right = CUSTOM_TAB_BUTTONS["Right"]
        for btn, ids in right:
            if checked:
                auibook.AddTabAreaButton(ids, wx.RIGHT, btn.GetBitmap())
            else:
                auibook.RemoveTabAreaButton(ids)

        auibook.Refresh()
        auibook.Update()


    def OnMinMaxTabWidth(self, event):

        auibook = self._mgr.GetPane("notebook_content").window
        minTabWidth, maxTabWidth = auibook.GetMinMaxTabWidth()

        dlg = wx.TextEntryDialog(self, "Enter the minimum and maximum tab widths, separated by a comma:",
                                 "AuiNotebook Tab Widths")

        dlg.SetValue("%d,%d"%(minTabWidth, maxTabWidth))
        if dlg.ShowModal() != wx.ID_OK:
            return

        value = dlg.GetValue()
        dlg.Destroy()

        try:
            minTabWidth, maxTabWidth = value.split(",")
            minTabWidth, maxTabWidth = int(minTabWidth), int(maxTabWidth)
        except:
            dlg = wx.MessageDialog(self, 'Invalid minimum/maximum tab width. Tab widths should be' \
                                   ' 2 integers separated by a comma.',
                                   'Error',
                                   wx.OK | wx.ICON_ERROR)
            dlg.ShowModal()
            dlg.Destroy()
            return

        if minTabWidth > maxTabWidth:
            dlg = wx.MessageDialog(self, 'Invalid minimum/maximum tab width. Minimum tab width' \
                                   ' should be less of equal than maximum tab width.',
                                   'Error',
                                   wx.OK | wx.ICON_ERROR)
            dlg.ShowModal()
            dlg.Destroy()
            return

        auibook.SetMinMaxTabWidth(minTabWidth, maxTabWidth)
        auibook.Refresh()
        auibook.Update()


    def OnPreview(self, event):

        auibook = self._mgr.GetPane("notebook_content").window
        auibook.NotebookPreview()


    def OnAddMultiLine(self, event):

        auibook = self._mgr.GetPane("notebook_content").window

        auibook.InsertPage(1, wx.TextCtrl(auibook, -1, "Some more text", wx.DefaultPosition, wx.DefaultSize,
                                          wx.TE_MULTILINE|wx.NO_BORDER), "Multi-Line\nTab Labels", True)

        auibook.SetPageTextColour(1, wx.BLUE)


    def OnFloatDock(self, event):

        paneLabel = event.pane.caption
        etype = event.GetEventType()

        strs = "Pane %s "%paneLabel
        if etype == aui.wxEVT_AUI_PANE_FLOATING:
            strs += "is about to be floated"

            if event.pane.name == "test8" and self._veto_tree:
                event.Veto()
                strs += "... Event vetoed by user selection!"
                self.log.write(strs + "\n")
                return

        elif etype == aui.wxEVT_AUI_PANE_FLOATED:
            strs += "has been floated"
        elif etype == aui.wxEVT_AUI_PANE_DOCKING:
            strs += "is about to be docked"

            if event.pane.name == "test11" and self._veto_text:
                event.Veto()
                strs += "... Event vetoed by user selection!"
                self.log.write(strs + "\n")
                return

        elif etype == aui.wxEVT_AUI_PANE_DOCKED:
            strs += "has been docked"

        self.log.write(strs + "\n")


    def OnExit(self, event):

        self.Close(True)


    def OnAbout(self, event):

        msg = "This Is The About Dialog Of The Pure Python Version Of AUI.\n\n" + \
              "Author: Andrea Gavana @ 23 Dec 2005\n\n" + \
              "Please Report Any Bug/Requests Of Improvements\n" + \
              "To Me At The Following Addresses:\n\n" + \
              "andrea.gavana@maerskoil.com\n" + "andrea.gavana@gmail.com\n\n" + \
              "Welcome To wxPython " + wx.VERSION_STRING + "!!"

        dlg = wx.MessageDialog(self, msg, "AUI Demo",
                               wx.OK | wx.ICON_INFORMATION)

        if wx.Platform != '__WXMAC__':
            dlg.SetFont(wx.Font(8, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL,
                                False, '', wx.FONTENCODING_DEFAULT))

        dlg.ShowModal()
        dlg.Destroy()


    def CreateTextCtrl(self, ctrl_text=""):

        if ctrl_text.strip():
            text = ctrl_text
        else:
            text = "This is text box %d"%self._textCount
            self._textCount += 1

        return wx.TextCtrl(self,-1, text, wx.Point(0, 0), wx.Size(150, 90),
                           wx.NO_BORDER | wx.TE_MULTILINE)


    def CreateGrid(self):

        grid = wx.grid.Grid(self, -1, wx.Point(0, 0), wx.Size(150, 250),
                            wx.NO_BORDER | wx.WANTS_CHARS)
        grid.CreateGrid(50, 20)
        return grid


    def CreateTreeCtrl(self):

        tree = wx.TreeCtrl(self, -1, wx.Point(0, 0), wx.Size(160, 250),
                           wx.TR_DEFAULT_STYLE | wx.NO_BORDER)

        imglist = wx.ImageList(16, 16, True, 2)
        imglist.Add(wx.ArtProvider.GetBitmap(wx.ART_FOLDER, wx.ART_OTHER, wx.Size(16, 16)))
        imglist.Add(wx.ArtProvider.GetBitmap(wx.ART_NORMAL_FILE, wx.ART_OTHER, wx.Size(16, 16)))
        tree.AssignImageList(imglist)

        root = tree.AddRoot("AUI Project", 0)
        items = []

        items.append(tree.AppendItem(root, "Item 1", 0))
        items.append(tree.AppendItem(root, "Item 2", 0))
        items.append(tree.AppendItem(root, "Item 3", 0))
        items.append(tree.AppendItem(root, "Item 4", 0))
        items.append(tree.AppendItem(root, "Item 5", 0))

        for item in items:
            tree.AppendItem(item, "Subitem 1", 1)
            tree.AppendItem(item, "Subitem 2", 1)
            tree.AppendItem(item, "Subitem 3", 1)
            tree.AppendItem(item, "Subitem 4", 1)
            tree.AppendItem(item, "Subitem 5", 1)

        tree.Expand(root)

        return tree


    def CreateSizeReportCtrl(self, width=80, height=80):

        ctrl = SizeReportCtrl(self, -1, wx.DefaultPosition, wx.Size(width, height), self._mgr)
        return ctrl


    def CreateHTMLCtrl(self, parent=None):

        if not parent:
            parent = self

        ctrl = wx.html.HtmlWindow(parent, -1, wx.DefaultPosition, wx.Size(400, 300))
        ctrl.SetPage(GetIntroText())
        return ctrl


    def CreateNotebook(self):

        # create the notebook off-window to avoid flicker
        client_size = self.GetClientSize()
        ctrl = aui.AuiNotebook(self, -1, wx.Point(client_size.x, client_size.y),
                              wx.Size(430, 200), agwStyle=self._notebook_style)

        arts = [aui.AuiDefaultTabArt, aui.AuiSimpleTabArt, aui.VC71TabArt, aui.FF2TabArt,
                aui.VC8TabArt, aui.ChromeTabArt]

        art = arts[self._notebook_theme]()
        ctrl.SetArtProvider(art)

        page_bmp = wx.ArtProvider.GetBitmap(wx.ART_NORMAL_FILE, wx.ART_OTHER, wx.Size(16, 16))
        ctrl.AddPage(self.CreateHTMLCtrl(ctrl), "Welcome to AUI", False, page_bmp)

        panel = wx.Panel(ctrl, -1)
        flex = wx.FlexGridSizer(rows=0, cols=2, vgap=2, hgap=2)
        flex.Add((5, 5))
        flex.Add((5, 5))
        flex.Add(wx.StaticText(panel, -1, "wxTextCtrl:"), 0, wx.ALL|wx.ALIGN_CENTRE, 5)
        flex.Add(wx.TextCtrl(panel, -1, "", wx.DefaultPosition, wx.Size(100, -1)),
                 1, wx.ALL|wx.ALIGN_CENTRE, 5)
        flex.Add(wx.StaticText(panel, -1, "wxSpinCtrl:"), 0, wx.ALL|wx.ALIGN_CENTRE, 5)
        flex.Add(wx.SpinCtrl(panel, -1, "5", wx.DefaultPosition, wx.Size(100, -1),
                             wx.SP_ARROW_KEYS, 5, 50, 5), 0, wx.ALL|wx.ALIGN_CENTRE, 5)
        flex.Add((5, 5))
        flex.Add((5, 5))
        flex.AddGrowableRow(0)
        flex.AddGrowableRow(3)
        flex.AddGrowableCol(1)
        panel.SetSizer(flex)
        ctrl.AddPage(panel, "Disabled", False, page_bmp)

        ctrl.AddPage(wx.TextCtrl(ctrl, -1, "Some text", wx.DefaultPosition, wx.DefaultSize,
                                 wx.TE_MULTILINE|wx.NO_BORDER), "DClick Edit!", False, page_bmp)

        ctrl.AddPage(wx.TextCtrl(ctrl, -1, "Some more text", wx.DefaultPosition, wx.DefaultSize,
                                 wx.TE_MULTILINE|wx.NO_BORDER), "Blue Tab")

        ctrl.AddPage(wx.TextCtrl(ctrl, -1, "Some more text", wx.DefaultPosition, wx.DefaultSize,
                                 wx.TE_MULTILINE|wx.NO_BORDER), "A Control")

        ctrl.AddPage(wx.TextCtrl(ctrl, -1, "Some more text", wx.DefaultPosition, wx.DefaultSize,
                                 wx.TE_MULTILINE|wx.NO_BORDER), "wxTextCtrl 4")

        ctrl.AddPage(wx.TextCtrl(ctrl, -1, "Some more text", wx.DefaultPosition, wx.DefaultSize,
                                 wx.TE_MULTILINE|wx.NO_BORDER), "wxTextCtrl 5")

        ctrl.AddPage(wx.TextCtrl(ctrl, -1, "Some more text", wx.DefaultPosition, wx.DefaultSize,
                                 wx.TE_MULTILINE|wx.NO_BORDER), "wxTextCtrl 6")

        ctrl.AddPage(wx.TextCtrl(ctrl, -1, "Some more text", wx.DefaultPosition, wx.DefaultSize,
                                 wx.TE_MULTILINE|wx.NO_BORDER), "wxTextCtrl 7 (longer title)")

        ctrl.AddPage(wx.TextCtrl(ctrl, -1, "Some more text", wx.DefaultPosition, wx.DefaultSize,
                                 wx.TE_MULTILINE|wx.NO_BORDER), "wxTextCtrl 8")

        # Demonstrate how to disable a tab
        ctrl.EnableTab(1, False)

        ctrl.SetPageTextColour(2, wx.RED)
        ctrl.SetPageTextColour(3, wx.BLUE)
        ctrl.SetRenamable(2, True)

        return ctrl


    def OnSwitchPane(self, event):

        items = ASD.SwitcherItems()
        items.SetRowCount(12)

        # Add the main windows and toolbars, in two separate columns
        # We'll use the item 'id' to store the notebook selection, or -1 if not a page

        for k in range(2):
            if k == 0:
                items.AddGroup(_("Main Windows"), "mainwindows")
            else:
                items.AddGroup(_("Toolbars"), "toolbars").BreakColumn()

            for pane in self._mgr.GetAllPanes():
                name = pane.name
                caption = pane.caption
                if not caption:
                    continue

                toolBar = isinstance(pane.window, wx.ToolBar) or isinstance(pane.window, aui.AuiToolBar)
                bitmap = (pane.icon.IsOk() and [pane.icon] or [wx.NullBitmap])[0]

                if (toolBar and k == 1) or (not toolBar and k == 0):
                    items.AddItem(caption, name, -1, bitmap).SetWindow(pane.window)

        # Now add the wxAuiNotebook pages
        items.AddGroup(_("Notebook Pages"), "pages").BreakColumn()

        for pane in self._mgr.GetAllPanes():
            nb = pane.window
            if isinstance(nb, aui.AuiNotebook):
                for j in range(nb.GetPageCount()):

                    name = nb.GetPageText(j)
                    win = nb.GetPage(j)

                    items.AddItem(name, name, j, nb.GetPageBitmap(j)).SetWindow(win)

        # Select the focused window

        idx = items.GetIndexForFocus()
        if idx != wx.NOT_FOUND:
            items.SetSelection(idx)

        if wx.Platform == "__WXMAC__":
            items.SetBackgroundColour(wx.WHITE)

        # Show the switcher dialog

        dlg = ASD.SwitcherDialog(items, self, self._mgr)

        # In GTK+ we can't use Ctrl+Tab; we use Ctrl+/ instead and tell the switcher
        # to treat / in the same was as tab (i.e. cycle through the names)

        if wx.Platform == "__WXGTK__":
            dlg.SetExtraNavigationKey('/')

        if wx.Platform == "__WXMAC__":
            dlg.SetBackgroundColour(wx.WHITE)
            dlg.SetModifierKey(wx.WXK_ALT)

        ans = dlg.ShowModal()

        if ans == wx.ID_OK and dlg.GetSelection() != -1:
            item = items.GetItem(dlg.GetSelection())

            if item.GetId() == -1:
                info = self._mgr.GetPane(item.GetName())
                info.Show()
                self._mgr.Update()
                info.window.SetFocus()

            else:
                nb = item.GetWindow().GetParent()
                win = item.GetWindow()
                if isinstance(nb, aui.AuiNotebook):
                    nb.SetSelection(item.GetId())
                    win.SetFocus()


def GetIntroText():

    text = \
    "<html><body>" \
    "<h3>Welcome to AUI</h3>" \
    "<br/><b>Overview</b><br/>" \
    "<p>AUI is an Advanced User Interface library for the wxPython toolkit " \
    "that allows developers to create high-quality, cross-platform user " \
    "interfaces quickly and easily.</p>" \
    "<p><b>Features</b></p>" \
    "<p>With AUI, developers can create application frameworks with:</p>" \
    "<ul>" \
    "<li>Native, dockable floating frames</li>" \
    "<li>Perspective saving and loading</li>" \
    "<li>Native toolbars incorporating real-time, 'spring-loaded' dragging</li>" \
    "<li>Customizable floating/docking behavior</li>" \
    "<li>Completely customizable look-and-feel</li>" \
    "<li>Optional transparent window effects (while dragging or docking)</li>" \
    "<li>Splittable notebook control</li>" \
    "</ul>" \
    "<p><b>What's new in AUI?</b></p>" \
    "<p>Current wxAUI Version Tracked: wxWidgets 2.9.4 (SVN HEAD)" \
    "<p>The wxPython AUI version fixes the following bugs or implement the following" \
    " missing features (the list is not exhaustive): " \
    "<p><ul>" \
    "<li>Visual Studio 2005 style docking: <a href='http://www.kirix.com/forums/viewtopic.php?f=16&t=596'>" \
    "http://www.kirix.com/forums/viewtopic.php?f=16&t=596</a></li>" \
    "<li>Dock and Pane Resizing: <a href='http://www.kirix.com/forums/viewtopic.php?f=16&t=582'>" \
    "http://www.kirix.com/forums/viewtopic.php?f=16&t=582</a></li> " \
    "<li>Patch concerning dock resizing: <a href='http://www.kirix.com/forums/viewtopic.php?f=16&t=610'>" \
    "http://www.kirix.com/forums/viewtopic.php?f=16&t=610</a></li> " \
    "<li>Patch to effect wxAuiToolBar orientation switch: <a href='http://www.kirix.com/forums/viewtopic.php?f=16&t=641'>" \
    "http://www.kirix.com/forums/viewtopic.php?f=16&t=641</a></li> " \
    "<li>AUI: Core dump when loading a perspective in wxGTK (MSW OK): <a href='http://www.kirix.com/forums/viewtopic.php?f=15&t=627</li>'>" \
    "http://www.kirix.com/forums/viewtopic.php?f=15&t=627</li></a>" \
    "<li>wxAuiNotebook reordered AdvanceSelection(): <a href='http://www.kirix.com/forums/viewtopic.php?f=16&t=617'>"\
    "http://www.kirix.com/forums/viewtopic.php?f=16&t=617</a></li> " \
    "<li>Vertical Toolbar Docking Issue: <a href='http://www.kirix.com/forums/viewtopic.php?f=16&t=181'>" \
    "http://www.kirix.com/forums/viewtopic.php?f=16&t=181</a></li> " \
    "<li>Patch to show the resize hint on mouse-down in aui: <a href='http://trac.wxwidgets.org/ticket/9612'>" \
    "http://trac.wxwidgets.org/ticket/9612</a></li> " \
    "<li>The Left/Right and Top/Bottom Docks over draw each other: <a href='http://trac.wxwidgets.org/ticket/3516'>" \
    "http://trac.wxwidgets.org/ticket/3516</a></li>" \
    "<li>MinSize() not honoured: <a href='http://trac.wxwidgets.org/ticket/3562'>" \
    "http://trac.wxwidgets.org/ticket/3562</a></li> " \
    "<li>Layout problem with wxAUI: <a href='http://trac.wxwidgets.org/ticket/3597'>" \
    "http://trac.wxwidgets.org/ticket/3597</a></li>" \
    "<li>Resizing children ignores current window size: <a href='http://trac.wxwidgets.org/ticket/3908'>" \
    "http://trac.wxwidgets.org/ticket/3908</a></li> " \
    "<li>Resizing panes under Vista does not repaint background: <a href='http://trac.wxwidgets.org/ticket/4325'>" \
    "http://trac.wxwidgets.org/ticket/4325</a></li> " \
    "<li>Resize sash resizes in response to click: <a href='http://trac.wxwidgets.org/ticket/4547'>" \
    "http://trac.wxwidgets.org/ticket/4547</a></li> " \
    "<li>'Illegal' resizing of the AuiPane? (wxPython): <a href='http://trac.wxwidgets.org/ticket/4599'>" \
    "http://trac.wxwidgets.org/ticket/4599</a></li> " \
    "<li>Floating wxAUIPane Resize Event doesn't update its position: <a href='http://trac.wxwidgets.org/ticket/9773'>" \
    "http://trac.wxwidgets.org/ticket/9773</a></li>" \
    "<li>Don't hide floating panels when we maximize some other panel: <a href='http://trac.wxwidgets.org/ticket/4066'>"\
    "http://trac.wxwidgets.org/ticket/4066</a></li>" \
    "<li>wxAUINotebook incorrect ALLOW_ACTIVE_PANE handling: <a href='http://trac.wxwidgets.org/ticket/4361'>" \
    "http://trac.wxwidgets.org/ticket/4361</a></li> " \
    "<li>Page changing veto doesn't work, (patch supplied): <a href='http://trac.wxwidgets.org/ticket/4518'>" \
    "http://trac.wxwidgets.org/ticket/4518</a></li> " \
    "<li>Show and DoShow are mixed around in wxAuiMDIChildFrame: <a href='http://trac.wxwidgets.org/ticket/4567'>"\
    "http://trac.wxwidgets.org/ticket/4567</a></li> " \
    "<li>wxAuiManager & wxToolBar - ToolBar Of Size Zero: <a href='http://trac.wxwidgets.org/ticket/9724'>" \
    "http://trac.wxwidgets.org/ticket/9724</a></li> " \
    "<li>wxAuiNotebook doesn't behave properly like a container as far as...: <a href='http://trac.wxwidgets.org/ticket/9911'>" \
    "http://trac.wxwidgets.org/ticket/9911</a></li>" \
    "<li>Serious layout bugs in wxAUI: <a href='http://trac.wxwidgets.org/ticket/10620'>" \
    "http://trac.wxwidgets.org/ticket/10620</a></li>" \
    "<li>wAuiDefaultTabArt::Clone() should just use copy constructor: <a href='http://trac.wxwidgets.org/ticket/11388'>" \
    "http://trac.wxwidgets.org/ticket/11388</a></li>" \
    "<li>Drop down button for check tool on wxAuiToolbar: <a href='http://trac.wxwidgets.org/ticket/11139'>" \
    "http://trac.wxwidgets.org/ticket/11139</a></li>" \
    "<li>Rename a wxAuiNotebook tab with double-click: <a href='http://trac.wxwidgets.org/ticket/10847'>" \
    "http://trac.wxwidgets.org/ticket/10847</a></li>" \
    "</ul>" \
    "<p>Plus the following features:" \
    "<p><ul>" \
    "<li><b>AuiManager:</b></li>" \
    "<ul>" \
    "<li>Implementation of a simple minimize pane system: Clicking on this minimize button causes a new " \
    "<i>AuiToolBar</i> to be created and added to the frame manager, (currently the implementation is such " \
    "that panes at West will have a toolbar at the right, panes at South will have toolbars at the " \
    "bottom etc...) and the pane is hidden in the manager. " \
    "Clicking on the restore button on the newly created toolbar will result in the toolbar being " \
    "removed and the original pane being restored;</li>" \
    "<li>Panes can be docked on top of each other to form <i>AuiNotebooks</i>; <i>AuiNotebooks</i> tabs can be torn " \
    "off to create floating panes;</li>" \
    "<li>On Windows XP, use the nice sash drawing provided by XP while dragging the sash;</li>" \
    "<li>Possibility to set an icon on docked panes;</li>" \
    "<li>Possibility to draw a sash visual grip, for enhanced visualization of sashes;</li>" \
    "<li>Implementation of a native docking art (<i>ModernDockArt</i>). Windows XP only, <b>requires</b> Mark Hammond's " \
    "pywin32 package (winxptheme);</li>" \
    "<li>Possibility to set a transparency for floating panes (a la Paint .NET);</li>" \
    "<li>Snapping the main frame to the screen in any positin specified by horizontal and vertical " \
    "alignments;</li>" \
    "<li>Snapping floating panes on left/right/top/bottom or any combination of directions, a la Winamp;</li>" \
    "<li>'Fly-out' floating panes, i.e. panes which show themselves only when the mouse hover them;</li>" \
    "<li>Ability to set custom bitmaps for pane buttons (close, maximize, etc...);</li>" \
    "<li>Implementation of the style <tt>AUI_MGR_ANIMATE_FRAMES</tt>, which fade-out floating panes when " \
    "they are closed (all platforms which support frames transparency) and show a moving rectangle " \
    "when they are docked and minimized (Windows excluding Vista and GTK only);</li>" \
    "<li>A pane switcher dialog is available to cycle through existing AUI panes; </li>" \
    "<li>Some flags which allow to choose the orientation and the position of the minimized panes;</li>" \
    "<li>The functions <i>[Get]MinimizeMode()</i> in <i>AuiPaneInfo</i> which allow to set/get the flags described above;</li>" \
    "<li>Events like <tt>EVT_AUI_PANE_DOCKING</tt>, <tt>EVT_AUI_PANE_DOCKED</tt>, <tt>EVT_AUI_PANE_FLOATING</tt> "\
    "and <tt>EVT_AUI_PANE_FLOATED</tt> are "\
    "available for all panes <b>except</b> toolbar panes;</li>" \
    "<li>Implementation of the <i>RequestUserAttention</i> method for panes;</li>" \
    "<li>Ability to show the caption bar of docked panes on the left instead of on the top (with caption " \
    "text rotated by 90 degrees then). This is similar to what <i>wxDockIt</i> did. To enable this feature on any " \
    "given pane, simply call <i>CaptionVisible(True, left=True)</i>;</li>" \
    "<li>New Aero-style docking guides: you can enable them by using the <i>AuiManager</i> style <tt>AUI_MGR_AERO_DOCKING_GUIDES</tt>;</li>" \
    "<li>New Whidbey-style docking guides: you can enable them by using the <i>AuiManager</i> style <tt>AUI_MGR_WHIDBEY_DOCKING_GUIDES</tt>;</li>" \
    "<li>A slide-in/slide-out preview of minimized panes can be seen by enabling the <i>AuiManager</i> style" \
    "<tt>AUI_MGR_PREVIEW_MINIMIZED_PANES</tt> and by hovering with the mouse on the minimized pane toolbar tool;</li>" \
    "<li>Native of custom-drawn mini frames can be used as floating panes, depending on the <tt>AUI_MGR_USE_NATIVE_MINIFRAMES</tt> style;</li>" \
    "<li>A 'smooth docking effect' can be obtained by using the <tt>AUI_MGR_SMOOTH_DOCKING</tt> style (similar to PyQT docking style);</li>" \
    '<li>Implementation of "Movable" panes, i.e. a pane that is set as `Movable()` but not `Floatable()` can be dragged and docked into a new location but will not form a floating window in between.</li>' \
    "</ul><p>" \
    "<li><b>AuiNotebook:</b></li>" \
    "<ul>" \
    "<li>Implementation of the style <tt>AUI_NB_HIDE_ON_SINGLE_TAB</tt>, a la <i>wx.lib.agw.flatnotebook</i>;</li>" \
    "<li>Implementation of the style <tt>AUI_NB_SMART_TABS</tt>, a la <i>wx.lib.agw.flatnotebook</i>;</li>" \
    "<li>Implementation of the style <tt>AUI_NB_USE_IMAGES_DROPDOWN</tt>, which allows to show tab images " \
    "on the tab dropdown menu instead of bare check menu items (a la <i>wx.lib.agw.flatnotebook</i>);</li>" \
    "<li>6 different tab arts are available, namely:</li>" \
    "<ul>" \
    "<li>Default 'glossy' theme (as in <i>wx.aui.AuiNotebook</i>)</li>" \
    "<li>Simple theme (as in <i>wx.aui.AuiNotebook</i>)</li>" \
    "<li>Firefox 2 theme</li>" \
    "<li>Visual Studio 2003 theme (VC71)</li>" \
    "<li>Visual Studio 2005 theme (VC81)</li>" \
    "<li>Google Chrome theme</li>" \
    "</ul>" \
    "<li>Enabling/disabling tabs;</li>" \
    "<li>Setting the colour of the tab's text; </li>" \
    "<li>Implementation of the style <tt>AUI_NB_CLOSE_ON_TAB_LEFT</tt>, which draws the tab close button on " \
    "the left instead of on the right (a la Camino browser); </li>" \
    "<li>Ability to save and load perspectives in <i>wx.aui.AuiNotebook</i> (experimental); </li>" \
    "<li>Possibility to add custom buttons in the <i>wx.aui.AuiNotebook</i> tab area; </li>" \
    "<li>Implementation of the style <tt>AUI_NB_TAB_FLOAT</tt>, which allows the floating of single tabs. " \
    "<b>Known limitation:</b> when the notebook is more or less full screen, tabs cannot be dragged far " \
    "enough outside of the notebook to become floating pages. </li>" \
    "<li>Implementation of the style <tt>AUI_NB_DRAW_DND_TAB</tt> (on by default), which draws an image " \
    "representation of a tab while dragging;</li>" \
    "<li>Implementation of the <i>AuiNotebook</i> unsplit functionality, which unsplit a splitted AuiNotebook " \
    "when double-clicking on a sash (Use <i>SetSashDClickUnsplit</i>);</li>" \
    "<li>Possibility to hide all the tabs by calling <i>HideAllTAbs</i>;</li>" \
    "<li>wxPython controls can now be added inside page tabs by calling <i>AddControlToPage</i>, and they can be " \
    "removed by calling <i>RemoveControlFromPage</i>;</li>" \
    "<li>Possibility to preview all the pages in a <i>AuiNotebook</i> (as thumbnails) by using the <i>NotebookPreview</i> " \
    "method of <i>AuiNotebook</i></li>;" \
    "<li>Tab labels can be edited by calling the <i>SetRenamable</i> method on a <i>AuiNotebook</i> page;</li>" \
    "<li>Support for multi-lines tab labels in <i>AuiNotebook</i>;</li>" \
    "<li>Support for setting minimum and maximum tab widths for fixed width tabs;</li>"\
    "<li>Implementation of the style <tt>AUI_NB_ORDER_BY_ACCESS</tt>, which orders the tabs by last access time inside the "\
    "<i>Tab Navigator</i> dialog</li>;" \
    "<li>Implementation of the style <tt>AUI_NB_NO_TAB_FOCUS</tt>, allowing the developer not to draw the tab " \
    "focus rectangle on tne <i>AuiNotebook</i> tabs.</li>"\
    "</ul><p>" \
    "<li><b>AuiToolBar:</b></li>" \
    "<ul>" \
    "<li><tt>AUI_TB_PLAIN_BACKGROUND</tt> style that allows to easy setup a plain background to the AUI toolbar, " \
    "without the need to override drawing methods. This style contrasts with the default behaviour " \
    "of the <i>wx.aui.AuiToolBar</i> that draws a background gradient and this break the window design when " \
    "putting it within a control that has margin between the borders and the toolbar (example: put " \
    "<i>wx.aui.AuiToolBar</i> within a <i>wx.StaticBoxSizer</i> that has a plain background);</li>" \
    "<li><i>AuiToolBar</i> allow item alignment: <a href='http://trac.wxwidgets.org/ticket/10174'> " \
    "http://trac.wxwidgets.org/ticket/10174</a>;</li>" \
    "<li><i>AUIToolBar</i> <i>DrawButton()</i> improvement: <a href='http://trac.wxwidgets.org/ticket/10303'>" \
    "http://trac.wxwidgets.org/ticket/10303</a>;</li>" \
    "<li><i>AuiToolBar</i> automatically assign new id for tools: <a href='http://trac.wxwidgets.org/ticket/10173'>" \
    "http://trac.wxwidgets.org/ticket/10173</a>;</li>" \
    "<li><i>AuiToolBar</i> Allow right-click on any kind of button: <a href='http://trac.wxwidgets.org/ticket/10079'>" \
    "http://trac.wxwidgets.org/ticket/10079</a>;</li>" \
    "<li><i>AuiToolBar</i> idle update only when visible: <a href='http://trac.wxwidgets.org/ticket/10075'>" \
    "http://trac.wxwidgets.org/ticket/10075</a>;</li>" \
    "<li>Ability of creating <i>AuiToolBar</i> tools with [counter]clockwise rotation. This allows to propose a " \
    "variant of the minimizing functionality with a rotated button which keeps the caption of the pane as label;</li>" \
    "<li>Allow setting the alignment of all tools in a toolbar that is expanded.</li>" \
    "<li>Implementation of the <tt>AUI_MINIMIZE_POS_TOOLBAR</tt> flag, which allows to minimize a pane inside " \
     "an existing toolbar. Limitation: if the minimized icon in the toolbar ends up in the overflowing " \
     "items (i.e., a menu is needed to show the icon), this style will not work.</li>" \
    "</ul>" \
    "</ul><p>" \
    "<p>" \
    "</body></html>"

    return text


#----------------------------------------------------------------------

class ParentFrame(aui.AuiMDIParentFrame):

    def __init__(self, parent):

        aui.AuiMDIParentFrame.__init__(self, parent, -1, title="AGW AuiMDIParentFrame",
                                       size=(640,480), style=wx.DEFAULT_FRAME_STYLE)
        self.count = 0

        # set frame icon
        self.SetIcon(images.Mondrian.GetIcon())

        mb = self.MakeMenuBar()
        self.SetMenuBar(mb)
        self.CreateStatusBar()


    def MakeMenuBar(self):

        mb = wx.MenuBar()
        menu = wx.Menu()
        item = menu.Append(-1, "New child window\tCtrl-N")
        self.Bind(wx.EVT_MENU, self.OnNewChild, item)
        item = menu.Append(-1, "Close parent")
        self.Bind(wx.EVT_MENU, self.OnDoClose, item)
        mb.Append(menu, "&File")
        return mb


    def OnNewChild(self, evt):

        self.count += 1
        child = ChildFrame(self, self.count)
        child.Show()


    def OnDoClose(self, evt):
        self.Close()


#----------------------------------------------------------------------

class ChildFrame(aui.AuiMDIChildFrame):

    def __init__(self, parent, count):

        aui.AuiMDIChildFrame.__init__(self, parent, -1, title="Child: %d" % count)
        mb = parent.MakeMenuBar()
        menu = wx.Menu()
        item = menu.Append(-1, "This is child %d's menu" % count)
        mb.Append(menu, "&Child")
        self.SetMenuBar(mb)

        p = wx.Panel(self)
        wx.StaticText(p, -1, "This is child %d" % count, (10,10))
        p.SetBackgroundColour('light blue')

        sizer = wx.BoxSizer()
        sizer.Add(p, 1, wx.EXPAND)
        self.SetSizer(sizer)

        wx.CallAfter(self.Layout)


#---------------------------------------------------------------------------

def MainAUI(parent, log):

    frame = AuiFrame(parent, -1, "AUI Test Frame", size=(800, 600), log=log)
    frame.CenterOnScreen()
    frame.Show()


#---------------------------------------------------------------------------

def MDIAUI(parent, log):

    frame = ParentFrame(parent)
    frame.CenterOnScreen()
    frame.Show()

#---------------------------------------------------------------------------


class TestPanel(wx.Panel):
    def __init__(self, parent, log):
        self.log = log
        wx.Panel.__init__(self, parent, -1)

        b1 = wx.Button(self, -1, " AGW AUI Docking Library ", (50,50))
        self.Bind(wx.EVT_BUTTON, self.OnButton1, b1)

##        b2 = wx.Button(self, -1, " AGW AuiMDIs ", (50, 80))
##        self.Bind(wx.EVT_BUTTON, self.OnButton2, b2)


    def OnButton1(self, event):
        self.win = MainAUI(self, self.log)


    def OnButton2(self, event):
        self.win = MDIAUI(self, self.log)

#----------------------------------------------------------------------

def runTest(frame, nb, log):

    win = TestPanel(nb, log)
    return win

#----------------------------------------------------------------------


overview = GetIntroText()


if __name__ == '__main__':
    import sys,os
    import run
    run.main(['', os.path.basename(sys.argv[0])] + sys.argv[1:])
