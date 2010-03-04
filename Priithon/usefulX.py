"Priithon Y module: all functions to do with GUI - imports * from usefulX2"

__author__  = "Sebastian Haase <haase@msg.ucsf.edu>"
__license__ = "BSD license - see LICENSE file"

##### from google:
#  #  > Btw, I just noticed that importing scipy assumes that wxPython is
#  #  > installed and DISPLAY must be working. When trying to import scipy
#  #  from a
#  #  > different computer without X connection, I get:
#  #  > 
#  #  > >>> import scipy
#  #  > 
#  #  > Gtk-WARNING **: cannot open display:
#  #  > 
#  #  > and python quits. Any idea how to fix this?

import sys
if hasattr(sys,'app'): # HACK: we use this as indicator for a graphic enabled environmaent
    from usefulX2 import *
    from usefulX2 import _bugXiGraphics #20070126 _bugOSX1036, 
else:
    def refresh():
        import sys
        sys.stdout.flush()
        sys.stderr.flush()
    def FN(verbose=0):
        raise "* sorry no GUI *"
    def DIR(verbose=0):
        raise "* sorry no GUI *"


del sys
