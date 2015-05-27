# Changelog #

### 2012-08-12 ###
  * added `Y.GuiParams` - `_setValueWithoutTriggerOrGUIupdate(n,v)`

### 2012-06-21 ###
  * changed `Y.vLeftViewSubRegion` - removed `color=False` option
  * added `Y.vLeftHorizProfile()`
  * added `Y.vLeftVertProfile()`
  * added `Y.vLeftZProfile()`
  * added `Y._vLeft_removeGfx()`
  * added `Y._vLeft_normalize_v_ids()`
  * added "on left click ..." popup menu to color viewer

### 2012-06-14 ###
  * added `PriConfig.shellCommandTimer`
  * CHANGED `colorAxis=='smart'` to consider ALL axes (also the last 2 ones)
### 2012-05-04 ###
  * changed (fixed) buttonbox center aligment of statictext,ceckbox,..
  * changed (fixed) buttonbox background color

### 2012-04-26 ###
  * added 'options...' to `U.saveImg(...)`

### 2012-01-31 ###
  * `Y.plotFit...()` understands non-int dataset argument to mean an array used for fitting instead datapoints found in plot

### 2012-01-25 ###
  * `guiParams.py::_holdParamEvents` now understands lists of param names
  * added  `guiParams.py::_enableParamGUIs(self, n=None, enable=True)`

### 2011-09-02 ###
  * added `PriConfig.viewerOriginLeftBottomDefault = 1`
  * added to `appendFilename=False)` option to `Y.vTitleSet()`
  * changed frame titles to indicate viewer orientation:
    * `id)` leftBottom;`id]` leftTop;`id>` FFT;`id}` rFFT

  * added `includeId=False` option to `Y.vTitleGet()`
  * fixed `viewerCommon.readGLviewport()` for `clip=True` and `originLeftBottom=0`

### 2011-09-01 ###
  * viewer/viewer2 shows `<filename>` for all data having `meta.filename`
  * removed `originLeftBottom` from `GLViewerCommon.__init__()` -- was unused
  * changed `originLeftBottom` default from `None` to `1` in
`GLViewer2.__init__()` -- `None` is invalid value here

  * added `meta.originLeftBottom` to loaded image file data
  * viewer and viewer2 now show TIFF,PNG,JPG,... correctly oriented !!

### 2011-08-31 ###
  * added "Clear import-completion cache" to `Options` menu

### 2011-08-26 ###
  * shell string popup options for directory, and print if file doesn't exist
  * added to `buttonbox` textcontrol `wx.TE_PASSWORD` support on "" or label trailing with '\\b'
  * added `guiParams::_bboxNewline()`
  * added `textMultiline=False` option to `guiParams::_bboxText()`
  * fixed  `guiParams` to set value even if text fields has (or just got to) length 0
  * added `Y.email()`

### 2011-08-19 ###
  * added TAB completion for `import` statements

### 2011-08-16 ###
  * added `execModule=None` option to `Y.guiParams::_guiBox`

### 2011-08-08 ###
  * added "p" type to `buttonBox` for `wx.Panel`
  * added `guiParams::_bboxPanel()`
  * added `panel=None` option to `Y.view()` and `Y.view2()`

  * `buttonbox`: only call initial `startNewRow()` if not done by user
  * added `panel` option to `Y.plotFigure()`
  * removed scipy `wxplt::plot_frame::__getattr__()` redirection-to-client-HACK
  * removed scipy `wxplt::plot_frame::update()`

### 2011-08-05 ###
  * added `shellDisplayHookStringPopup = True` to `PriConfig.py`
  * added `Y._guiDisplStringChoice()`

### 2011-07-20 ###
  * added option `secMax=100000` to `U.loadImg_iterSec`
  * added `meta` attribte for resulting array of `Y.loadImg_seq()` -- todo: return `mockNDarray`

### 2011-07-12 ###
  * `Y.DropFrame` now accepts `execStr` to be a callable -- todo: should be renamed...

### 2011-07-05 ###
  * added `panel=None` option to `Y.DropFrame`
  * added `_getParamsGUIsTopLevelParents()` to `Y.guiParams()`

### 2011-06-21 ###
  * changed `Y.DropFrame`: added `callAfter=False` option (trying to fix "hanging/busy" mouse pointer on Windows, when execStr takes long time)

### 2011-05-05 ###
  * added context help via `F1` key
  * NOTE: `wxHtml` has problems with `<`(less than) inside `<PRE>` -- so `>` is shown instead -- BAD HACK !!!
### 2011-04-29 ###
  * added `PriConfig.shellEditEmacs`

### 2011-04-19 ###
  * added `external=''` option to `Y.editor`
  * added shell popup for modules and functions
  * added `PriConfig.shellDisplayHookEditPopup=True`

### 2011-02-22 ###
  * changed `Y.guiParams` `_bboxFloat` and `_bboxInt` default argument `sliderWidth=100` (old: `sliderWidth=-1`)
  * refactored `guiParams.py`: standard functionality does not depend on `execModule`; now default '''changed''' for `execModule` to be `__main__` again, like in plain buttonboxes

### 2011-02-21 ###
  * added filename TAB completion to Priithon shell (PyShell,PyCrust)
  * removed `__main__.shell` -- use `sys.app.frame.shell` instead

### 2011-02-08 ###
  * added `remove dataset` sub-menu to plot window context menu

### 2011-02-03 ###
  * added key shortcut for turning "commandwise autosave" on/off

### 2011-01-25 ###
  * changed `guiParams._bboxText()` default to `textWeight=1`

### 2011-01-24 ###
  * added `U.nd__center_of_geometry()`

### 2011-01-10 ###
  * changed viewer shortcut `a` now calls `vAutoSizeFrame()`
    * `p` now to toggles between `phase` and `abs` view for complex data
  * added `Y.vAutoSizeFrame()`
  * added viewer context menu item for `Y.vAutoSizeFrame()`
  * fixed viewer centering for FFT and rFFT views

### 2011-01-05 ###
  * `all.py` now sets matplotlib backend to `wxagg` before `from matplotlib import pyplot as P`

### 2010-12-06 ###
  * added `PriConfig.viewerShowComplexVals = True`
  * added `Show Complex Vals (real,imag)` to `Options` menu

### 2010-11-29 ###
  * added `readerSDT` for reading Becker & Hickl SDT files

### 2010-11-18 ###
  * added `close all viewers` to `Priithon` menu
  * added `Y.vGammaGUI(vid=-1, gamma=.3)`
  * added `C` (capital) shortcut for gammaGUI in (single color) viewer
  * changed `guiParams` to ignore exceptions when converting string to value
  * renamed `PriConfig.displayHookNdarrayPopup` to `PriConfig.shellDisplayHookNdarrayPopup`
  * added `PriConfig.shellDefaultActionOnArray`
  * renamed arguments of `Y.vd()`, `Y.vTransferFct()`, `Y.vClose()` `id` to `vid`
  * added `verbose=True` option to `Y.saveSession()`
  * added `autosave()` to `py/shell.py`
  * added `PriConfig.autoSaveEveryCommand = True`
  * added `Auto Save every command` to `Options` menu

### 2010-11-12 ###
  * fixed `Y.sleep()` for fractional secs

### 2010-11-08 ###
  * added `_swig_Priithon_minimum_sample` folder to `Priithon_25_xxx` distribution, to demo "game of life"

### 2010-11-05 ###
  * renamed SWIG include file `threadNoThread.i` to `threadNoThreads.i` - and some cleanup

### 2010-10-27 ###
  * added `PriConfig::displayHookNdarrayPopup = True`
  * added `Options`->`Display ndArray popup` menu
  * cleaned up more relative imports and changed `from Priithon ...` to `from ..`

### 2010-10-26 ###
  * changed `PriShell.py` to rely on `startupPriithon.py` for all init calls
  * changed `startupPriithon.py` to call init calls
  * added `Y._fixGuiDisplayHook()` to show popup menu for ndarrays

### 2010-10-12 ###
  * `Y.guiParams()._guiBox(...)` sets `weakref` `buttonBoxes[-1].gp`

### 2010-10-05 ###
  * added `guiParams._doOnPreAnyParamChanged` and `guiParams._doOnPostAnyParamChanged`
  * added optional argument `Y._callAllEventHandlers(..., neverRaise=False )`
  * added `Y.vSyncViewersGui()`
  * added `Priithon menu` item for `sync viewers`

### 2010-10-04 ###
  * changed default behavior for pixel interpolation when zooming _out_ back to _nearest neighbor_
  * added optional argument to `vClearClosedViewers(verbose=True)`

### 2010-10-01 ###
  * fixed unicode problems in `Y.listFilesViewer` (by adding explicite `decode('u8')` and `encode('u8')`)
  * added `ndarray_meta.py` -- `imgArr.meta`
  * added `s` key shortcut to open "enter histogram scale" dialog
  * fixed histogram to accept "leftBrace == rightBrace"
  * added `PriConfig.viewerInterpolationMinifyDefault = 1` # for zoom<1, use linear if 1, use nearest is 0
    * changed default behavior for pixel interpolation when zooming _out_
  * added `PriConfig.viewerInterpolationMagnifyDefault= 0` # for zoom>1, use linear if 1, use nearest is 0

### 2010-09-28 ###
  * renamed `Y.startSocketServer()` to `Y.socketServerStart()`
  * renamed `Y.startSocketServer_demo()` to `Y.socketServer_demo()`
  * renamed `Y.startSocketServer_clearAll()` to `Y.socketServer_clearAll()`
  * fixed `Y.saveSession()` -- don't use `Latin1` encoding
