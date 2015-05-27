## page was renamed from PriithonChangeLog
2007-02-16
  * on Linux:   `priithon` is now an alias for `priithonN`  === to use the old (numarray) priithon, use `priithon24`


2007-02-11
  * added support for Numpy scalars to SWIG typemaps
  * added test for "not byte-swapped" into SWIG typemaps
  * added `U.binaryRepr(x)` -- returns x in binary representation as string of 0s and 1s

2007-01-31
  * added `'b'` to file-open() in `Mrc` load and save -- seems very important on Windows !

2007-01-08
  * added auto-completion on TAB-key into Priithon-shell
  * buttonBox now supports TextFields and CheckBoxes -- see buttonbox.py

2007-01-02
  * `U.DEBUG_HERE()`    shortcut for  `import pdb;  pdb.set_trace`

2006-11-01
  * added `Y.plotClear()` to simplify: `Y.plothold(0);Y.ploty(...);Y.plothold(1);Y.ploty(...)...`
  * added `smartTranspose` option to `Y.plotxy()` and `Y.ploty()` to make plotting of few-datapoint cases more predictable (x-y plot vs. y-x plot)

2006-08-14
  * added `Y.vScale()` to adjust intensity scaling of a viewer

2006-08-09
  * onBaboon: now `priithon` is `priithon24` - additionally there is `priithonN` which is the ''future'' priithon24 using `numpy`
  * added new `skipCol` argument to `U.readArray` for when each line starts with some word
2006-07-19
  * removed `P` and `S` from being loaded automatically with `from Priithon.all import *` (`P`=`priism`: use `F` and `Mrc` instead -- `S`=`seb`: use `U` instead)
  * added `Y.buttonBox()`, `Y.buttonBoxAdd()`, `Y.buttonBox_setFocus()`, `Y.buttonBoxes` for simple ''buttons only'' user-interfaces
  * `numpy` and `scipy` are ready to be used on all platforms
  * new wiki page (["PriithonGUI"]) showing the simplest case of making a standalone Priithon program



2006-06-06
  * changed drag-and-drop of python files into shell window (always insert module path as ''first'' into `sys.path` before doing `import`,`importAs` or `execfile` - remove it afterwards
  * fixed `type` bug in F.radialArr for 1D case (type=`na.Float32` gave `na.Float64` result)


2006-05-23
  * added `U.arrF(*args)`, ... functions as shortcut for making small arrays
  * added `type` argument to all function in `F` module (mostly default is `na.Float32`)

2006-05-19
  * now ccg is part of Priithon (`from Priithon import ccg`)
  * added "save screenshot" to viewer pop-up menu
2006-04-14
  * added `U.insert()` - creates a ''new'' array one element larger than an exisiting one
  * added `U.median2d()` and `U.median22d() - calc median or (median,med.dev.) per section
  * added `U.topPercentile2d()` - similar NOTE: topPercentile assumes pixel values are 0..65535 (uses histogram "optimized" for UInt16 !!!)

2006-04-13
  * added `hold` argument to `Y.ploty` and `Y.plotxy`
2006-03-27
  * in viewer window (`splitND.py`) key shortcuts work also with 'ALT-' pressed (used as workaround for Linux/GTK2 where single key shortcuts don't seem to work)
  * added drag'N'drop to file-list-viewer (`Y.listFilesViewer()`) so that filename now can be dragged ''from'' the list into the PyShell window

2006-03-23
  * added `Y.vZoom()` and `Y.vCenter()`  allows adjusting view  of a viewer
  * added `Y.plotFitAny()`, `Y.plotFitPoly()`, `Y.plotFitDecay()`, `Y.plotFitLit()`, `Y.plotFitGaussian1D()` conveniently plots curve fits ''after'' you did a `U.fit...()`
  * new default for `max_iterations=1000` in `U.fit...()` - was infinit, which could cause hanging ''forever''

2006-03-21
  * U.zeroArrCC for cmplex64 arrays
  * new context menu point in histogram for 'user enter: min max [gamma](gamma.md)'
  * U.saveImg8\_seq and U.saveImg\_seq  to same 3+-D data into sequence on many (tiff,bmp,...) files

2006-02-17
  * changed `F.radialArray`, `radialPhiArr` and `maxNormRadialArr` to ''NOT'' require the 'silly' radius arg and the `func` NOT to have the silly [r0](https://code.google.com/p/priithon/source/detail?r=0) arg
2006-02-16
  * `includeAll.py` is now gone  - instead of PYTHON\_STARTUP its all in `PriShell.py`
2005-12-12
  * changed in Pr source tree: makefiles now use CC,CXX,FC - which is GNU(or also others !?) default
> > (also 2.95 is no special default anymore, use "CC=gcc-2.95 CXX=g++-2.95 FC=g77-2.95"
2005-12-07
  * added 'OSX bug workaround' to FILE-menu
  * added `U.primeFactors(max=None, includeRemainder=False)`
2005-11-17
  * plot function now use '-+' as default
  * TODO: check if `U.naSetArrayPrintMode(precision=4, suppress_small=0)` (or suppress..=1) would be a good default for Priithon

2005-11-16
  * viewer:  colmap now a submenu in contex menu
    * new item in submenu "single left click...":  select/view xy-sub-region
    * scroll increment a) used only for first axis b) cycles "in phase" when wrapping at z<0 or z>=nz
2005-11-02
  * (semi)-official live of Priithon outside our lab starts on 11/2/2005
  * PyShell: whole py packaged moved to Priithon/py (was is wx before) for local custom changes
    * new menu items: file menu: open img file, saveSession, ...
    * drag and drop of files/directories into text window now popup menu

  * LICENSE file:  Priithon is BSD style - but it comes with FFTW (GPL)
> > That makes everything really GPL - unless you delete FFTW (and PyX, ...)

  * new PrLin compiled with GTK2 (python2.4, wx2.6) seems very slow !!
  * all files indentation changed from tabs back to 4-spaces