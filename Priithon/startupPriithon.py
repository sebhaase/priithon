"""this is the minimal priithon (non GUI) startup file"""

__author__  = "Sebastian Haase <haase@msg.ucsf.edu>"
__license__ = "BSD license - see LICENSE file"

import __main__
exec "from Priithon.all import *" in __main__.__dict__
__main__.U._fixDisplayHook()
__main__.U._execPriithonRunCommands()

#20051117-TODO: CHECK if good idea  U.naSetArrayPrintMode(precision=4, suppress_small=0)