### 2010-09-28 ###
  * added `--no-cleanup-main` as commandline option to `PriShell.py` (i.e. `priithon_shell`, `priithon_shell.bat`)
  * removed `self.print_data.SetPaperId(wx.PAPER_LETTER)` lines from `wxplt.py`

### 2010-09-20 ###
  * added `Ctrl-C` shortcut to viewer, copy to clipboard

### 2010-09-13 ###
  * removed `mmviewer.py::m_sizeChanged` and `viewerCommon.py::m_sizeChanged` - where never used.
  * added `viewerCommon::flipY()`
  * added `Y._callAllEventHandlers()`
  * added `viewerCommon::doOnPanZoom`


### 2010-09-07 ###
  * fixed `Y.viewInViewer()` and `Y.viewInViewer2()` to auto-set title when `a` is a file

### 2010-08-11 ###
  * fixed `guiParams._guiBox` to clear removed GUIs without relying on delay
  * renamed `Y._registerEventHandler()` to `Y.registerEventHandler()`

### 2010-08-06 ###
  * added to `Y.buttonBox` and `guiParams._guiBox` the option `ret=False`
  * renamed `Y.vHistSettings()` to `Y.vHistSettingsCopy`
  * added `guiParams._clearDeletedGuis()`
  * fixed `guiParams._guiBox` to install `doOnClose` handler to remove deleted GUIs (with a 50ms delay after close)

### 2010-08-04 ###
  * added `Y.inspectWX()` -- ref http://wiki.wxpython.org/Widget%20Inspection%20Tool

### 2010-08-03 ###
  * added `plot as z-slider` function to plot figure pop up menu
  * added support for arrow keys to inspect data GUI
  * added buttonbox radiobutton support
  * renamed `guiParams._bboxItemsGroup()` to  `guiParams._bbox_genericTextAndSlider()`
  * added `guiParams._bboxChoice()`

### 2010-07-29 ###
  * added `U.project_lowmem(a, mode='max', astype=None)`

### 2010-07-27 ###
  * added `U.asUInt16(a, round=False, setMinTo0=False, rescaleToMax=False)`

### 2010-07-22 ###
  * changed `Y.cms()` to `Y.cm_calcSmoothCM()`
  * added `Y.cm_calcDiscreteCM()`
  * added `Y.cm_readColor()`
    * added col\_names from http://simple.wikipedia.org/wiki/List_of_colors

### 2010-07-20 ###
  * added `F.magicArr(n)` and `F.magicArr_check(arr)` -- adapted from _Alec Mihailovs_: http://mihailovs.com/Alec  http://mihailovs.com/Alec/Python/magic_square.html

### 2010-07-16 ###
  * added `Y.plotsave_csv_singleXcolumn()`
  * added `save` and `copy to clipboard` singleXcolumn menu entries to plot figure file menu
  * added `Change Format` menu item to plot figure axis popup-menu

### 2010-07-08 ###
  * fixed `readerHIS.py::openHIS()`, can now handle HIS files with "extraneousness" trailing bytes

### 2010-07-06 ###

  * fixed `U.nd__sum()` returned shape for `len(index)==0` case
  * fixed "save as seen" viewer menu command (now: `flipY=True`, `clip=True`)
  * added `U.geoGetPointsOfCenteredBox(cyx, sy, sx=None, clockwise=False)`

### 2010-06-29 ###
  * added `Y.vClearClosedViewers()`
  * added Priithon menu item `clear unused hight viewers IDs`
  * cleaned up code splitND vs splitND2 vs splitNDcommon
  * added autohist functionality to multi-color viewer's popup menu
  * added `ctrl-arrow-key shifts by ...` menu to viewer's popup menu

### 2010-06-24 ###
  * changed `U.deco_memoized` to be a function !
  * added option to `U.deco_memoized(cacheSize=None)`

### 2010-06-02 ###
  * renamed `Y.plotSetColorsDefault()` to `Y.plotColorsDefault()`

### 2010-06-02 ###
  * added `sortCaseSensitive=False` argument to `getAutoCompleteList()` and `getAttributeNames()` in `introspect.py`
  * added `Sort Case Sensitive` option to `Options->Auto Completion` menu --- NOTE: auto-completion appears broken, when typing "lower case" attribute (at least on GTK)

  * added `Y.vPlotInspectDatapointsGUI()`
  * added `inspect plot data points` to `Priithon` menu
  * added `inspect data points` to plot figure context menu

### 2010-05-28 ###
  * `U.fitAny()` and other `U.fit...()` now support "weighted" least square (Levenberg-Marquardt) fitting

### 2010-05-20 ###
  * added "copy CSV to clipboard" function to plot "file menu"
  * hacked `wxversion.py` - to essentially ignore it's original purpose, but making work

### 2010-05-11 ###
  * fixed typo in `Y.vgAddCircles()` - radius was ignored for y,x,r tuples

### 2010-05-10 ###
  * remove old non-working `Y.vtk...` stuff...
  * cleanup `viewer.py` colmap code
    * removed `viewer.cm_size` variable (use a function default of 256)
    * moved all `cm...()` methods to `viewerCommon.py::cm_...()` functions
    * `colnames` and name lists (like `spectrum3`) moved `viewerCommon.py::cms_...()`

  * added `ColMap` entry to `viewer2.m_imgList` (as 13th entry per item)
  * changed `Y.vColMap(id=...)` to `Y.vColMap(vid=...)`
    * vid can now be a scalar [(grey) viewers](for.md) or a tuple(vid, channel) [color-viewers](for.md)
  * added `Y.vColMap2(vid=-1, channel=0, colmap="", reverse=0, rgb=(1,1,1))`
  * added all functions and colorname-list related to colormaps from viewerCommon into `Y` module
    * `cm_HSV2RGB()`, `cm_blackbody()`, `cm_col()`, `cm_gray()`, `cm_grayMinMax()`, `cm_grey()`, `cm_log()`, `cm_wheel()`, `cms()`,
    * `cms_blackbody`, `cms_colnames`, `cms_colnames_255`, `cms_greenred`, `cms_grey`, `cms_redgreen`, `cms_spectrum`, `cms_spectrum2`, `cms_spectrum3`, `cms_spectrum4`, `cms_twocolorarray`

### 2010-05-06 ###
  * added to `PriShell.py::main` `cleanup_main=True` option

### 2010-05-05 ###
  * fixed `Y.vgNameRemove()` (`viewerCommon.py::newGLListRemoveByName()`) to remove named gfx index names if they get invalid
  * added "email bug report" button to GUI exception window

### 2010-04-21 ###
  * collected all help-strings into `PriDocs.py` module
  * `setupy.py` is working

### 2010-04-19 ###
  * added `win32com` support to PyShell's autocompletion support (using `_prop_map_get_`)

### 2010-04-15 ###
  * fixed Priithon Shell's "notebook mode" to allow cut and paste

### 2010-04-09 ###
  * added `Y.showHtmlInfo()`
  * added `guiInfoFrame.py`
  * added new help menu entries
  * changed `U.loadImageFromURL()` to not create a temp-file anymore


### 2010-03-26 ###
  * changed `Y.buttonBox()` to ignore a trailing "\n" in `itemList`
  * added `guiParams._guiBox(...)` as shortcut for `Y.buttonBox(..., execModule=guiParams)`
  * added `refitFrame=True` option to `Y.buttonBoxAdd(...)`
  * added `size=wx.DefaultSize` option to `Y.buttonBox()` -- (`style` option moved to remain  last argument !!)

  * fixed `save CSV` function in `plt` to not write line-trailing column-separator

### 2010-03-25 ###
  * fixed `originLeftBottom == False` orientation for "line graphics"
  * fixed `originLeftBottom == False` orientation for multi-color viewer
  * renamed to `viewer2.py::GLViewer2`
  * fixed 10-grid display for 256x256 sized images (wrong rounding error in `N.arange(0,nx,spacing)`)

### 2010-03-19 ###
  * added `U.reload( *modules )`

### 2010-03-11 ###
  * changed drop-popup-menu to to do "prepend to sys.path" (instead of append)

### 2010-03-04 ###
  * now `priithon -xc "cmdLine1<newline>cmdLine2" ...` can be used from the OS-command-line to have commands executed at startup

### 2010-03-01 ###
  * added `Y.shellExec(command, addHistory=True, useLocals=True)`
  * added `Y.plotSetXAxisFormat(format="%s", figureNo=None)` and Y.plotSetYAxisFormat`


### 2010-02-24 ###
  * added `Ctrl-W` shortcut to close plot window
  * added `_openHIS_fastMap(m)`: `U.loadHIS()` tries now to memmap the whole file, if only the first section contains a variable length comment (NOTE: `arr.HIS.hdr[0]` will be corrupt, use `arr.HIS.hdr0` instead !)
  * added `Y._guiExcept(exctype, value, tb)`
  * added a `CallAfter(Raise)` to `guiExceptionFrame` - to ensure exception frames not being hidden (by accident)
  * changed `startSocketServer(..linewise=True..)` to use gui-exceptions by default

### 2010-02-19 ###
  * added `U.flatten(x, mode='listsOnly')`
  * added `U.hexdump(s, numsPerLine=16, ret=False)`
  * fixed `Y.saveSession()` to handle unicode text correctly
  * added `U.zip_extractall(fn, outDir="", percent=0, verbose=False)`
  * added `U.zip_zipDir(fn, dir)`

### 2010-02-15 ###
  * Priithon's shell magic now understands "`>>> <SPACE> cd directory`" to _really_ change the current directory (not just in a (later disappearing) sub-process)

### 2010-02-05 ###
  * added `__getitem__` and `__setitem__` to `GuiParams`

### 2010-01-21 ###
  * Priithon major refortoring: now using relative import syntax and `from __future__ import absolute_import`
  * added `Y.test6()` showing nice zernike polynomials

### 2010-01-21 ###
  * added `U.exe()`
  * now Priithon shell supports some **magic**: lines starting with `<SPACE>` are executed as shell commands (sent to `U.exe()`) (if line end with `#` or `;` output is suppressed)

