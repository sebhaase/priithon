""" use
from Priithon.all import *
to get access to all the modules like na,U,Y,...
"""
__author__  = "Sebastian Haase <haase@msg.ucsf.edu>"
__license__ = "BSD license - see LICENSE file"

## __all__ = ["priism", "seb"]
#  #from priism import *
#  from priism.priism   import *
#  from seb.seb         import *
#  from bettina.bettina import *
#  from lin.lin         import *
#  from willy.willy     import *

# aaa=45

#  from sys import getrefcount as rc

_broken=""

#20060719 try:
#20060719     import priism  as P
#20060719 except:    _broken +=" P"
try:
    import numpy as N
except:    _broken +=" N"

# try:
#     import numarray as na
# except:    _broken +=" na"
#  try:
#      from numarray import random_array as ra
#  except:    _broken +=" ra"


#  try:
#      import ArrayIO as A # needs Scientific.IO.TextFile
#  except:    _broken +="  A"

#interesting stuff is in useful anyway...
#  try:
#      from PIL import Image as I # PIL
#  except:    _broken +="  I"

import useful as U
import fftfuncs as F
try:
    import Mrc
except:    _broken +=" Mrc"


#20060719 #try:
#20060719 import seb     as S
#20060719 #except:    _broken +=" seb"

try:
    import usefulX as Y
    FN = Y.FN
    DIR = Y.DIR
except:    _broken +="  Y"
try:
    import pylab as P
except:    _broken +="  P"

if _broken != "":
    print " * couldn't load module(s): ", _broken
