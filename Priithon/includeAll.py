"""this is the GUI (PyShell) startup file"""
from __future__ import absolute_import

__author__  = "Sebastian Haase <haase@msg.ucsf.edu>"
__license__ = "BSD license - see LICENSE file"

print "   !!!  Welcome to Priithon !!!"
#from .all import *
#SyntaxError: 'import *' not allowed with 'from .'
#<hack>
from . import all
for n in all.__dict__:
    if not n.startswith('_'):
        exec "%s = all.%s" % (n,n)
del n, all
#</hack>

def _sebsDisplHook(v):
    if not v is None: # != None:
        import __main__ #global _
        #_ = v
        __main__._ = v
        print U.myStr(v)
        
import sys
sys.displayhook = _sebsDisplHook
#print "debug: Pr/includeAll"
#if sys.argv[1:]:
#    import string
#    print "start->eval:", sys.argv[1:]
#    eval(string.join(sys.argv[1:]))

#20051117-TODO: CHECK if good idea  U.naSetArrayPrintMode(precision=4, suppress_small=0)

import wx
if hasattr(sys,'argv') and wx.GetApp() is not None: # CHECK: in embedded wxPython sys,.argv not defined
    # sys.app not defined yet
    wx.GetApp().GetTopWindow().SetTitle("priithon on %s" % wx.GetHostName())
del wx
del sys