### 2010-01-19 ###
  * added `Y.plotsave_csv(fn=None, sep="\t", transpose=True, figureNo=None)`

### 2010-01-15 ###
  * added `Y.vRaise()`
  * added `Y.vSyncViewers()` and `Y.vSyncViewersReset()`

### 2010-01-12 ###
  * added file `wxAsyncDispatcher.py` - inspired [AsynchronousSockets page on wxPython wiki](http://wiki.wxpython.org/AsynchronousSockets) by Josiah Carlson
    * added `Y.startSocketServer()`
    * added `Y.startSocketServer_clearAll()`
    * added `Y.startSocketServer_demo()`

### 2010-01-08 ###
  * added useful decorators to `U` module -- from [the python.org decorator library](http://wiki.python.org/moin/PythonDecoratorLibrary)
    * deco\_simple\_decorator
    * deco\_memoized
    * deco\_addInstanceMethodTo

### 2010-01-06 ###
  * added `_bboxButton()` to `Y.guiParams`
  * added `Text Editor` menu item to `file menu`
  * added `Inspect` menu item to `file menu`
  * changed "V" (capital) shortcut in viewers to do "mean" (not "sum") projection

### 2009-12-07 ###
  * fixed warning in `plt/interface.py` - renamed variable `as` to `ashape`
  * added  `load text table` to drop-file pop-up menu

### 2009-11-25 ###
  * `Y.vShowPixelGrid()` now supports fractional spacing and alpha colors

### 2009-11-19 ###
  * added `U.diffAngle(a1,a0, abs=False, useDegree = True)`
  * added `U.normAngle(angle, abs=False, useDegree = True)`
  * added right-click to refresh function to `Y.vgNameEnablerGUIbox`
  * added `Minimize all Windows` menu entry to Priithon menu

### 2009-11-18 ###
  * added `U.hasDuplicates(s)`
  * added `U.unique(s)` (from activestate recipes [52560](http://code.activestate.com/recipes/52560/))

### 2009-11-13 ###
  * changed the help->about window

### 2009-11-12 ###
  * added viewer key shortcut `1` to set zoom to unity
  * added `parent=None` option to `Y.plotFigure()`

### 2009-11-10 ###
  * added `Priithon` menu with some helpful functions
  * moved `animation control` and `plot z-slider` to `Priithon` menu
  * added `raise all`, `mark all` and two demo/test function to `Priithon` menu

### 2009-11-06 ###
  * changed panning behavior when using `Ctrl+arrow keys`, w/ or w/o `Shift`
  * added `PriConfig.viewerArrowKeysShiftBy` config option

### 2009-11-03 ###
  * refoctoring: moved `putZSlidersIntoTopBox` to `splitNDcommon.py`
  * right click on viewer's pixel info opens control box for `Y.vSetCoordsDisplayFormat`
  * added more options to `U.email()` - e.g. now it supports using GMail's SMTP
  * added those email SMTP related options to `PriConfig.py`

### 2009-10-30 ###
  * added itertools function from Python 2.6 as
    * `U.iterPermutations(iterable, r=None)`
    * `U.iterProduct(*iterables[, repeat])`

### 2009-10-29 ###
  * `Y.vFollowMouse()` now calls other viewers default handler `splitND_onMouse` or `splitND2_onMouse` i.e. shows pixel coords and value

### 2009-10-23 ###
  * added to `Y.vLeftClickDoes` option `onlyOnClick=True` - to support functions calls on moving mouse while left-down
    * fixed `Y.vLeftClickNone()` accordingly (i.e. clear `doOnMouse`)
  * renamed `Y.test()` to `Y.test1()`

### 2009-10-22 ###
  * `Y.editor()` now accepts `functions` as arguments, opening the corresponding module file at the proper line

### 2009-10-06 ###
  * added "V" (capital) shortcut in viewers to get "sum"-projections over first axis

### 2009-10-05 ###
  * added to `U.timeIt()` `useTime=False` option (to support wall-time mode on Linux)

### 2009-10-02 ###
  * added `F.mandelbrotArr(ny=512, nx=512, itermax=30, ymin=-1.25, ymax=1.25, xmin=-2, xmax=.6)` (thanks to [Dan Goodman](http://thesamovar.wordpress.com/2009/03/22/fast-fractals-with-python-and-numpy))
  * added `Y.test5()`

### 2009-09-30 ###
  * changed `Y.vgAddLines`: added `segcols=None, segcolflat=True` option to allow for segment-wise coloring

### 2009-09-29 ###
  * `Y.vFollowMouse`: `xyViewers` is list of `vid`s where `vid` can now be either a scalar or a tuple `(vid, (scaleY,scaleX))`

### 2009-08-31 ###
  * added "change axis bounds" to plot figure axis right-click popup menu

### 2009-08-28 ###
  * added read support for Princeton Instruments CCD image format (.SPE)
    * `U.loadSPE(fn)`

### 2009-08-24 ###
  * added plot right-click popup menu item for changing background color

### 2009-08-11 ###
  * added support for `Ctrl-C` KeyboardInterrupt (to be pressed in the terminal window)
    * added "(pid: 12345)" text to PyShell window title
    * now when Priithon starts it also prints that info (process id) to the corresponding terminal window
  * added `skipNlines=0` option to `Y.clipboardGetText2array` and `U.text2array`
  * added `sympy` Package (version 0.6.5)

### 2009-08-07 ###

  * changed `Y.plotSetColorsDefault()` (if called with non-True argument) to return current color sequence string
    * reminder note: if `c`-option in `Y.ploty()` / `Y.plotxy()` starts with a digit, it is used to reset index in color sequence (valid values are 0..9)
  * added `Y.plotDatasetRemove(dataset=-1, figureNo=None, refreshNow=True)`

### 2009-08-06 ###
  * added `Y.test2()`
  * added `Y.test3()`
  * moved `F.mockNDarray` into separate file `mockNDarray.py`

### 2009-07-28 ###
  * added `Y.vPlotAsSliderGUI(vid=-1, figNo=-1, zaxis=0, activate=True)`
  * new PyShell file menu entries for:
    * "Open viewer animation control -- Y.vAnimate()"
    * "Open GUI to make a plot figure function as z slider for a viewer -- .vPlotAsSliderGUI()"


### 2009-07-14 ###
  * fixed "some" of `U.topPercentile()` --
    * also added `throw` to `seb1.cpp::toppercentile` -- recompiling required
  * in SWIG makefile(s): `PYPATH_DIR` now defaults always to "."

### 2009-07-02 ###
  * `added U.email()`
  * added `format` option to `U.saveImg()` and `U.saveImge8()` (useful if `fn` is really a stream instead of a filename)

### 2009-06-25 ###
  * added `hold` to plot right-click popup menu
  * added `topdown=True` argument to `Y.iterChildrenTree()`

### 2009-06-24 ###
  * changed `Y.buttonBox` arguments:
    * old: `buttonBox(itemList=[], title="button box", parent=None,pos=wx.DefaultPosition,  style=wx.DEFAULT_FRAME_STYLE,  layout="boxHoriz",  execModule=None)`
    * new: `buttonBox(itemList=[], title="button box", execModule=None, layout="boxHoriz", panel=None, parent=None, pos=wx.DefaultPosition, style=wx.DEFAULT_FRAME_STYLE)`
  * similar changes to `_buttonBox.__init__()`
  * added `panel` argument to `Y.buttonBox` to support putting buttonBox inside other wxWindows, not creating a new frame
    * in case `panel` is not a top-level frame, `doOnClose` event handler will get closed with wx's `wx.EVT_WINDOW_DESTROY` and will NOT `Close()` all children -- otherwise (if panel is top-level) children will get `Close()`ed before `panel` will get `Destroy()`ed

### 2009-06-22 ###
  * added `iniFcn` option (optional 5th item-tuple entry) to `Y.buttonBox`

### 2009-06-19 ###
  * `Y.viewInViewer` and `Y.viewInViewer2` now interpret a string argument both as frame title and to be evaluated to get the image data

### 2009-06-18 ###
  * `Y._registerEventHandler` now accepts strings as `newFcn` -- they are executed in `__main__` with `args` containing the handler function arguments

### 2009-06-12 ###
  * package `numexpr` now in Priithon
  * removed Priithon's (workaround-cut-down) `pylab` module -- `P` is now `matplotlib.pyplot` - `P.ion()` is called with `from Priithon.all import *`

### 2009-06-11 ###
  * added `Y.iterChildrenTree(parent, includeParent=True)`
  * viewer stop using `SetAcceleratorTable` -- no accel table/ acceleratortable anymore -- because of persisting problems with wx > 2.5 - especially on GTK
  * added `splitNDcommon::keyShortcutTable` -- internally uses`OnKeyDown` for viewer/split
  * changed `Y.vShortcutAdd` option `flags` to `mod`
  * added viewer/viewer2 shortcut: `Ctrl-Shift-Left/Right/Up/Down` pan image by one pixel

### 2009-06-09 ###
  * added 'zoom history'-function to plot right-click-popup menu

### 2009-05-18 ###
  * added `U.myStr(a)`: (like str()  but calls str() (instead of repr(), recursively for lists and tuples)

### 2009-05-08 ###
  * changed `priithon_script` scripts to use "=" instead of "==" (for strict POSIX complaiance; Ubuntu uses "dash" rather then "bash" for "sh")

### 2009-05-05 ###
  * changed `viewerCommon::newGLListRemoveByName` to check for and remove trailing `None`s in `m_moreGlLists` and `m_moreGlLists_enabled`

### 2009-05-04 ###
  * fixed typo in `Mrc.initHdrArrayFrom()`
  * fixed `guiParams::set_attr()` for iterable value types (use `all()` to test if value has really changed)

### 2009-04-02 ###
  * changed `Mrc` header format: instead of 30-bytes called `blank`, we have now `nblank`(int16), `ntst`(int32) and `extra`(24xuint8)`(unsigned!)

### 2009-03-31 ###
  * added menu command to plot windows to save data into a CSV-file (x,y on separate lines for each dataset)

### 2009-03-27 ###
  * added `PriConfig.raiseEventHandlerExceptions=False` -- if `False`, `traceback.print_exc()`, otherwise `raise` is used on exceptions


### 2009-03-25 ###

  * `U.loadTxt()` now also supports `.bz2` (besides `.gz`)

### 2009-03-23 ###
  * added `edit text file` to drop-file popup menu also for non-Python (i.e. non `.PY`,`.PYW` or `.PYC`) files


### 2009-03-19 ###
  * added `fixed_mask=None` option to all (non linear) fitting routines in `U` module: `fitAny()`,`fitDecay()`, `fitGaussian()`, `fitPoly()` (-- so no change for `U.fitLine()`)
  * addded `**leastsq_kwargs` to those functions as well

  * refactored `U.yPoly` to manually (inside for loop) built up powers of `t` rather than calling `N.power`
  * change in `filePopDrop.py` (`onImport`, `onExe`, `onImportAs`) to call `sys.path.remove(p)` instead of `del sys.path[0]` (-- in case script has inserted something else at start of `sys.path`)

### 2009-03-16 ###
  * changed `U.loadHIS()` to support both memmap and fromfile (useful for big files on 32bit OSs):
    * `U.loadHIS(fn, secStart=0, secEnd=None, stride=1, mode='r')`

  * changed handling of _priithon resource file_:
    * `PRIITHONRC` env var should now point to the rc-file, not to it's directory
    * in addition to `.priithonrc.py` also `_priithonrc.py` is checked
    * search order remains: current dir, then env var, then hom dir
      * now: if env var is set, the referred filename should exist, no extra exists-test done anymore


### 2009-03-12 ###
  * `guiParams`: text fields and sliders are now responsive to `up`/`down`-arrow keys. Hold down shift to "scroll" 10x faster. Hold down Ctrl key to prevent event handlers from getting called
  * changed `guiParams` so that event handlers will not get called when `new value` == `old value`
  * added `guiParams::_holdParamEvents(self, n=None, hold=True)`

### 2009-03-05 ###
  * fixed `F.mockNDarray` to handle `N.newaxis` (i.e. `None`) as index; such as `a``[``None``]` and `a``[``:,None``]`
  * changed order of arguments in `U.saveTxt`: now `U.saveTxt(arrND, fname,...)`
  * added `U.saveTiffMultipageFromSeq()` to save into multipage tiff from an iterator

### 2009-03-04 ###
  * fixed `Y.vgNameBlacklist()` to silently ignore if the given `name` not used, therefore not being blacklisted
  * added `Y.vSetCoordsDisplayFormat` -- set "float" vs "int" coord display on a viewer by viewer bases
    * added `splitNDcommon::showFloatCoordsWhenZoomingIn`
  * fixed `F.mockNDarray` to handle list of lists; `None`s are interpreted as 0-dim-mockarray


### 2009-03-02 ###
  * `guiParams`: changed empty labels to be skipped: no creation of a static text control
  * added `guiParams::_bboxText(...)`

### 2009-02-26 ###
  * added`textWidth=-1` option to `guiParams::_bboxInt`,`guiParams::_bboxFloat`and `guiParams::_bboxItemsGroup`
  * changed `buttonbox::onClose` behavior to _explicitly_ call `OnClose(True)` on the children (ref. http://aspn.activestate.com/ASPN/Mail/Message/wxPython-users/2020248 and the other reply by Robin Dunn)
  * removed `OnClose` from `histogram.py` ((was never called: print "OnClose"))

### 2009-02-24 ###
  * added tooltip option to `buttonbox` -- in `Y.buttonbox(itemList)` the tooltip can be given as 5th element of the item-tuple
  * added `tooltip` option to all `guiParams` types
  * reimplemented `Y.glCirlce` and `Y.glEllipse` (mostly) in C++


### 2009-02-13 ###
  * `U.histogram...()` and `Y.plotHistogram()`: added `cumsum=False` option for calculation of cumulative histograms
  * 

### 2009-01-20 ###
  * changed argument name in `Y.vgNameRemove`: `ignoreKeyError` to `ignoreError`

### 2009-01-14 ###
  * extended buttonbox and guiParams

### 2009-01-13 ###
  * fixed `splitNDcommon::doOnSecChanged` to set `v.img` BEFORE event handlers get called
### 2009-01-09 ###

  * changed `Y.vSetSlider`: renamed first arg from `id` to `v_id` (can be either an int or a splitND object now
    * removed `autoscale` argument because it was not implemented

  * added `U.text2array(txt, transpose=False, comment='#', sep=None, convFcn = None, convertDecimalKomma=False)`
  * added `Y.clipboardGetText2array(...)`


### 2009-01-08 ###
  * buttonbox now support `cmd` to be a function object or a list of callables
    * each "button" (meaning: any by buttonbox supported wx control) maintains a list of event handlers: `buttonbox.doOnEvt[i]`; `i` beeing the index of the respective "button"/control
    * the "old-style" string-cmd (or if cmd is a callable) is the first entry in that list

### 2009-01-07 ###
  * changed `viewerCommon::newGLListRemove` to actually remove trailing idxs rather than producing (a bunch of) trailings `None`s; i.e. only "middle" idxs are kept (and set to None) to not mess up (all gettings decremented by one) higher idxs

### 2008-12-18 ###
  * change docstrings to use tripple double quotes, following PEP Python coding style
    * tripple single quotes shall be used for commenting out code, and for "non human readable" code
  * added `exclude_amax` option to `U.histogram()`,`U.histogramYX()`,`U.histogramXY()` functions

  * added `Y.plotHistogram()`
  * added new menu item to popup menu in plot window


### 2008-12-05 ###
  * changed behavior of `viewerCommon::newGLListDone` -- ignores "enable" argument if idx is beeing reused; so disabled gfx will stay off, even when the gfx changes
    * consequently all for `Y.vgAdd...` functions the gfx stays off if the idx is reused

### 2008-12-01 ###

  * added `Y.vgNameBlacklist()` (name-blacklists cause skipping of vgNameEnable, esp. when called via auto on/off on sect-change)
  * changed arguments: `Y.vgNameEnable(id=-1, name='', on=True, skipBlacklisted=False, refreshNow=True)` (default behavior does not change)
  * change in `Y.vFollowMouse`: gfx idx to "vFollowMouse" (was: "vFollowMouse\_Idx"); removed use of gfx name (was: "vFollowMouse")

### 2008-11-25 ###
  * added `Y.guiParams` and `guiParams.py` -- work in progess, needs clean-up (e.g. text fields, support for custom tool-tips) and (better) integration with buttonbox
  * added `doOnClose` parameter to buttonBox, (event handler list for frame close event)

### 2008-11-25 ###
  * added `U.rms(a)` -- http://en.wikipedia.org/wiki/Root_mean_square
  * fixed `Y.plot` functions - removed flickering on Windows, by implementing double-buffering (`wxBufferedPaintDC`, `plt/wxplt.py`)
  * added `Y.vAnimate()` - a GUI buttonbox to support auto-animated z-Slidering

### 2008-11-24 ###
  * fixed saveSession - removed ugly newlines "\r\n" ("<sup>M</sup>M" in emacs)
  * extended `Y.viewerInViewer()`, `Y.viewerInViewer2()` to autoconvert tuple of arrays to `mockNDarray`
  * renamed `sifreader.py` to `readerSIF.py`
  * added support for Hamamatsu Image Sequence (HIS) file format (`readerhis.py`); `U.loadHIS()`; `U.load` recognizes ".his" file extension

### 2008-11-20 ###
  * added `Y._glutInit(argv=[])` (its a noop for non-first calls)
  * added call to `Y._glutInit(sys.argv)` in PriShell.py

### 2008-11-18 ###
  * added `U.smooth1d` -- copy and paste from http://www.scipy.org/Cookbook/SignalSmooth
  * changed default for `Y._registerEventHandler` -- default "replace" rather than append: `oldFcnName=''` short for oldFcnName==newFcnName
  * changed also behavior of `Y.vLeftClickDoes` to replace rather than append handlers

### 2008-11-13 ###
  * changed `F.shift`:
    * use Priithon's `F.rfft` instead of numpy's rfft , and dito for irfft
    * removed `dtype` option (left as FIXME TODO, to put it back)
    * `delta` argument: scalars are "auto expanded" to tuple of same values
    * `F.shift`  IS STILL BROKEN -- e.g. shifting one center object by 1 pixel, duplicates the object

  * added
    * `U.nd__sum()`
    * `U.nd__maximum_position(()`
    * `U.nd__minimum_position()`

### 2008-10-24 ###

  * refactoring `usefulP.py` by separating out common code lines into `_getFig(figureNo)`

### 2008-10-23 ###
  * added `PriConfig.py`: this modules defines some default parameters used in Priithon. This module is imported into the shell as `_priConfig`. So far parameters are:
    * `autoSaveSessionDir`
    * `autoSaveSessionFn`
    * `autoSaveSessionCommands`
    * `saveSessionDefaultPrefix`
    * `viewerShowFloatCoordsWhenZoomingIn`
    * `defaultGfxColor`
    * `viewerBkgColor`
    * `viewer2maxNumColors`
  * added autoSaveSession command to file menu - shortcut Ctrl-S (or Cmd-S on Macs)
    * added `autosave=False` option to `Y.saveSession`
    * added `Y._setAutosavePath()`
  * added `enumLabel=None` argument to `Y.vgAddTexts`: if enumLabel is a number, labels will be auto-generated by counting; starting at `enumLabel`, `enumLabel+1`, `enumLabel+2`,...
  * changed `Y.vgRemove` -- added `ignoreError=True`: invalid `idx` will be silently ignored
  * added `Y.vgIdxAddName` and `Y.vgIdxRemoveName` to add/remove names to an existing line-gfx

### 2008-10-07 ###
  * new class `F.mockNDarray`: a list of ndarrays "pretending" to be one higher dimensional array
  * changed `Y.view` and `Y.view2` for `type(img)` being a sequence
    * `Y.view & Y.view2 (imgList)` open separate viewers one for each item
    * `Y.view & Y.view2 (imgTuple)` creates a mockNDarray to open one viewer for "higher dimensional" array
      * for both **list** and **tuple** arguments string-items are interpreted as filenames (implicit call to `Y.load`)

  * unified file drag-and-drop: now pyShell, view and view2 now all behave the same and show a choice of what to do

### 2008-10-02 ###
  * added "debug" button to gui exception frame
  * added `U._getSourceCodeLine(depth=0)`
  * added `U._getSourceCodeFilename(numPathTails=None, depth=0)`
  * added `U._getSourceCodeLocation(numPathTails=None, depth=0)`
  * added `U._getSourceCodeFuncName(depth=0)`
  * added `U._raiseRuntimeError(msg, appendSourceCodeLocation=True, numPathTails=None)`
  * added global flag to `py/shell.py`: `NO_SPECIAL_GUI_EXCEPT=True` -- this "turns off" all special exception handling parts of `py/shell.py`; no wxMessageBox - instead rely on (now standard) guiException
  * added global variable to `splitND2.py`: `maxNumColors=8` -- can be changed dynamically really needed


### 2008-09-09 ###
  * added `Y.vInterpolationSet(v_ids=[-1], magnify=0, minify=0)`

### 2008-09-08 ###
  * added `retImg=False` option to `U.calc_threshold_basic()`
  * fixed / unified all `U.calc_threshold_...()` functions to use "threshold strictly(!) above" convention: `1 if arr > T else 0`

  * added TAB-completion for function/method arguments -- first attempt; so far this only works if argument is _not_ already partially typed

### 2008-09-05 ###
  * added `F.calcHistEqualizedF(arr, histYX=None)`
  * changed meaning of `nBins=None` default for `U.histogram...` functions and `U.generalhistogram`: if nBins is None: `nBins=int(amax-amin+1)` _unless(!)_ for float dtypes: nBins is forced to be >= 100

### 2008-09-03 ###
  * added test for `N.int0` type in `viewer.py`  [`(ao*255-b).dtype.type == N.int32 --> False` (ao.dtype==bool & b.dtype == unit8)]
  * changed argument in `Y.bottonBox()` !!  old: "vertialLayout=False" is now: `layout="boxHoriz"` -- other options are "boxVert"("v") or 2-tuple / 4-tuple for FlexGridSizer
  * fixed `U.calc_threshold_otsu`
  * fixed `U.calc_threshold_otsu2` for two thresholds
  * added `retEM=False, retImg=False` arguments to both functions
  * added `U.calc_threshold_otsu3` for three thresholds - takes 30sec for 220 grey-scales (hist.nBin = 220)

### 2008-09-02 ###

  * added `Y.plotSetColor(color=(255,0,0), dataset=0, plotNofigureNo=None)`
  * added `Y.plotRefresh(figureNo=None)`
  * added `Y.plotGetXminmax(figureNo=None)`
  * added `Y.plotGetYminmax(figureNo=None)`
  * added `Y.plotChangeDatapoints` (not working yet)

### 2008-08-29 ###
  * now we have uncaught exceptions shown in a nice wx windows
    * new module `Priithon.guiExceptionFrame` and
    * new function `Y._fixGuiExceptHook()` called from `PriShell.py`

  * `U.reloadAll()` does not `reload(sys)`, even if sys is imported in main; this is to prevent automatic resetting of `sys.excepthook`

  * fixed `Y.vFollowMouse` to handle y-z-viewers


### 2008-08-28 ###
  * bugfixes in `Mrc.py` - e.g.
    * `raise ValueError, "zAxisOrder z slower than t is not supported my Mrc format"`
  * `U.image2array`: new: if i0 is None, no seek, just read and convert "next section" in image
  * added `U.loadImg_iterSec`: iterator: load img by iterating section-wise
  * changed `viewer.py` & `viewer2.py` back to using the `.375` in `glOrtho (-.375, self.m_w-.375, -.375, self.m_h-.375, 1., -1.)`        ---      otherwise some images were shown with "bottom line shown somewhat at top of image" old: `glOrtho (0, self.m_w, 0, self.m_h, 1., -1.)`


### 2008-08-27 ###
  * **renamed `usefulX2.py` to `usefulX.py`**
    * for the case of no "X"-GUI available there is now `usefulX_noX.py`  -- containing code from old `usefulX.py` file
    * `Priithon/all.py` now contains the `if hasattr(sys, "app")` line to conditionally import `usefulX` or `usefulX_no` as `Y`
    * --> now `Y` always contains all "single leading underscore" names from `usefulX`


  * added `autoscale=True` option to `Y.vReload`
  * added `assign filename to varname` to drag-and-drop menu when  dropping a file

### 2008-08-20 ###
  * added `reportlab` package to Priithon distribution -- http://www.reportlab.org/rl_toolkit.html
  * removed `PyX` -- needs latex for text redering
  * fixed `Y.vgAddBoxes` to go through center of yx points again (also removed a "+1" for top right edge of drawn boxes !?)
  * renamed option `ignoreKeyError` to `ignoreError` in `Y.vgEnable` -- now also about IndexError

### 2008-08-18 ###
  * removed `splitND2::addHistPanel`: was only used once and only contained two lines
  * added `viewer2::getColor(imgidx)`
  * fixed RGBcolors when `Y.viewInViewer2` changes number of colors
  * added `_registerEventHandler` to being visible as `Y._registerEventHandler`

### 2008-08-14 ###
  * fixed true division bug in `Mrc.py::shapeFromHdr()`: `nz = nsecs / nt / nw` -> `nz = nsecs // nt // nw`
### 2008-08-11 ###
  * dded more arguments to `Y.plotFit....()` functions:
> > `figureNo=figureNo, logY=logY, logX=logX, logZeroOffset=logZeroOffset`
### 2008-08-07 ###
  * added new argument `rgbOrder="rgba"` to all `U.saveImg...` functions
    * now even a `(1,ny,nx)` array can be saved in color: either red,green or blue
  * `Y.assignNdArrToVarname` returns now varname as string on success, None otherwise
  * drag-and-drop of "file-to-execute" and "file-to-LoadImgAndAssignToVar" now generate command history entries  ((note: the original "file-to-execute" also sets sys.path and resets it back; the command history entry would not do this))

### 2008-08-06 ###
  * added `self.keepZoomedToBraces` to histogram -- now "zoom-to-braces" is like a ''state'', that is kept until, left or middle mouse dragging deactivates it
  * added `self.keepCentered` to viewerCommon -- now "center" is like a ''state'', that is kept until, left or middle mouse dragging deactivates it
  * added "auto zoom + scale all" to popup-menu in multi-color viewer
  * internal renaming:
    * renamed `histogram.py::fitXcontrast()` to `zoomToBraces`
    * in splitND.py and splitND2.py:
      * `On13` -> `OnAutoHistScale`
      * `On81` -> `OnViewFFT`
      * `On82` -> `OnViewFFTInv`
      * `On83` -> `OnViewCplxAsAbs`
      * `On84` -> `OnViewCplxAsPhase`
      * `On85` -> `OnViewViewFlipXZ`
      * `On86` -> `OnViewViewFlipYZ`
      * `On87` -> `OnViewViewMaxProj`
      * `On90` -> `OnHistLogMode`
      * `On61` -> `OnViewChangeColorMap`
      * `On62` -> `OnViewChangeShowGrid`
      * `On63` -> `OnViewChangeOrigin`
      * `On64` -> `OnViewChangeNoGfx`
      * `On69` -> `OnViewVTK`
    * in viewerCommon.py  (removed from viewer2.py)
      * `On51,52,53,54` -> `OnShiftOffsetLeft`/`Right`/`Up`/`Down`
  * small changes in LICENSE file
  * moved SWIG generated files into new `Priithon_bin/_bin` folder -- `Priithon_bin` is ''parallel'' to the `Priithon`-folder, but/and `Priithon_bin` is added in `PYTHONPATH`
-- now `Priithon` (including all sub-folders!) is  identical between platforms !

### 2008-07-30 ###
  * added `clone=False` option to `Y.shell()` -- this allows to have multiple "view"-windows of the Priithon shell
    * fixed `Priithon/py/shell.py` to set `__main__.shell` only for the first (main) shell; subsequent "additional" shells or shell-views, will not change `__main__.shell`
  * added new "file menu item" to Priithon shell windows: open second view of shell
  * changed behavior of `Y.vgEnable()` -- added `ignoreKeyError=True` option
  * added option `refreshNow=True` to `Y.vgEnable()`
  * fixed `Y.plotClear()` to reset colors

### 2008-07-29 ###
  * changed `Y.vReadRGBviewport` by adding `clip`-option: `vReadRGBviewport(v\_id=-1, clip=False, flipY=True)
  * cleanup of `histogram.py`
    * removed "ev.GetEventType() === wx.EVT\_MOUSEWHEEL:" section in `OnMouse` -- `def OnWheel()` had "always" been called instead (at least on MAC OS-X)

  * fixed hist range for uint8,uint16,int16 in `splitND`,`splitND2::setupHistArr()`
  * fixed histogram "autoFit()" function -- popup menu: "auto zoom + scale"
  * added `fitYtoSeen` flag to histogram  -- default: `True`
    * opup menu: "auto fit y axis to shown values"

### 2008-07-22 ###
  * `Mrc::init_simple` defaults changed to wavelength=0 --- was: 999 (`0` means now "undefined" or "meaningless" -- look at `NumWaves`, to see how many waves there are)
  * `Mrc.save()` can now save 5D data; `zAxisOrder` argument string is now read from start (not from end anymore), so that `zAxisOrder='wtzyx'` is now equivalent to `zAxisOrder='wtz'`
  * changed `arr.Mrc.info()` to show slice order in "python/C style" rather than "Fortran order": `slice order:  0 (0,1,2 = (wtz, tzw or twz)` instead of `slice order:  0 (0,1,2 = (ZTW or WZT or ZWT)`

  * removed `Y.vFollowMouseReset()` -- now use `Y.vFollowMouse(id)` without further arguments
  * `idx` argument in `Y.vg....` functions can now be a string -- on first use this will create a new gllist entry, subsequent uses will ''overwrite'' the gllist entry in-place

### 2008-07-21 ###
  * removed `Y.hist()` and `Y.vview` -- were unused !?
  * for all `Y.vLeft....()` functions set first argument to have default `id=-1`
  * added `Y.vLeftViewSubRegion()`
  * removed unused member in histogram class: `self.mouse_last_wx, self.mouse_last_wy`

### 2008-07-18 ###
  * added `Y.vShowPixelGrid(v_id=-1, spacingY=1, spacingX=1, color=(1,0,0), width=1)`

### 2008-07-16 ###
  * fixed `colorAxis="smart"` option in `Y.viewInViewer2() ; and enforce check for nColors<=8 in same function
  * added `F.rampArr()` -- this is the one used by Y.test()
  * fixed case if `type(img)===str` splitND and splitND2 will now eval str using locals from calling function-frame


### 2008-07-07 ###
  * changed behavior of `viewer::doOnMouse`: now the handler gets ''always'' called by `OnMouse` -- irrespective of mouse cursor being within or outside edges of image (removed variable `xyEffInside`)
  * changed signature of `histogram::doOnMouse(self, xEff, bin)` -- removed `bin` argument
  * changed signature of `viewer::doOnMouse(self, x,y, xyEffVal)` -- removed `xyEffVal` argument

  * `viewer::OnMouse()` and `viewer2::OnMouse()` now moved to `viewerCommon` -- **todo:** fix up `mmviewer`

  * in `viewer.py, viewer2.py,mmviewer.py and histogram.py`: removed `self.dragging`  -- was  not used; only set to 1 but never reset to 0
  * in `viewer.py, viewer2.py and histogram.py`: removed `if ev.Leaving(): return` from `OnMouse` handler
  * in `viewer.py, viewer2.py and histogram.py`: added mouse-capturing for dragging

  * changed `U.reloadAll()`: added `histogram.py` to reloadAll() list

  * changed "some" viewer, histogram handlers to be **lists of handlers** rather than a single handler function
    * renamed `splitNDcommon::doSecChanged`
    * renamed `viewerCommon::doLDClick`
    * renamed `viewerCommon::doLDown`
    * removed `viewerCommon::doOnFrameChange`  -- was used nowhere inside Priithon
> > new:    ( each of these is a lists of functions called with `(x,y)` as argument )
    * `splitNDcommon::doOnSecChanged`
    * `viewerCommon::doOnMouse`
    * `viewerCommon::doOnLDClick`
    * `viewerCommon::doOnLDown`

  * added `_registerEventHandler(handlerList, newFcn=None, newFcnName=None, oldFcnName=None, delAll=False)` to `Y` module, to manage these handler-lists



### 2008-07-01 ###
  * **new coord system**, integer pixel coordinates go through the center of pixel; i.e. pixel `0` goes from `-.5` to `+.5`
    * `Y.vgAdd...` function don't need to each add `+.5` anymore; -- i.e. overall nothing changes when using `Y.vgAdd...` functions !!!
    * ''todo:'' fix fft-mode and rfft-mode

### 2008-06-11 ###
  * added new options in popup-menu when dragging multiple files into Priithon shell: load&assign img.seq. , view img.seq.

### 2008-06-05 ###
  * make file-list-viewer window drop-aware: drop in a dir to start browsing that dir -- fn-pattern is kept ( dropping in a file, will browse it's containing folder)

### 2008-06-02 ###
  * fixed `Y.editor(mod)` in case mod.file points to `.py` file instead of `.pyc` file
  * added "edit py-file" option in pop-menu when drag-and-dropping py-files into Priithon shell

### 2008-06-02 ###
  * changed `Y.shellMenuAppendNewCommand()` to also accept functions as cmd arg "directly" -- no exec "f()" string needed
  * buttonBox: added more "automatic" variables accessible when `cmd` gets exec'ed;
    * before: "`x`"=Value, "`_`"=execModule;
    * newly added: "`_ev`"=wx-event,   "`_b`"=wx-event-object (i.e. the GUI control itself (e.g. the "button")
  * added `viewer2` support for `N.float64,N.int32, N.uint32, N.int64, N.uint64` --> they are (sectionwise) converted to `float32`

### 2008-05-28 ###
  * changed `U.loadImg_seq()`; if `channels` is scalar returned arr.ndims is now 3, not 4
  * added `Y.shellMenuAppendNewCommand()` -- useful for creating (global) key-shortcuts
  * added `ignoreKeyError=True` option to `Y.vgNameRemove()`

### 2008-05-27 ###
  * refactored `Y.listFilesViewer()` to be a "real" class with member functions, instead of functions inside init; now `Y._listFilesViewer_obj.frame` is the wxFrame of the last listFilesViewer opened
  * same to `Y.listArraysViewer()`
  * added `U.pathPrependToFilename(path, prefix)`
  * fixed `Y.listFilesViewer()` to keep file-pattern when switching through directories
  * changed `Y.listFilesViewer()` -- only "double click" changes directories --> **TODO:** pressing 

&lt;Return&gt;

 should also change dir

### 2008-05-21 ###
  * added `Y.vTitleGet()` and `Y.vTitleSet()`, to get/set the title of a viewer window
### 2008-05-14 ###
  * added `U.load()` -- load "any" image; like `Y.load()` but without GUI
  * PIL: added support for TIFF (= Zeiss LSM) format key: ('l', 2, 1, 1, (8, 8, 8, 8), ())
  * `U.image2array()`: added support images (mode: RGBX)

### 2008-04-22 ###
  * fixed many function in usefulP.py to work even if no figure was opened yet -- added `plt.validate_active()`
  * removed the `"---------->"` label in viewer when viewing 2D arrays (in `splitND.py` and `splitND2.py`)

### 2008-04-17 ###
  * changed default value from -1 to None in `Y.vzslider(idxs=None,...)` -- meaning stays the same, i.e. "all current viewers"

### 2008-04-16 ###
  * now SWIG shall be included in Priithon. `Priithon_25_mac/_swig/{bin/,share/,swig}` for now
    * `_swig/swig` is a script that adjusts the include paths -- in the same way priithon\_script does it
    * PriithonSrc/common is then copied to `Priithon_25_mac/_swig/PriithonCommon`
  * TODO: add `water.py::vgAddEdges` to usefulX2 -- it used a new SWIGged function for all the glVertex calls
    * (speed up is about 50x over the prior numpy version)
  * METAINFO: created google groups and googlecode for Priithon:

### 2008-04-15 ###
  * fixed `F.noiseArr()` -- dtype argument was ignored
  * added support for multi-page TIFF
    * `U.saveTiffMultipage(arr, fn, rescaleTo8bit=False, **params)`
    * `U.saveImg()` and `U.saveImg8()` automagically call saveTiffMultipage for higher dimensional arrays
      * both functions have a new argument `forceMultipage=False` to control multiPage vs. RGB mode
  * copied `WbmpImagePlugin.py` from Priithon\_25\_win/PIL to Priithon\_25\_mac/PIL -- check if this is o.k. !
  * copied all other `*.py` files from mac to win PIL folder -- windows had DOS-newline ...

### 2008-04-07 ###
  * added key "accel" (shortcut) for `view` and `view2`: Ctrl-w (cmd-w; i.e. apple-w on macs) to close viewer window
  * fixed to `Y.vHistSettings()` to also work for `viewer` (not only for `viewer2`)
  * fixed viewer:  preserve hist settings when pressing key to get x-z or y-z flips or z-projection (now same feature as was already there for viewer2)
  * added `refreshNow=True` argument to `Y.vgMarkIn3D()`
  * fixed default color for `Y.ploty` called with multi-column array
  * changed PyShell to ''also'' accept Cmd-Key besides of Contrl (mac only -- no change for Unix and PC !)
  * fixed `U.histogram` and relatives to work also with lists (implicit `N.asarray()`)
  * added doc line for Y.glutText: ``[GLUT stroke font size of 1 is 100 "pixels" high for the letter `A`]``


### 2008-04-04 ###
  * fixed `Mrc.data_withMrc(self, fn)` -- removed `fn` argument, wasn't used
  * added support for Andor SIF files. `U.loadSIF()` is imported from `sifreader.py` -- it uses memmaping

  * fixed viewer2: x-z and y-z flips now preserve hist settings -- just like z-projection already did

### 2008-04-03 ###
  * added `U.grep(pattern, *files, retList=False)`
  * fixed `Y.editor()` to accept modules instead of filenames

### 2008-04-02 ###
  * fixed `U._saveSeq_getFixedFN(fn, n)` -- for 10 files the largest number will be 9, so only one digit is needed, not two

### 2008-04-01 ###
  * Windows batch script fixed -- now windows version can be installed anywhere (`C:/Priithon_win_25` is no longer hard coded)

### 2008-03-25 ###
  * `U.saveImg()` (and similar functions) save "RG" (i.e. blue set to 0) in case of 2 color channels


### 2008-03-03 ###
  * added `figureNo` option to most functions `Y.plot...`
  * added `Y.plotFigureGetNo(createNewIfNeeded=False)`
  * added `Y.plotClose()`  (might cause trouble)

### 2008-02-26 ###
  * added `colorAxis="smart"` option to `viewInViewer2(...)
  * changed default colorAxis in `Y.view2` to `"smart"`

### 2008-02-25 ###
  * fixed `PriApp` to not overwrite `sys.app` if it exists (TODO: fix usefulX.py -> usefulX2.py (import wx without DISPLAY problem, then we don't need sys.app)
  * note: add `__init__.py` in PriApp folder  -- then you can do: from PriApp import ...

### 2008-02-21 ###
  * changed `U._getImgMode()` -- returns now `return dtypet,ncols, ny,nx, isSwapped`
  * renamed module `PriiApp` to `PriApp`

### 2008-02-12 ###
  * added 'skip' option to `ifExists` in `Mrc.save`
  * added `Y.vgAddTexts`

### 2008-02-04 ###
  * added `logY=False, logX=False, logZeroOffset=.01` arguments to `U.ploty()` and `U.plotxy()`
  * fixed `U.ploty()` and `U.plotxy()` so that it can plot more than 6 "columns" in one command (instead of just doing nothing when numCols > 6)

### 2008-02-01 ###
  * (!!!) change of default origin for `F.radialArr` , `F.radialPhiArr`, `F.maxNormRadialArr`
    * before: `orig = N.array(shape) / 2.`  now: `orig = (N.array(shape)-1) / 2.`
    * example: before:  `[ 1.5  0.5  0.5]` or `[ 1.  0.]`  now: `[ 1.  0.  1.]` or `[ 0.5  0.5]`
  * changed `F.discArr`, `F.ringArr`, `F.squareArr` from `<r` to `<=r`
    * now a pixel ''at'' the radius edge is ''included''(!) and set to "inside" value

  * added `F.binaryStructure_Zero()` and `F.binaryStructure_2dDisc_in3d()`
  * added `U.uu_encodestring(text, compress=True)` and `U.uu_decodestring(text, decompress=True)`
  * added arguments `x0,y0` to `Y.vArrange()` (to prevent "loosing title bar" on OS-X)

### 2008-01-31 ###
  * fixed `U.histogram()` (and implicitly all related) so that "amax" will be the (included !) lower bound of the last bin; before it was the (non-included!!) upper bound of the last bin. (not a min,max of 0..255 with 256 bins will results in a bin-width of 1)
  * cleaned up `usefulX2.py` by adding arguments to `viewerCommon.py::readGLviewport(self, clip=False, flipY=True, copy=True)`

### 2008-01-30 ###
  * added optinal argument `returnTuple` to `U.histogram` (`if returnTuple: return (histArray, nBins, amin, amax)`)
  * fixed `X`-axis (bins) in `U.histogramXY` and `U.histogramYX`

### 2008-01-25 ###
  * **running list of true division** bugs:
    * .../Priithon\_25\_mac/PIL/XVThumbImagePlugin.py:30: DeprecationWarning: integer argument expected, got float
> > PALETTE = PALETTE + (chr((r\*255)/7)+chr((g\*255)/7)+chr((b\*255)/3))
      * .../Priithon\_25\_mac/PIL/GifImagePlugin.py:90: DeprecationWarning: integer argument expected, got float
> > if not (chr(i/3) === p[i](i.md) === p[i+1] === p[i+2]):
      * TiffImagePlugin.py:633: DeprecationWarning: integer argument expected, got float
> > > > palette = map(lambda a: chr(a // 256), self.tag[COLORMAP](COLORMAP.md))
      * same file: `count = count // 2        # adjust for rational data field `
      * `stride = len(bits) * ((im.size[0]*bits[0]+7)//8)`
      * `usefulX2.py::1671`: `ddx = int(dx/l)`


  * new file !! `splitNDcommon.py` to separate out common parts of `splitND.py` and `splitND2.py`
  * fixed `OnZZSlider`:  every graphic having (also) a name like `tuple(z,)`(general: `zsecTuple`) will get "automagically" enables as the z-slider goes to that zsec, the graphics from the "last seen zsec" will get disabled





### 2008-01-24 ###
  * fixed tite when opening TIF/jpeg/lsm suing drag-and-drop  for `viewer2`
  * in `Scientific_IO_TextFile.py` changed mode from 'r' to 'rU' -- `U.readArray...` now handle mac-newline format

### 2008-01-21 ###
  * `Y.view2` viewer (i.e. `splitND2.py`) shows on mouse-over pixel values for all colors
  * `Y.view()` and `Y.view2()` can handle `bool`-arrays now....

  * changed in `Y.vgAddArrows()`, `Y.vgAddArrowsDelta()`, `Y.vgAddLineStrip()`, `Y.vgAddLines()`:

> > argument `as` and `bs` (not in `LineStrip` and `Lines`) to
> > `ps` and `qs`

  * BIG CHANGE !!!!!!!!!!
    * ew division**is now by default on !!
> > changed   PY="python2.5  -Qnew" and PYW="pythonw2.5  -Qnew"**


> let's see if it all still works !?!?  write `arr[i//2]` instead of `arr[i/2` !!


  * change: `U._getImgMode` now returns extra `BigEndian` bool-value, to help handling some TIFF files (CHECK !!)



### 2008-01-18 ###
  * added `Y.vDrawingCircles(v_id=-1, channel=None, r=10, val=1, add=0)`


### 2008-01-14 ###
  * added `Y.vHistScale2()` and `Y.vHistScale2Get()`
  * added support for a **.priithonrc.py** file. It will be executed from `startupPriithon.py`
    * the file is looked for in the current directory, then in PRIITHONRC env var, then in HOME dir
    * added `U._execPriithonRunCommands()` and `U._getRCfile()`
  * added `U.getHomeDir()`

### 2008-01-10 ###
  * fixed bug in `newGLListRemove()` (`Y.vgRemove()`)  for negative `idx`

### 2008-01-08 ###
  * `Y.vHistScale()` added `autoscale=True` argument

### 2007-12-18 ###
  * added `b`-key as viewer shortcut for "hide all gfx" (the letter B is close to G on the keyboard, and almost all others where already used)

### 2007-12-13 ###
  * TODO: fix / decide how Mrc.py handles 2D images; if nz === 1 should the z-dimension be removed ?
  * TODO:  change py/editor py/frame --> editor should have a `write()` method so that it can be used with `print` -- frame should have the proper generic(!) file-menu, only PyShellFrame should have a "special Priithon file menu"
  * TODO:  remove /decide on `__main__.shell` and `sys.app`

  * added: `Y.vgAddEllipses()`
  * implemented ROI types `box`, `circle`(Ellipses), `line`
  * added `Y.vROI().mask`

### 2007-12-10 ###
  * renamed `U._getTifMode(im)` to `U._getImgMode(im)`
  * added `U.loadImg_seq()` to load a squence of multiple tif (or other formats) into a single numpy array


### 2007-11-23 ###
  * fixed `splitND2.data` attribute to keep `Mrc` attribute (after discussion on numpy-mailing list and reading http://www.scipy.org/Subclasses)

### 2007-11-21 ###
  * renamed `Y.varrage()` to `Y.vArrage()`
  * renamed `Y.vSettings()` to `Y.vHistSettings`
  * added doc strings to many functions in `Y` module
  * added `F.zeroArrB` for uint8 array
  * added `Y.vgEnableMaster()` and `Y.vgEnabledMaster()` to set/get master-enable line-gfx for viewer

### 2007-11-20 ###
  * added `view()` menu command in histogram context of multi-color viewer
### 2007-11-14 ###
  * added `usingXX` argument to `vTransferFct` to provide `xx ` as shortcut for scaled and clipped `x`
  * cleaned up `viewer.py`
    * removed `m_imgToDo`, now taken care or `m_imgChanged`
    * removed `m_histScaleChanged` (also now taken care or `m_imgChanged` -- as histScale changed, always required to reload the data into the gfx card)
    * renamed `maxUShort` to `maxValueWhite`
  * added new color map "gray Min Max" - like grey, but shows min in blue, max in red
    * see `viewer.cmGrayMinMax(minCol, maxCol)`
  * "renamed" in `viewerRubberbandMode` (returned by `Y.vROI`) changed `xy0`,`xy1`  to `yx0` and `yx1`

### 2007-11-12 ###
  * renamed `Y.vScale()` to `Y.vHistScale()`
  * added `Y.vHistScaleGet()`
  * added `Y.vColMap()`

### 2007-11-08 ###
  * added `Y.DropFrame()` (removed `Y.dragFrame()`)
    * execute a given string for every file dropped into a frame

### 2007-11-02 ###
  * added useful functions to `Y` module from "3D picker" application
    * `vgMarkIn3D`
      * place marker at 3D position,
> > > above and below markerZ show marker in different color
> > > default: green above (z+), red below (z-)
> > > outside z +/- zPlusMinus: don't show marker at all - default: zPlusMinus=1000
    * `vFollowMouse`
      * connect mouse pointer of XY-view with a
> > > > "moving cross" in other XY or XZ views of same data set

  * `vFollowMouseReset`
    * disconnect mouse pointer again
### 2007-10-31 ###
  * fixes for `viewInViewer2` - color view with `listFilesViewer`
    * change from n colors to m!=n colors
    * change from one dataset to different sized dataset

### 2007-10-11 ###
  * added `U.localsAsOneObject()` - very helpful for code testing/algorithm development
  * `U.loadImageFromURL(url)` to download images from the web -- TODO: find ImageJ samples by "keyword"


### 2007-09-27 ###
  * PyShell: Ctrl-D behaves now as DELETE (like in Unix/Emacs) -- default was: duplicate line

  * found existing command in PyShell:  Shift-Ctrl-V (PastePlus) calls "Paste-And-Run" --- this actually allowes pasting multi-line python-text and executing it line-by-line(!)

  * `Y.vTransfer...` changed from using eval to using exec - results needs to get assigned to `y`
    * `Y.vTransferFct` now supports RGB output

  * removed used `maparr` and `maparrt` from `Y` module (imported from `usefulP.py`) -- what were these used for .... ?


### 2007-08-27 ###
  * removed `alpha` argument in `viewer2.py::addImg` and `addImgL` -- was not used !
  * changed BLEND-function from `glBlendFunc(GL_SRC_ALPHA, GL_ONE)` to `glBlendFunc(GL_ONE, GL_ONE)`
    * ref. OpenGL-doc for `GL_LUMINANCE` -- i.e. alpha was one anyway !
  * `Y.vgAdd...` command set blend function to `(GL_ONE,GL_ZERO)` before and `(GL_ONE,GL_ONE)` after
    * so now: a green cross really stays green ;-)
    * no change for `viewer.py` - BLEND is not enabled ...

### 2007-08-22 ###
  * added slider control to `ButtonBox` (type `sl`)
  * added `Y.vRotate()` to show data rotated and/or mirrored -- `angle=None` shows nice ''slider GUI''

### 2007-08-21 ###
  * call initial `v.center()` from inside `OnPaint` instead of `splitND.py::__init__` to ensure existence of window (`self.m_w`)

### 2007-08-17 ###
  * remove `splitND.py::scale()` and same in `splitND2.py`  - was not used ...
### 2007-08-08 ###
  * added `what` argument to `Y.inspect()`
### 2007-08-08 ###
  * added `Y.viewInViewer2()` and `multi-color`-checkbox in `Y.listArray/FilesViewer()`
    * needs more testing...

### 2007-08-07 ###
  * added `Mrc.shapeFromHdr(hdr, verbose=0)`
  * fixed `Mrc.Mrc2.setHdrForShapeType()` for 4+ dim data - todo: fix logic `setHdrForShapeType` vs. `init_simple()` -- why must one call both !?

### 2007-08-06 ###
  * `buttonBox`:  ''(changes untested)''
    * added `verticalLayout` option - default is `False`
    * added `'tb'` type for toggleBotton
  * experimental:
    * added `U.interpolate1d(x0, y, x=None)`
    * added `U.arrSharedMemory()` - windows only !

### 2007-08-01 ###
  * `F` module: renamed in many functions argument `type` to `dtype`
  * fixed `F.drawHexPattern2d()`
  * aaded `Y.clipboardImageSaveToFile()`
  * fixed `plt` package: plotting of `uint8` data
  * changed TAB-key on continuation lines in `shell.py`

### 2007-07-26 ###
  * added `execModule` argument to buttonBox - exec in `__main__` stays default
  * added documentation to buttonBox.py`
  * added `Y.buttonBox_clickButton(label, bb_id=-1)`
  * new geometry module: `usefulGeo` imported '**' into `U`
    * `geoPointLineDist`, `geoPointSegsDist`, `geoPointSeqSide`, `geoPointsEq`, `geoSegEqOpposite`, `geoSeqsBoundingBox`
  * added `U.strTranslate(s, frm='', to='', delete='', keep=None)`  (and `string` module into `U`)
  * added `Y.vShortcutAdd()` and `Y.vShortcutReset()`**


### 2007-07-25 ###
  * moved recalcHist into onIdle ((TODO:  make `recalcHist` into a thread that can be interupted/aborted as needed -- especially needed for `splitND2`))
  * added `U.reloadAll(verbose=False, repeat=1)`

### 2007-07-24 ###
  * fixed viewer-title for viewer opened with `Y.listFilesViewer()`
  * renamed `Y.viewerRubberbandMode()` to `Y.vROI()`

### 2007-07-23 ###
  * added `Y.getClipboardText()`
  * prepared code for "exec clipboard" button function
    * added optional `newPrompt` argument to `shell.push()`
  * `histogram`: changed default to log-scale


### 2007-07-14 ###
  * added `Y.plotSetColorsDefault()`
  * removed `includeAll.py` and `includeAllOnLetter.py` - not used
  * created `viewerCommon.py` -- base class for `viewer` and `viewer2`
  * removed `self.m_pixelGrid =3D 0 # 0x3333` -- was already not used,
instead viewer grid was/is done via `newGLList...()` (dashed lines
(0x3333) were/are also not used anymore)

  * TODO:
    * popmenu - hide all gfx - never shows check-mark on Windows
    * F.lowPassFilter -- instead of using sigma (of the gaussian) use
arr.shape/sigma **someFactor -- to indicate how much a pixel will
spread.  Watch out for non square images !!
    * remove `__main__.shell`  -- use `sys.app.frame.shell` instead
-- support multiple shell windows !!**

  * added `U.gamma(x)`: gamma functions for  x=3D.5, 1, 1.5, ...
  * added `F.lorentzian()` and `F.lorentzianArr`
  * fixed `Y.shell()` and `Y.crust()` to use Priithon's not wx's
py-package  ((wx.py.introspect still has seb's numarray stuff in it
... BUG!))
  * (started) to add matplotlib as 'P' module into Priithon
  * added `metamenus.py` by E. A. Tacao (http://j.domaindlx.com/elements28/wxpython/Metamenus.html)


### 2007-07-12 ###
  * added `Y.vCopyToClipboard()`
  * in viewer pop-menu added `save to clipboard` and `center`
  * in shell - imporved TAB-completion: now tab after '(' and `xx.yy` shows popup - no pop-up when empty choice list
  * renamed in `viewer.py`: `On30`,`On31`,`On32` to `OnCenter/OnZoomIn/Out`
  * make closing PyShell-window smart (asks if other windows are open)


### 2007-07-05 ###
  * move `shellMessage()` and `assignNdArrToVarname` into `usefulX2.py`

### 2007-06-27 ###
  * `viewerRubberbandMode.py`: AltDown: even sized --- Ctrl ''or'' Shift: square ---  Ctrl ''and'' Shift: power of 2 sized

### 2007-06-21 ###
  * `MySplitter` removed from `splitND`-class -- wx has `wxSplitterWindow::SetSashGravity` since 2.6 to support "resizing top part" instead of bottom
    * added `style=wx.SP_LIVE_UPDATE|wx.SP_3DSASH` instead of default `wx.SP_3D`
    * added `histogram::OnEraseBackground()` back in -- much less flickering (not quite perfect - but much better)
  * revive `splitND2`
    * added on-off toggle button for each channel
    * double click into histogram, switches display color of respective channel
  * `splitND.spv.viewer` now moved to `usefulX2` module variable -- shared between `splitND` and `splitND2`

### 2007-06-01 ###
  * fixed `float()` in `histogram autoFit` -- pyOpenGL cannot handle numpy.float32
  * changed mouse-cursor back from cross to arrow -- on Win only, black cross on black image was bad...
  * fixed `Y.vzslider()`, `splitND setSlider()`
  * added `Y.vSetSlider` with autoscale option


---


### older changes ###

> [changes done at UCSF](http://code.google.com/p/priithon/wiki/ChangeLog_old_SF)

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