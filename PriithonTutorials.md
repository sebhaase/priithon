# PriithonTutorials #

Learning is best done by browsing and excercising (working / complete) examples



# From the PriithonHandbook #



## Demo 1: synthetic "star/bead images" ##

Simulation of 2d images of resolution limited point sources with two types of noise sources:

```
>>> a = F.gaussianArr((256,256), sigma=3, peakVal=100, orig=0, wrap=1) # shape of a perfect bead
>>> b = F.poissonArr((256,256), mean=.001)        # random bead positions
>>> c = 100 + F.convolve(a,b)
>>> d = c + F.noiseArr((256,256), stddev=1)
>>> e = F.poissonize(d)
>>> Y.view(c) # noise free
>>> Y.view(e) # with "readout" noise and quantum shot noise
```



## Demo 2: image file analysis ##

Image analysis of data saved in ''any'' file format

```

  Drag image-file into PyShell window (jpg,bmp,tiff, ... or fits or MRC/Priism format)
  Select: 'view'

>>> a = Y.vd(-1) # get data from latest viewer
>>> U.mmms(a) # show min,max,mean,stddev of whole (nd)data-set


 # set viewer into mode so that each left-mouse-click shows a line profile
 #   (averaged over deltaY=15 pixel) in graph-plot window

>>> Y.vLeftClickHorizProfile(-1, 15, '-+')

 # click into the image viewer window !

```







# some first steps in image processing #



## interactive session ##

```

>>> a = F.noiseArr(shape=(256, 256), stddev=1.0, mean=0.0, type=N.float32)
# window: 0) a
>>> Y.view(a)
>>> b = F.gaussianArr(shape=(256, 256), sigma=3, integralScale=None, peakVal=1, orig=0, wrap=True, type=N.float32)
# window: 1) b
>>> Y.view(b)
>>> c = F.convolve(a, b, conj=0, killDC=0)
# window: 3) c
>>> Y.view(c)
>>> def doit(a):
...     b = F.gaussianArr(shape=a.shape, sigma=3, integralScale=None, peakVal=1, orig=0, wrap=True, type=N.float32)
...     c = F.convolve(a, b, conj=0, killDC=0)
...     Y.view(b)
...     

>>> 
>>> 
>>> w = F.ringArr(shape=(256, 256), radius1=20, radius2=40, orig=None, wrap=0, type=N.float32)
# window: 4) w
>>> Y.view(w)
# window: 5) b
>>> doit(w)
>>> def doit2(a, sigma=3):
...     '''
...     this low-pass filters with gaussian 
...     gaussian sigma can be specified (or defaults to 3)
...     '''
...     b = F.gaussianArr(shape=a.shape, sigma=3, integralScale=None, peakVal=1, orig=0, wrap=True, type=N.float32)
...     c = F.convolve(a, b, conj=0, killDC=0)
...     Y.view(c)
...     
>>> 
# window: 7) c
>>> doit2(w+a, sigma=3)
```



## from a "script-file" ##

put this into a file `listInfo.py` ! You can either execute this from a unix terminal with

```
priithon listInfo.py
```

or -- if you

  1. set the 'x' (executable) permission (( `chmod +x listInfo.py` )) you can even call it by
  1. make sure to include the first line (`#!/usr/bin/env priithon`) and hope that it really finds your priithon installation in the shell `$PATH`

```
listInfo.py
#or you might need:
./listInfo.py

```

```
#!/usr/bin/env priithon

from Priithon.all import * # this preload all Priithon-modules the same way as the interactive shell


import glob
dd = glob.glob('/home/haase/Brandeis/2004_Nov/*.mrc')
# here you could "drag and drop" a multiple files and assign var name 'dd'
dd.sort()


for f in dd:
    print '================================'
    print f
    print '================================'
    a = Mrc.bindFile(f)
    print a.Mrc.info()
    print "recalculate Min/Max/Mean/Stddev over all sections:"
    print U.mmms(a)
    print "min/max/mean of first extended header float from all sections:"
    print U.mmm(a.Mrc.extFloats[:,0])
```



# The simplest standalone GUI program #



Here is a boiled down GUI program. For a more complete one see next section.

However, this still contains -- at the end of the file -- the obligatory ` if __name__ == '__main__' ` check, that allows to also import the file as a module. In the case `__name__` is NOT '`__main__`' !

The rest is "short-circuited" by using the oh-so-powerful  `Y.buttonbox`



Put this into a file `gui.py` ! You can either execute this from a unix terminal with

```
priithon gui.py
```

or -- if you

  1. make sure to include the first line (`#!/usr/bin/env priithon`) and hope that it really finds your priithon installation in the shell `$PATH`
  1. set the 'x' (executable) permission (( `chmod +x gui.py` ))



you can even call it by

```
gui.py
#or you might need:
./gui.py
```


```
#!/usr/bin/env priithon

## this a template for the 
## most simple / standalone GUI program

import sys
sys.app = None # dummy to force Priithon.Y getting loaded
import wx
from Priithon.all import Y # *

def main():
    Y.buttonBox([
        ('hello', 'wx.MessageBox("Welcome to Priithon GUI !")'),
        ('ask',   'a=wx.GetTextFromUser("enter var a:")'),
        '\n',
        ('shell', 'Y.shell()')
        ])

if __name__ == '__main__':
    if wx.GetApp():
        main()
    else:
        import sys
        sys.app = wx.PySimpleApp()
        main()

        sys.app.MainLoop()
```



# Another simple standalone GUI program #



A wxPython GUI program requires some -- essentially always constant -- extra lines of code.

  * at the end of the file the ` if __name__ == '__main__' ` check, that allows to also import the file as a module ( this is the case when `__name__` is NOT '`__main__`')
  * the application class that starts everything (if PyShell is not already running
  * the frame class that shows the "main window"