"""Priithon Y module: all functions to do with GUI
"""

__author__  = "Sebastian Haase <haase@msg.ucsf.edu>"
__license__ = "BSD license - see LICENSE file"

import wx
import numpy as N

_error =  _error0 = '' ## FIXME
try:
    _saveSessionDefaultPrefix
except:
    _saveSessionDefaultPrefix = "_pySession-"


def _bugXiGraphics(doWorkaround=1):
    import viewer
    viewer.bugXiGraphics = doWorkaround
    import viewer2
    viewer2.bugXiGraphics = doWorkaround
    import mmviewer
    mmviewer.bugXiGraphics = doWorkaround

def test():
    """test for  viewer + histogram with colMap band"""
    q = N.zeros((256,256), dtype=N.uint8)
    q[:] = N.arange(256)
    view(q)
def test2():
    """test for  viewer2 + histogram with colMap band"""
    q = N.zeros((3,256,256), dtype=N.uint8)
    q[0,:] = N.arange(256)
    q[1,:] = N.arange(256-1,-1,-1)
    q[2,:] = N.arange(256)[:,None]
    view2(q)



def editor(filename=None, retTextWindow=False):
    """
    if filename is None:
        open new <blank> file
    elif filename is a module:
        open the corresponding .py file if possible 
    if retTextWindow:
        return the wxStyledTextCtrl object
        this can be used to print into
    """
    import os.path
    if type(filename) == type(wx): # module
        if hasattr(filename, "__file__")                     \
                and filename.__file__[-4:-1] == '.py'        \
                and os.path.isfile(filename.__file__[:-1]):
            filename = filename.__file__[:-1]
        else:
            raise ValueError, "cannot find .py file for %s"%filename

    from wx import py
    f = py.editor.EditorFrame(parent=None,#, would kill editor without cheking for save !! sys.app.GetTopWindow(),
                                 title="Priithon Editor",
                                 filename=filename)
    if not filename: # we ALWAYS want bufferCreate - even when filename is "False"
        f.bufferCreate(filename)
    f.Show()
    if retTextWindow:
        return f.editor.window

def commands():
    import __main__
    f = wx.Frame(None, -1, "command history") #, size=wx.Size(400,400))
    sizer = wx.BoxSizer(wx.VERTICAL)
    #import __main__
    #cl = __main__.shell.history
    l = wx.ListBox(f, wx.ID_ANY) #, choices=cl) #, wx.LB_SINGLE)
    sizer.Add(l, 1, wx.EXPAND | wx.ALL, 5);
    #wx.EVT_LISTBOX(f, 60, self.EvtListBox)
    def dd(ev):
        #s= ev.GetString()
        s = l.GetStringSelection()
        #print s

        endpos = __main__.shell.GetTextLength()
        __main__.shell.InsertText(endpos, s)
        # __main__.shell.AppendText(len(s), s)
        __main__.shell.SetFocus()

    wx.EVT_LISTBOX_DCLICK(f, l.GetId(), dd)
    # wx.EVT_RIGHT_UP(self.lb1, self.EvtRightButton)

    hsz = wx.BoxSizer(wx.HORIZONTAL)
    sizer.Add(hsz, 0, wx.EXPAND)
    b1 = wx.Button(f, wx.ID_ANY, "insert")
    hsz.Add(b1, 1, wx.EXPAND|wx.ALL, 2)
    wx.EVT_BUTTON(f, b1.GetId(), dd)
    
    def refreshList(ev):
        cl = list(__main__.shell.history) # copy!
        cl.reverse()
        #not true-20070725 cl = cl[1:] # CHECK - first command is always: print Startup script executed: /jws30/haase/PrLin0/Priithon/includeAll.py
        l.Clear()
        l.InsertItems( cl, 0 )
        if l.GetCount():
            l.SetSelection( l.GetCount()-1 )

    b2 = wx.Button(f, wx.ID_ANY, "refresh")
    hsz.Add(b2, 1, wx.EXPAND|wx.ALL, 2)
    wx.EVT_BUTTON(f, b2.GetId(), refreshList)


    refreshList(None)

    f.SetSizer(sizer)
    #sizer.SetSizeHints(f)
    f.SetAutoLayout(1)
    sizer.Fit(f)
    f.Show()

def load(imgFN=None):
    """open any image file:
          '.fits'  - FITS files
          any image file: jpg/bmp/png/... (all PIL formats)
               #20060824 CHECK  in this case the returned arr gets attr: arr._originLeftBottom=0
          'Mrc' (use Mrc.bindFile)
          TODO: "_thmb_<fn.jpg>" files are taken to mean <fn.jpg>
       returns image array
               None on error

       if imgFN is None  call Y.FN()  for you
    """
    if imgFN is None:
        imgFN = FN()
    if not imgFN:
        return
    try:
        if imgFN[-5:].lower() == ".fits":
            import useful as U
            a = U.loadFits( imgFN )
        elif imgFN[-4:].lower() == ".sif":
            import useful as U
            a = U.loadSIF( imgFN )
        else:
            try:
                iDelta = 1
                if imgFN[-4:].lower() == ".lsm":
                    iDelta=2 # LSM-Zeiss every 2nd img is a thumbnail
                import useful as U
                a = U.loadImg(imgFN, iDelta=iDelta)
                #20060824 CHECK  a._originLeftBottom=0
            except (IOError, SystemError):
                import Mrc
                a = Mrc.bindFile(imgFN)
    except:
        import sys
        e = sys.exc_info()
        wx.MessageBox("Error when opening: %s - %s" %\
                      (str(e[0]), str(e[1]) ),
                      "Bad File !?",
                      style=wx.ICON_ERROR)
    else:
        return a

def viewInViewer(id, a, title=None, doAutoscale=1):
    """
    like view but instead of opening a new window
    it reused existing viewer # id
    if that viewer is closed (or was newer opened)
    viewInViewer fails EXCEPT id==-1
      in that case a new viewer is created and gets reused
      for subsequent called with id=-1
    """
    try:
        spv =  viewers[id]
        if spv is None:
            raise 'xx'
    except:
        if id==-1:
            view(a)
            return
        else:
            raise "viewer %d doesn't exist"%id

    from splitND import spv as spv_class
    if not isinstance(spv, spv_class):
        raise RuntimeError, "viewer #%d is not a mono-color viewer" % id

    if min(a.shape) < 1:
        raise ValueError, "array shape contains zeros (%s)"%(a.shape,)
    
    #multicolor = hasattr(spv, "ColorAxisOrig") # HACK FIXME


    #print a.ndim-2, spv.zndim
    if a.ndim-2 != spv.zndim:
        #wx.MessageBox("Dimension mismatch old vs. new",
        #             "Differnt dimesion !?",
        #             style=wx.ICON_ERROR)
        spv.zshape= a.shape[:-2]
        spv.zndim = len(spv.zshape)
        spv.zsec  = [0] * spv.zndim
        spv.zlast = [0]*spv.zndim # remember - for checking if update needed

        spv.putZSlidersIntoTopBox(spv.upperPanel, spv.boxAtTop)
    else:
        spv.zshape= a.shape[:-2]
        for i in range(spv.zndim):
            nz = a.shape[i]
            spv.zzslider[i].SetRange(0, nz-1)
            if spv.zsec[i] >= nz:
                spv.zsec[i] = 0 # maybe better: nz-1
                spv.zlast[i] = 0

    spv.data = a
    spv.helpNewData(doAutoscale=doAutoscale)
    if title is None:
        title=''
        if hasattr(spv.data, 'Mrc'):
            title += "<%s>" % spv.data.Mrc.filename
    title2 = "%d) %s" %(spv.id, title)
    
    #20070808spv.frame.SetTitle(title2)
    wx.GetTopLevelParent(spv.viewer).SetTitle(title2) # CHECK

def viewInViewer2(id, a, colorAxis="smart", title=None, doAutoscale=1):
    """
    like view2 but instead of opening a new window
    it reused existing viewer # id
    if that viewer is closed (or was newer opened)
    viewInViewer2 fails EXCEPT id==-1
      in that case a new viewer is created and gets reused
      for subsequent called with id=-1
    """
    try:
        spv =  viewers[id]
        if spv is None:
            raise 'xx'
    except:
        if id==-1:
            view2(a)
            return
        else:
            raise "viewer %d doesn't exist"%id

    from splitND2 import spv as spv2_class
    if not isinstance(spv, spv2_class):
        raise RuntimeError, "viewer #%d is not a multi-color viewer" % id

    if a.ndim < 3:
        raise ValueError, "array ndim must be at least 3"
    if min(a.shape) < 1:
        raise ValueError, "array shape contains zeros (%s)"%(a.shape,)
    
    #multicolor = hasattr(spv, "ColorAxisOrig") # HACK FIXME


    #print a.ndim-2, spv.zndim
    if a.ndim-3 != spv.zndim:
        # reinit number of "z sliders" (ndim-3 == colorAxis is excluded)
        spv.zshape= a.shape[:-3]
        spv.zndim = len(spv.zshape)
        spv.zsec  = [0] * spv.zndim
        spv.zlast = [0] * spv.zndim # remember - for checking if update needed

        spv.putZSlidersIntoTopBox(spv.upperPanel, spv.boxAtTop)
    else:
        spv.zshape= a.shape[:-3]
        for i in range(spv.zndim):
            nz = a.shape[i]
            spv.zzslider[i].SetRange(0, nz-1)
            if spv.zsec[i] >= nz:
                spv.zsec[i] = 0 # maybe better: nz-1
                spv.zlast[i] = 0

    if a.shape[-3] != spv.nColors:
        if a.shape[-3] < spv.nColors:
            # delete last images first -> ::-1 (reverse)
            for i in range(a.shape[-3], spv.nColors)[::-1]:
                spv.viewer.delImage(i)
        else:
            # add additional images(=colors)
            imgL =  a[tuple(spv.zsec)]
            spv.viewer.addImgL(imgL[spv.nColors:])
            # NOTE: the image data might get loaded into gfx-card twice - because of setImage call 

        # reinit number of color channnels
        spv.nColors = a.shape[-3]
        spv.histsPanel.DestroyChildren()
        spv.initHists()
        #FIXME spv.splitter.SplitHorizontally(spv.upperPanel, spv.histsPanel, -40*spv.nColors)
        spv.histsPanel.Layout() # triggers redraw

    spv.data = a
    spv.helpNewData(doAutoscale=doAutoscale)
    if title is None:
        title=''
        if hasattr(spv.data, 'Mrc'):
            title += "<%s>" % spv.data.Mrc.filename
    title2 = "%d) %s" %(spv.id, title)
    #20070808spv.frame.SetTitle(title2)
    wx.GetTopLevelParent(spv.viewer).SetTitle(title2) # CHECK

class _listFilesViewer:
  def __init__(self, dir=None, viewerID=None):
    self.viewerID = viewerID
    self.dir = dir
    if self.dir is None:
        self.dir = DIR(0)
        if not self.dir:
            return
    import os
    #self.dir=os.path.abspath(os.path.dirname(self.dir))
    self.dir=os.path.abspath(self.dir)
    frame = wx.Frame(None, -1, '') #, size=wx.Size(400,400))
    sizer = wx.BoxSizer(wx.VERTICAL)
    self.lb = wx.ListBox(frame, wx.ID_ANY, size=(300,400)) #, choices=cl) #, wx.LB_SINGLE)
    sizer.Add(self.lb, 1, wx.EXPAND | wx.ALL, 5)
    #wx.EVT_LISTBOX(f, 60, self.EvtListBox)
    wx.EVT_MOTION(self.lb, self.onStartDrag)

    def onDClick(ev):
        #s= ev.GetString()
        s = self.lb.GetStringSelection()
        fn = self.dir+'/'+s

        import os.path
        if os.path.isdir(fn):
            self.dir = os.path.normpath(fn)
            #20051201 n = os.path.basename(self.txt.GetValue())
            #20051201 self.txt.SetValue(os.path.join(self.dir, n))
            self.txt.SetValue(os.path.join(self.dir, '*'))
            refreshList()
            return
        a = load(fn) #20051213
        if a is None:
            return
        if     not self.reuse.GetValue() or \
               self.viewerID is None or \
               self.viewerID >= len(viewers) or \
               viewers[self.viewerID] is None:
            if self.multicolor.GetValue():
                # 20071114 added back "title" because of tif files  - FIXME 
                view2(a, title="<%s>" % s) #20071106 splitND.makeFrame auto-appends filename-title:, title="<%s>"%s)
            else:
                # 20071114 added back "title" because of tif files - FIXME 
                view(a, title="<%s>" % s) #20071106 splitND.makeFrame auto-appends filename-title:, title="<%s>" % s) #fn)
            self.viewerID = len(viewers)-1
            title = "files in %s (viewer %s)" % (self.dir, self.viewerID)
            frame.SetTitle(title)
        else:
            if self.multicolor.GetValue():
                viewInViewer2(self.viewerID, a, title="<%s>" % s, doAutoscale=self.autoscale.GetValue())
            else:
                viewInViewer(self.viewerID, a, title="<%s>" % s, doAutoscale=self.autoscale.GetValue())
        #print s
        
    def refreshList(ev=None):
        import os.path,os
        import glob
        filesGlob = self.txt.GetValue()
        if os.path.isdir(filesGlob):
            self.dir = filesGlob
            #sort broken: dd= map(os.path.abspath, os.listdir(filesGlob) )
            dd = glob.glob(filesGlob+'/*')
        else:
            self.dir = os.path.dirname(filesGlob)
            dd = glob.glob(filesGlob)
        
        def mySort(f1,f2):
            d1 = int( os.path.isdir(f1) )
            d2 = int( os.path.isdir(f2) )
            #ddd = d1-d2    # move dirs to end of list
            ddd = d2-d1
            #print ddd, f1,f2

            return ddd or cmp(f1,f2)
        dd.sort( mySort )
        dd = [os.path.basename(f) for f in dd]
        dd[0:0] = ["../"]

        di = 1 # just in case for-loop doesn;t run == di used below !!
        for di in range(1,len(dd)):
            if os.path.isdir(self.dir+'/'+dd[di]):
                dd[di] += '/'
            else:
                break
        self.lb.Clear()
        self.lb.InsertItems( dd, 0 )
        self.lb.SetSelection( di ) # first is '..'

        title = "files in %s (viewer %s)" % (self.dir, self.viewerID)
        frame.SetTitle(title)


    #wx.EVT_LISTBOX_DCLICK(frame, 1001, onDClick)
    wx.EVT_LISTBOX(frame, self.lb.GetId(), onDClick)
    # wx.EVT_RIGHT_UP(self.lb1, self.EvtRightButton)

    hsz = wx.BoxSizer(wx.HORIZONTAL)
    sizer.Add(hsz, 0, wx.EXPAND)

    self.txt = wx.TextCtrl(frame, wx.ID_ANY, self.dir)
    hsz.Add(self.txt, 1, wx.EXPAND|wx.ALL, 2)
    wx.EVT_TEXT(frame, self.txt.GetId(), refreshList)
    
    self.autoscale = wx.CheckBox(frame, wx.ID_ANY, "autoscale")
    hsz.Add(self.autoscale, 0, wx.EXPAND|wx.ALL, 2)
    self.autoscale.SetValue(1)
    self.reuse = wx.CheckBox(frame, wx.ID_ANY, "reuse")
    hsz.Add(self.reuse, 0, wx.EXPAND|wx.ALL, 2)
    self.reuse.SetValue(1)
    self.multicolor = wx.CheckBox(frame, wx.ID_ANY, "color")
    hsz.Add(self.multicolor, 0, wx.EXPAND|wx.ALL, 2)
    #self.multicolor.SetValue(1)

    #b1 = wx.Button(frame, 1002, "show")
    #hsz.Add(b1, 0, wx.EXPAND|wx.ALL, 2)
    #wx.EVT_BUTTON(frame, 1002, onDClick)
    
    #b2 = wx.Button(frame, 1003, "refresh")
    #hsz.Add(b2, 0, wx.EXPAND|wx.ALL, 2)
    #wx.EVT_BUTTON(frame, 1003, refreshList)

    ll = self.txt.GetLastPosition()
    #self.txt.ShowPosition(ll) #makes only LINE of ll visible
    self.txt.SetInsertionPoint(ll)

    refreshList(None)

#   if self.lb.GetCount() > 1:
#       if viewerID is None:
#           view(self.dir+"/"+self.lb.GetString(1)) # first is '..'
#           id = len(viewers)-1
#       else:
#           id = viewerID

    frame.SetSizer(sizer)
    sizer.SetSizeHints(frame)
    frame.SetAutoLayout(1)
    sizer.Fit(frame)
    frame.Show()
  def onStartDrag(self, evt):
      if evt.Dragging():
          import os.path
          fn = self.lb.GetStringSelection()
          fn = os.path.join(self.dir, fn)
          data = wx.FileDataObject()
          data.AddFile(fn)
          dropSource = wx.DropSource(self.lb)
          dropSource.SetData(data)
          dropSource.DoDragDrop(1)
      evt.Skip()

def listFilesViewer(dir=None, viewerID=None):
    """
    open a window showing a list of all (image) files in a given directory
    per click these can be displayed in an image viewer
    """
    global _listFilesViewer_obj
    _listFilesViewer_obj = _listFilesViewer(dir,viewerID)

class _listArrayViewer:
  def __init__(self, modname='__main__', viewerID=None):
    self.viewerID = viewerID
    import sys
    
    frame = wx.Frame(None, -1, "") #, size=wx.Size(400,400))
    sizer = wx.BoxSizer(wx.VERTICAL)
    self.lb = wx.ListBox(frame, wx.ID_ANY, size=(300,400)) #, choices=cl) #, wx.LB_SINGLE)
    sizer.Add(self.lb, 1, wx.EXPAND | wx.ALL, 5);
    #wx.EVT_LISTBOX(f, 60, self.EvtListBox)
    def onDClick(ev=None):
        #s= ev.GetString()
        s = self.lb.GetStringSelection()
        mod = __import__(modname) # , globals(), locals(), [])
        showdict=mod.__dict__
        a = showdict[s]
        if     not self.reuse.GetValue() or \
               self.viewerID is None or \
               self.viewerID >= len(viewers) or \
               viewers[self.viewerID] is None:

            if self.multicolor.GetValue():
                view2(a, title="%s"%s)
            else:
                view(a, title="%s"%s)
            self.viewerID = len(viewers)-1
            title = "arrays in %s (viewer %s)" % (modname, self.viewerID)
            frame.SetTitle(title)
        else:
            if self.multicolor.GetValue():
                viewInViewer2(self.viewerID, a, title="%s"%s, doAutoscale=self.autoscale.GetValue())
            else:
                viewInViewer(self.viewerID, a, title="%s"%s, doAutoscale=self.autoscale.GetValue())
#       #print s
        
    def refreshList(ev=None):
        modname = self.txt.GetValue()
        #       if not modname:
        #           global fr,fc, argsn, args
        #           fr = sys._getframe(1)
        #           fc = fr.f_code
        #           showdict = fr.f_locals # .keys()
        #           modname = fr.f_globals['__name__']
        
        #           # fr.f_globals['__name__']
        #           # '__main__'
        #           # fr.f_locals['__name__']
        #           # '__main__'
        #       else:
        if not modname:
            modname = '__main__'
        try:
            #exec('import %(modname)s;showdict=%(modname)s'%locals())
            mod = __import__(modname) # , globals(), locals(), [])
            showdict=mod.__dict__ # eval('%(modname)s.__dict__'%locals())
        except ImportError:
            frame.SetTitle("module '%s' not found" % modname)
            self.lb.Clear()
            return
        varlist = []
        arrs = {}
    
        def sebsort(m1,m2):
            import __builtin__
            k1 = arrs[ m1 ][1]
            k2 = arrs[ m2 ][1]
            return __builtin__.cmp(k1,  k2)

        for k in showdict:
            o = showdict[k]

            if isinstance(o, N.ndarray):
                varlist.append(k)
                # 20070731 size = len(o.data)
                # 20070731 memAt = o.ctypes.get_data()
                '''20070731
                f = string.split( repr(o._data) )
                if f[0] == '<memory': # '<memory at 0x50a66008 with size:0x006f5400 held by object 0x092772e8 aliasing object 0x00000000>'
                    fs = string.split( f[4],':' )
                    size   = eval( fs[1] )
                    memAt  = f[2]
                    objNum = f[8]
                elif f[0] == '<MemmapSlice': # '<MemmapSlice of length:7290000 readonly>'
                    fs = string.split( f[2],':' )
                    size   = eval( fs[1] )
                    objNum = 0
                else:
                    #print "# DON'T KNOW: ",     k, repr(o._data)
                    continue
                    '''
                '''20070731
                try:
                    arrs[ memAt ][0] += 1
                    arrs[ memAt ][1].append( k )
                    arrs[ memAt ][2].append( size )
                except:
                    arrs[ memAt ] = [ 1, [k], [size] ]
                '''

        '''20070731 was this to only show an array once - even if there are to names for it in the dictionary !?!?!?
        ms = arrs.keys()
        ms.sort( sebsort )
        #print kStringMaxLen
        for memAt in ms:
            ks   = arrs[ memAt ][1]
            size = arrs[ memAt ][2][0]
            o = showdict[ ks[0] ]
            if len(ks) == 1:
                ks = ks[0]
    
            varlist.append(ks)
        '''
        varlist.sort()


        self.lb.Clear()
        if len(varlist):
            self.lb.InsertItems( varlist, 0 )
            self.lb.SetSelection( 0 )

        title = "arrays in %s (viewer %s)" % (modname, self.viewerID)
        frame.SetTitle(title)


    #wx.EVT_LISTBOX_DCLICK(frame, self.lb.GetId(), onDClick)
    wx.EVT_LISTBOX(frame, self.lb.GetId(), onDClick)
    # wx.EVT_RIGHT_UP(self.lb1, self.EvtRightButton)

    hsz = wx.BoxSizer(wx.HORIZONTAL)
    sizer.Add(hsz, 0, wx.EXPAND)

    self.txt = wx.TextCtrl(frame, wx.ID_ANY, modname)
    hsz.Add(self.txt, 1, wx.EXPAND|wx.ALL, 2)
    wx.EVT_TEXT(frame, self.txt.GetId(), refreshList)
    
    self.autoscale = wx.CheckBox(frame, wx.ID_ANY, "autoscale")
    hsz.Add(self.autoscale, 0, wx.EXPAND|wx.ALL, 2)
    self.autoscale.SetValue(1)
    self.reuse = wx.CheckBox(frame, wx.ID_ANY, "reuse")
    hsz.Add(self.reuse, 0, wx.EXPAND|wx.ALL, 2)
    self.reuse.SetValue(1)
    self.multicolor = wx.CheckBox(frame, wx.ID_ANY, "color")
    hsz.Add(self.multicolor, 0, wx.EXPAND|wx.ALL, 2)
    #self.multicolor.SetValue(1)
    
    #b1 = wx.Button(frame, 1002, "show")
    #hsz.Add(b1, 0, wx.EXPAND|wx.ALL, 2)
    #wx.EVT_BUTTON(frame, 1002, onDClick)
    
    b2 = wx.Button(frame, wx.ID_ANY, "refresh")
    hsz.Add(b2, 0, wx.EXPAND|wx.ALL, 2)
    wx.EVT_BUTTON(frame, b2.GetId(), refreshList)

    ll = self.txt.GetLastPosition()
    #self.txt.ShowPosition(ll) #makes only LINE of ll visible
    self.txt.SetInsertionPoint(ll)

    refreshList()
    #onDClick()
    frame.SetSizer(sizer)
    sizer.SetSizeHints(frame)
    frame.SetAutoLayout(1)
    sizer.Fit(frame)
    frame.Show()
    ##return None # CHECK - still returns self - CHECK
def listArrayViewer(modname='__main__', viewerID=None):
    """
    open a window showing a list of all numpy arrays in given module
    per click these can be displayed in an image viewer
    """
    global _listArrayViewer_obj
    _listArrayViewer_obj = _listArrayViewer(modname,viewerID)

    
def saveSession(fn=None):
    """
    saves all text from PyShell into a file w/ file name 'fn'
    if fn is None it calls smart 'FN()' for you
    """
    
    import sys
    if hasattr(sys, "app"):       # PyShell, PyCrust, ...
        shell = sys.app.frame.shell
#     elif hasattr(sys, "shell"): # embedded in OMX
#         import __main__
#         shell = __main__.shell
#         #shell = sys.shell
    else:
        raise RuntimeError, "sorry, can't find shell"

    if fn is None:
        import time
        # global _saveSessionDefaultPrefix
        fn = _saveSessionDefaultPrefix + time.strftime("%Y%m%d-%H%M.py")
        fn = wx.FileSelector("Please select file", "",fn, flags=wx.SAVE)

    if not fn: # cancel
        return

    f = open(fn, "w")
    f.write(shell.GetText())
    f.close()
    print "# '%s' saved." %( fn, )
    
    
def FN(save=0, verbose=1):
    """use mouse to get filename

    if verbose is true: also print filename
    """

    ## frame title, start-dir, default-filename, ??, default-pattern
    if save:
        flags=wx.SAVE
    else:
        flags=0
    fn = wx.FileSelector("Please select file", flags=flags)
    if verbose:
        print repr(fn)
    return fn

def DIR(verbose=1):
    """use mouse to get directory name

    if verbose is true: also print dirname
    """

    import os
    try:
        d = os.getcwd() # OSError or Erik's  Laptop
    except:
        d = "/"
    fn = wx.DirSelector("Please select directory", d)
    if verbose:
        print repr(fn)
    return fn

def cd():
    """change current working directory"""
    import os
    os.chdir( DIR() )

def refresh():
    """use in scripts to refresh PyShell"""
    try:
        import wx
        wx.Yield()
    except:
        pass # maybe we don't have wx...
def sleep(secs=1):
    """resfresh and then sleep"""
    try:
        import wx
        wx.Yield()
        wxSleep(secs)
    except:
        pass # maybe we don't have wx...

###############################################################################
###############################################################################
###############################################################################
###############################################################################


import plt
from usefulP import *



def plotProfileHoriz(img_id, y, avgBandSize=1, s='-'):
    if type(img_id) == int:
        img = viewers[ img_id ].img
    else:
        img = img_id
    h,w = img.shape

    if avgBandSize >1:
        vals = N.sum( img[ y:y+avgBandSize ].astype(N.float64), 0 ) / float(avgBandSize)
        ploty( vals, s )
    else:
        ploty( img[ y ], s )
def plotProfileVert(img_id, x, avgBandSize=1, s='-'):
    if type(img_id) == int:
        img = viewers[ img_id ].img
    else:
        img = img_id
    h,w = img.shape

    if avgBandSize >1:
        vals = N.sum( img[ :, x:x+avgBandSize ].astype(N.float64), 1 ) / float(avgBandSize)
        ploty( vals, s )
    else:
        ploty( img[ :, x ], s )
def plotProfileZ(img_id, y,x, avgBandSize=1, s='-'):
    if type(img_id) == int:
        data = viewers[ img_id ].data
    else:
        data = img_id

    if avgBandSize >1:
        w,h = avgBandSize,avgBandSize
        w2,h2 = w/2., h/2.
        x0,y0,x1,y1 = int(x-w2+.5),int(y-h2+.5),  int(x+w2+.5),int(y+h2+.5)
        #from useful import mean2d
        nz = data.shape[-3]
        prof = N.empty(shape=nz, dtype=N.float64)
        for z in range(nz):
            prof[z] = data[z,  y0:y1, x0:x1].mean()
        ploty( prof, s )
    else:
        ploty( data[ :, int(y), int(x) ], s )

'''

def plotFitAny(f, parms, min=None,max=None,step=None,hold=True,s='-'):
    """
    if min is None defaults to min-x of current plot (dataset 0)
    if max is None defaults to max-x of current plot (dataset 0)
    if step is None defautls to 1000 points between min and max
    if hold is not None call Y.plothold(hold) beforehand
    """
    import useful as U
    import __builtin__
    if min is None or max is None:
        dpx = plotDatapoints(0)[0]
        if min is None:
            min = __builtin__.min(dpx)
        if max is None:
            max = __builtin__.max(dpx)
    if step is None:
        step = (max-min)/1000.
    if hold is not None:
        plothold(hold)
    x=N.arange(min,max,step)
    plotxy(x,f(parms,x), s)

def plotFitLine(abTuple, min=None,max=None,step=None,hold=True,s='-'):
    """
    if min is None defaults to min-x of current plot (dataset 0)
    if max is None defaults to max-x of current plot (dataset 0)
    if step is None defautls to 1000 points between min and max
    if hold is not None call Y.plothold(hold) beforehand
    """
    import useful as U
    plotFitAny(U._poly,(abTuple[1],abTuple[0]), min,max,step,hold,s)
def plotFitPoly(parms, min=None,max=None,step=None,hold=True,s='-'):
    """
    if min is None defaults to min-x of current plot (dataset 0)
    if max is None defaults to max-x of current plot (dataset 0)
    if step is None defautls to 1000 points between min and max
    if hold is not None call Y.plothold(hold) beforehand
    """
    import useful as U
    plotFitAny(U._poly, parms, min,max,step,hold,s)
def plotFitDecay(parms, min=None,max=None,step=None,hold=True,s='-'):
    """
    if min is None defaults to min-x of current plot (dataset 0)
    if max is None defaults to max-x of current plot (dataset 0)
    if step is None defautls to 1000 points between min and max
    if hold is not None call Y.plothold(hold) beforehand
    """
    import useful as U
    plotFitAny(U._decay, parms, min,max,step,hold,s)
def plotFitGaussian1D(parms, min=None,max=None,step=None,hold=True,s='-'):
    """
    if min is None defaults to min-x of current plot (dataset 0)
    if max is None defaults to max-x of current plot (dataset 0)
    if step is None defautls to 1000 points between min and max
    if hold is not None call Y.plothold(hold) beforehand
    """
    import useful as U
    if   len(parmTuple0) == 2:
        f = U._gaussian1D_2
    elif len(parmTuple0) == 3:
        f = U._gaussian1D_3
    elif len(parmTuple0) == 4:
        f = U._gaussian1D_4
    
    plotFitAny(f, parms, min,max,step,hold,s)

'''










def plotFitAny(func, parms, min=None,max=None,step=None,hold=True,s='-', dataset=0, doFit=True):
    '''
    if min is None defaults to min-x of current plot (for given dataset)
    if max is None defaults to max-x of current plot (for given dataset)
    if step is None defautls to 1000 points between min and max
    if hold is not None call Y.plothold(hold) beforehand

    if doFit:
      do a curve fit to adjust parms  before plotting
      return (parms, fitFlag)
    '''
    import __builtin__
    if min is None or max is None:
        dpx = plotDatapoints(dataset)[0]
        if min is None:
            min = __builtin__.min(dpx)
        if max is None:
            max = __builtin__.max(dpx)
    if step is None:
        step = (max-min)/1000.
    if hold is not None:
        plothold(hold)
    x=N.arange(min,max,step)
    if doFit:
        import useful as U
        data = N.asarray(plotDatapoints(dataset), dtype=N.float64)
        parms, ret = U.fitAny(func, parms, data.T)
        
    plotxy(x,func(parms,x), s)
    if doFit:
        return parms, ret

def plotFitDecay(parms=(1000,10000,10), min=None,max=None,step=None,hold=True,s='-', dataset=0, doFit=True):
    '''
    see U.yDecay.
    if min is None defaults to min-x of current plot (dataset 0)
    if max is None defaults to max-x of current plot (dataset 0)
    if step is None defautls to 1000 points between min and max
    if hold is not None call Y.plothold(hold) beforehand
    '''
    import useful as U
    return plotFitAny(U.yDecay, parms, min,max,step,hold,s, dataset, doFit)

def plotFitGaussian(parms=(0,10,100), min=None,max=None,step=None,hold=True,s='-', dataset=0, doFit=True):
    '''
    see U.yGaussian.
    if min is None defaults to min-x of current plot (dataset 0)
    if max is None defaults to max-x of current plot (dataset 0)
    if step is None defautls to 1000 points between min and max
    if hold is not None call Y.plothold(hold) beforehand
    '''
    import useful as U
    return plotFitAny(U.yGaussian, parms, min,max,step,hold,s, dataset, doFit)

def plotFitLine(abTuple, min=None,max=None,step=None,hold=True,s='-', dataset=0, doFit=True):
    '''
    if min is None defaults to min-x of current plot (dataset 0)
    if max is None defaults to max-x of current plot (dataset 0)
    if step is None defautls to 1000 points between min and max
    if hold is not None call Y.plothold(hold) beforehand
    '''
    import useful as U
    return plotFitAny(U.yLine, abTuple, min,max,step,hold,s, dataset, doFit)
def plotFitPoly(parms, min=None,max=None,step=None,hold=True,s='-', dataset=0, doFit=True):
    '''
    if min is None defaults to min-x of current plot (dataset 0)
    if max is None defaults to max-x of current plot (dataset 0)
    if step is None defautls to 1000 points between min and max
    if hold is not None call Y.plothold(hold) beforehand
    '''
    import useful as U
    return plotFitAny(U.yPoly, parms, min,max,step,hold,s, dataset, doFit)








from gridviewer import gridview

#  try:
from histogram import hist as histogram
from mmviewer import mview
from scalePanel import scalePanel
from zslider import ZSlider

from buttonbox import *

#HIST= #dictionary
#VIEW= #dictionary

def hist(viewer, resolution=0):
    """old"""
    import useful as U
    try:
        img  = viewer.m_imgArr
    except:
        img  = viewer.m_imgArrL[0] ## hack !
    mmms = U.mmms(img)
    if not resolution:
        resolution = int(mmms[1]-mmms[0]+2) # e.g. (8.8-0)
        if resolution > 10000:
            print "resolution (max-min = %d) limited to %d"%(resolution, 10000)
            resolution = 10000
        elif resolution < 1000: #CHECK
            resolution = 10000 # CHECK 

    a_h = U.histogram(img, resolution, mmms[0], mmms[1])
    h = histogram(a_h, mmms[0], mmms[1], "hist 4: " + viewer.GetParent().GetTitle())
    def a(l,r):
        try:
            viewer.changeHistogramScaling(l,r)
        except:
            pass
    h.doOnBrace = a
    #v.changeHistogramScaling(mmms[0],mmms[1])
    h.setBraces(mmms[0],mmms[1])
    h.fitXcontrast()
    return h


def vview(img, title='', size=None):
    """old"""

    from viewer import view as view2d

    if img.dtype.type == N.float64:
        print 'view Float as float32'
        return vview(img.astype(N.float32), title, size)
    if img.dtype.type == N.int32:
        print 'view int32 as int16'
        return vview(img.astype(N.int16), title, size)
    if img.dtype.type in (N.complex64,N.complex128) :
        print 'view abs'
        return vview(N.absolute( img ), title, size)

    if len( img.shape ) == 2:
        from Priithon import seb as S
        amin, amax, amean, astddev = S.mmms(img)
        v = view2d(img, title, size)
        import wx
        wx.Yield()
        try:
            v.changeHistogramScaling(amin,amax)
        except:
            print "-Error changeHistogramScaling", amin, amax
        h = hist( v )
        v.hist = h
        return v
    elif len( img.shape ) == 3:
        v = vview(img[0], title)

        v.autoHistUpdate = 1
        h = v.hist
        s = ZSlider(img.shape[0], "zslider 4 " + title)
        def f(newZ):
            imgZ = img[newZ]
            v.setImage( imgZ )

            if v.autoHistUpdate:
                from Priithon import seb as S
                mmms = S.mmms( imgZ )
                resolution = int(mmms[1]-mmms[0]+2)
                if resolution > 10000:
                    #print "resolution (max-min = %d) limited to %d"%(resolution, 10000)
                    resolution = 10000
                elif resolution < 1000: #CHECK
                    resolution = 10000 # CHECK 

                a_h = U.histogram(imgZ, resolution, mmms[0], mmms[1])
                h.setHist(a_h, mmms[0], mmms[1])

        s.doOnZchange = f
        return v
        
    else:
        print " ** what should I do with data - shape=", img.shape


try:
    viewers
except:
    viewers=[]

from splitND import run as view
from splitND2 import run as view2


from DragAndDrop import DropFrame
from viewerRubberbandMode import viewerRubberbandMode as vROI

def vd(id=-1):
    """
    return data arr of viewer 'id'
    shortcut for: Y.viewers[id].data
    """
    v = viewers[id]
    return v.data

def vTransferFct(id=-1, execStr='', usingXX=True):
    """
    define custom transfer function:
    execStr is evaluted pixelwise
          (more precise: "vectorized" on all pixels (2d array) "in parallel")
    x : pixel value
    x0: left hist brace value ( as float(..) )
    x1: right hist brace value ( as float(..) )
    y:  result needs to get assigned to `y`

    string is evaluated in __main__ as globals
    empty evalStr deactivates custom transfer function (default)
    if result y is ndim 3 (col,y,x): y gets transposed to (y,x,rgb) and interpreted as RBG 

    if usingXX is True: `xx` can be used as shortcut for `N.clip((x-x0)/(x1-x0), 0, 1)`

    Examples:
    `y=N.clip((x-x0)/(x1-x0), 0, 1)`         #  equivalent to default
    `y=N.clip((x-x0)/(x1-x0))**.3, 0, 1)` # gamma value of .3

    NOTE: be care to not create errors ! 
      In case it happens, you will get error infinite messages,
      minimize window, and reset transfer functions quickly !!
    """
    
    vv = viewers[id].viewer
    vv.transferf = execStr
    vv.transferf_usingXX = usingXX
    #CHECK vv.colMap = None
    vv.m_imgChanged = True
    vv.Refresh(False)

def vTransferGamma(id=-1, gamma=.3):
    """
    set transfer function so that
    images gets displayed using given gamma value
    """
    if gamma == 1:
        vTransferFct(id, '')
    else:
        vTransferFct(id, 'y=N.clip(((x-x0)/(x1-x0))**%f, 0, 1)'%gamma, usingXX=False)


#  def viewfn(fn=''):
#   """open file fn memmapped and view it"""
#   if fn is None or fn == '':
#       fn = FN()
#   try:
#       import Mrc
#       a = Mrc.bindFile(fn)
#   except:
#       import sys
#       global _error, _error0  ## FIXME
#       _error0 = sys.exc_info()
#       _error = map(str, _error0)
#       print "*ERROR while opening file (see var _error)"
#       #self.window.WriteText("Error when opening: %s - %s" %\
#       #                      (str(e[0]), str(e[1]) ))
#   else:
#       view(a, '')


def vClose(id='all'):
    """
    close viewer with given id
    id can be a number, a sequence of numbers, or 'all'
    """
    if id is 'all':
        id  = range(len(viewers))
    elif type(id) == int:
        id = [id]

    for i in id:
        v = viewers[i]
        if v:
            wx.GetTopLevelParent(v.viewer).Close()

def vReload(id):
    """
    "reload" image data from memory into gfx card
    """
    v = viewers[id]
    vv = v.viewer
    vv.OnReload()


def vArrange(idxs=-1, nx=4, refSizeId=None, doCenter=1, x0=0, y0=0):
    """
    move viewer windows on screen to layout in order on a grid
    nx viewers per row (left to right)
    as many columns as needed
    """
    if idxs==-1:
        idxs = range(len(viewers))
    first = 1
    x,y = x0,y0
    ix,iy = 0,0
    hh=0
    if refSizeId != None:
        s = wx.GetTopLevelParent(viewers[refSizeId].viewer).GetSize()
    for i in idxs:
      try:  
        f = wx.GetTopLevelParent(viewers[i].viewer)
        f.SetPosition( (x,y) )
        if refSizeId != None:
            f.SetSize(s)
        if doCenter:
            wx.Yield()  # CHECK ... FIXME:  HistogramCanvas.OnSize: self.m_w <=0 or self.m_h <=0 170 -2
            viewers[i].viewer.center()
        #f.Raise()
        fl = f
        

        
        h = f.GetSize()[1]
        if hh< h:
            hh=h
        ix += 1
        if ix == nx:
            ix = 0
            x = 0
            iy+=1
            y += hh
        else:
            x += f.GetSize()[0]
      except:
        pass
    rrr = list(idxs)
    rrr.reverse()
    for i in rrr:
      try:
        f = wx.GetTopLevelParent(viewers[i].viewer)
        f.Raise()
      except:
        pass


def vHistSettings(id_src=-2, id_target=-1):
    """
    copy settings from one viewer (viewer2) to another
    """
    from Priithon import splitND
    from Priithon import splitND2
    #isinstance(v, splitND.spv)
    spvFrom=viewers[id_src]
    spvTo = viewers[id_target]

    if spvFrom.__class__ is spvTo.__class__ is splitND2.spv:

        #Y.clipboardSetText([i[4:9] for i in v.viewer.m_imgList], 1)

        #self.m_imgList = [] # each elem.:
        ## 0       1        2       3            4     5   6 7 8   9, 10,11, 12
        ##[gllist, enabled, imgArr, textureID, smin, smax, r,g,b,  tx,ty,rot,mag]

        #li = eval(Y.clipboardGetText().rstrip())
        for i,l in enumerate(spvFrom.viewer.m_imgList):
            spvTo.hist[i].m_sx, spvTo.hist[i].m_tx = spvFrom.hist[i].m_sx, spvFrom.hist[i].m_tx
            spvTo.hist[i].zoomChanged=True
            sss = spvFrom.hist_show[i]
            spvTo.hist_show[i] = sss
            spvTo.hist_toggleButton[i].SetValue( sss )
            spvTo.OnHistToggleButton(i=i)

            #vv.changeHistScale(i, l[0],l[1])
            spvTo.setColor(i, l[6:9], RefreshNow=False)
            spvTo.hist[i].setBraces(spvFrom.hist[i].leftBrace, spvFrom.hist[i].rightBrace)

        spvTo.viewer.Refresh(0)
        spvTo.viewer.GetParent().Refresh(0)

    elif spvFrom.__class__ is spvTo.__class__ is splitND.spv:
        vh = spvFrom.hist
        spvTo.hist.m_sx, spvTo.hist.m_tx = spvFrom.hist.m_sx, spvFrom.hist.m_tx
        spvTo.hist.zoomChanged=True
        amin,amax =  vh.leftBrace, vh.rightBrace
        #spvTo.hist.autoFit(None, amin, amax)
        spvTo.hist.setBraces(amin,amax)
        vColMap(id_target, spvFrom.viewer.colMap)

    else:
        raise ValueError, "src and target are different type viewers (%s vs. %s)" %(spvFrom.__class__, spvTo.__class__)

def vGetZSecTuple(id=-1):
    """
    return values of all z-sliders of a given viever as a tuple
    """
    return tuple(viewers[id].zsec)


def vShortcutAdd(id=-1, key=' ', func='Y.wx.Bell()', flags=wx.ACCEL_NORMAL):
    '''
    appends entry to AccelleratorTable of specified viewer

    key: keyCode (an int) or a char (implicit call of ord(key))
    
    flags: wx.ACCEL_NORMAL(0), wx.ACCEL_ALT(1),wx.ACCEL_CTRL(2)
    func: function (no args) to call on presseing shortcut key
         if type(func)== str: use exec func in __main__
    '''
    vv = viewers[id].viewer
    iii = wx.NewId()
    if type(key) != int:
        key = ord(key)
    if type(func) == str:
        def OnKey(ev):
            import __main__
            exec func in __main__.__dict__
    else:
        def OnKey(ev):
            func()
    vv.Bind(wx.EVT_MENU, OnKey, id=iii)
    vv.setAccels([(flags, key, iii)])

def vShortcutReset(id=-1):
    '''
    reset AccelleratorTable of specified viewer
    '''
    vv = viewers[id].viewer
    vv.setAccels(reset = True)
    
def vZoom(id, zoomfactor, absolute=True, refreshNow=True):
    """
    set new zoom factor to zoomfactor
    if absolute is False
    adjust current zoom factor to
    "current"*zoomfactor
    image center stays center 
    """
    v = viewers[id]
    vv = v.viewer
    vv.zoom(zoomfactor, absolute, refreshNow)
def vHistScale(id=-1, amin=None, amax=None, autoscale=True):# refreshNow=True):
    """
    set new intensity scaling values
    None mean lowest / highest intensity for min / max respectively
    autoscale: scale displayed range to new left and right braces
    """
    v = viewers[id]
    vh = v.hist
    vh.autoFit(None, amin, amax)

def vHistScaleGet(id=-1):
    """
    return current leftBrace and rightBrace values used in given viewer
    """

    v = viewers[id]
    vh = v.hist
    return vh.leftBrace, vh.rightBrace

def vHistScale2(id=-1, channel=None, amin=None, amax=None, autoscale=True):# refreshNow=True):
    """
    set new intensity scaling values for a view2 viewer
    if channel is None - set all channels - otherwise only the given channel
    amin, amax:
    None mean lowest / highest intensity for min / max respectively
    autoscale: scale displayed range to new left and right braces
    """
    v = viewers[id]
    if channel is None:
        for ch in range(v.nColors):
            vHistScale2(id=id, channel=ch, amin=amin, amax=amax, autoscale=autoscale)
        return

    vh = v.hist[channel]
    #CHECK
    #     if amin is None:
    #         amin = v.mmms[ch][0]
    #     if amax is None:
    #         amax = v.mmms[ch][1]
    #     vh.setBraces(amin,amax)
    vh.autoFit(None, amin, amax, autoscale)

def vHistScale2Get(id=-1, channel=None):
    """
    return current leftBrace and rightBrace values used in given viewer2 
    for the given channel; 
    if channel is None a list of tuples for all channels is returned
    """
    v = viewers[id]
    if channel is not None:
        vh = v.hist[channel]
        return vh.leftBrace, vh.rightBrace
    else:
        return [(vh.leftBrace, vh.rightBrace) for vh in v.hist]


def vColMap(id=-1, colmap="", reverse=0):
    """
    set color map for given viewer
    colmap should be a string; one of:
      ''   <no color map>
      log       log-scale
      minmaxgray (both mi or mm work)
      blackbody
      rainbow
      wheel
      wheel10  (last two characters are evals as number-of-cycles
      wheelXX  (last two characters are evals as number-of-cycles
      
      (only first two letters are checked)

    if colmap is a numpy array, the array is used directly as colmap
       it should be of shape (3, 256)
    """
    v = viewers[id].viewer
    if type(colmap) in (str,unicode):
        colmap = colmap.lower()
        if colmap == "":
            v.cmnone()
        elif   colmap.startswith("bl"):
            v.cmblackbody(reverse=reverse)
        elif colmap.startswith("ra"):
            v.cmcol(reverse=reverse)
        elif colmap.startswith("lo"):
            v.cmlog()
        elif colmap.startswith("mm") or colmap.startswith("mi"):
            v.cmGrayMinMax()
        elif colmap.startswith("wh"):
            try:
                cycles = int(colmap[-2:])
            except:
                cycles = 1
            v.cmwheel(cycles=cycles)
    elif isinstance(colmap, N.ndarray):
        #20080407  v.colMap = N.zeros(shape=(3, v.cm_size), dtype=N.float32)
        #20080407 v.colMap[:] = colmap
        v.colMap = colmap.copy()

        v.changeHistogramScaling()
        v.updateHistColMap()
# v.cmgray(gamma=1)
# v.cmgray(gamma=12)
# v.cmgray(gamma=.3)
# v.cmgrey(reverse=0)
# v.cmgrey(reverse=1)
# v.cms(colseq=['darkred', 'red', 'orange', 'yellow', 'green', 'blue', 'darkblue', 'violet'], reverse=0)
# v.cms(colseq=['darkred', 'red', 'orange', 'yellow', 'green', 'blue', 'darkblue', 'violet'], reverse=1)

def vSetSlider(id, z, zaxis=0, autoscale=False): #, refreshNow=False)
    """
    zaxis specifies "which" zaxis should moved to new value z
    """
    v = viewers[id]
    v.setSlider(z, zaxis)
    if autoscale:
        vScale(id)
def vSetAspectRatio(v_ids=[-1], y_over_x=1, refreshNow=1):
    '''
    strech images in y direction
    use negative value to mirror

    if v_ids is a scalar change only for that viewer, otherwise for all viewers in that list
    '''
    try:
        v_ids[0]
    except:
        v_ids = (v_ids,)
    for v_id in v_ids:
        vs=Y.viewers[v_id]
        vs.viewer.setAspectRatio(y_over_x, refreshNow)

def vCenter(id=-1, refreshNow=True):
    """
    move displayed image into center of 'visible' area of given viewer
    """
    v = viewers[id]
    vv = v.viewer
    vv.center(refreshNow)

def vReadRGBviewport(v_id=-1, flipY=1):
    """
    return returns array with r,g,b values from "what-you-see"
       shape(3, height, width)
       dtype=uint8

       v_id is either a number (the "viewer-ID")
               or a "viewer"-object
    """
    if type(v_id)  is int:
        v_id = viewers[v_id].viewer

    if flipY:
        return v_id.readGLviewport()[:, ::-1]
    else:
        return v_id.readGLviewport()
        
def vSaveRGBviewport(v_id, fn, clip=True, flipY=True):
    """
    save "what-you-see" into RGB file of type-given-by-filename

       v_id is either a number (the "viewer-ID")
               or a "viewer"-object
    """
    if type(v_id)  is int:
        v_id = viewers[v_id].viewer
    
    import useful as U
    a = v_id.readGLviewport(clip=clip, flipY=flipY, copy=True)

    U.saveImg(a, fn)

def vCopyToClipboard(v_id=-1, clip=True):
    """
    copies image as seen on screen into clipboard
    if clip is True, clip backgound
    """
    if type(v_id)  is int:
        v_id = viewers[v_id].viewer

    aa = v_id.readGLviewport(clip=clip, flipY=True, copy=0)

    im = wx.ImageFromData(nx,ny,aa.transpose((1,2,0)).tostring())
    bi=im.ConvertToBitmap()
    bida=wx.BitmapDataObject(bi)
    if not wx.TheClipboard.Open():
        raise RuntimeError, "cannot open clipboard"
    try:
        wx.TheClipboard.SetData(bida)
    finally:
        wx.TheClipboard.Close()

def vresizeto(refId=0, idxs=-1, nx=4):
    if idxs==-1:
        idxs = range(555)
    s = wx.GetTopLevelParent(viewers[refId].viewer).GetSize()
    
    for i in idxs:
      try:
        f = wx.GetTopLevelParent(viewers[i].viewer)
        #f.Raise()
        f.SetSize(s)
      except:
        pass
    rrr = list(idxs)
    rrr.reverse()
    for i in rrr:
      try:
        f = wx.GetTopLevelParent(viewers[i].viewer)
        f.Raise()
      except:
        pass

def vRotate(v_id, angle=None):
    """
    set displaying-rotation for viewer v_id
    if angle is None open slider GUI

    v_id is either a number (the "viewer-ID")
         or a "viewer"- or a "spv"-object
    """
    if type(v_id)  is int:
        spv = viewers[v_id]
    elif hasattr(v_id, "my_spv"):
        spv = v_id.my_spv
    else:
        spv=v_id
    
    if angle is not None:
        spv.viewer.setRotation(angle)
    else:
        viewerID = spv.id
        class _xx:
            pass
            def flip(self, x):
                self.v.m_aspectRatio *= -1
                self.v.m_y0 -= self.v.pic_ny * self.v.m_scale * self.v.m_aspectRatio
                #if x:
                #else:
                #    self.v.m_y0 -= self.v.pic_ny * self.m_scale * self.v.m_aspectRatio
                    
                self.v.m_zoomChanged=1
                self.v.Refresh(0)
                    
        xx = _xx()
        xx.v = spv.viewer
        xx.tc = 0 # text-change triggered event -- prevent calling circle when txt.SetValue() triggers text-change-event
        # note: first call of onText happend before sli is made
        buttonBox([
                ('c x.SetValue(v.m_aspectRatio<0)\tflip', "_.flip(x)", 0),
                ('l\tangle:', '', 0),
                ('t _.txt=x\t0',         "y=(len(x) or 0) and int(x);_.tc or (hasattr(_,'sli') and sli.SetValue(y));v.setRotation(y);_.tc=0", 0),
                ('sl _.sli=x\t0 0 360', "txt.SetValue(str(x));_.tc=1")],
                  title="rotate viewer %s"%(viewerID,),
                  execModule=xx)

def vzslider(idxs=None, nz=None, title=None):
    """
    show a "common slider" window
    for synchronous z-scrolling through multiple viewer
    idxs is list of indices
    if idxs is None, synchronize all open viewers
    if an index in idxs is given as tuple, it means (viewerID, zaxis)
    default is zaxis=0 otherwise
    """
    if idxs==None:
        idxs = [i for i in range(len(viewers)) if viewers[i] is not None]
    if title is None:
        title = "slide:" + str(idxs)

    if nz is None:
        nz=1
        for i in idxs:
            try:
                i,zaxis = i
            except:
                zaxis=0
            try:
                v = viewers[i]
                if v.zshape[zaxis] > nz:
                    nz = v.zshape[zaxis]
            except:
                pass
    def onz(z):
        for i in idxs:
            try:
                i,zaxis = i
            except:
                zaxis=0
            try:
                v = viewers[i]
                v.setSlider(z, zaxis)
            except:
                pass
    zs = ZSlider(nz, title)
    zs.doOnZchange = onz


def vClearGraphics(id):
    v = viewers[id]
    vv = v.viewer
    def ff0():
        pass
    vv.updateGlList( ff0 )
    vv.SetToolTipString('')


def vLeftClickMarks(id, callFn=None):
    def fg(x,y):
        glCross(int(x)+0.5, int(y)+0.5, length=50, color=(1,0,0))

    vLeftClickDoes(id, fg, callFn)


_plotprofile_avgSize=1


def vLeftClickHorizProfile(id, avgBandSize=1, s='-'):
    v = viewers[id]
    h,w = v.img.shape

    global _plotprofile_avgSize
    _plotprofile_avgSize = avgBandSize

    def f(x,y):
        if _plotprofile_avgSize >1:
            vals = N.sum( v.img[ y:y+_plotprofile_avgSize ].astype(N.float64), 0 ) / float(_plotprofile_avgSize)
            ploty( vals, s )
        else:
            ploty( v.img[ y ], s )
    def fg(x,y):
        if _plotprofile_avgSize >1:
            glLine(0,y,w,y, (1,0,0))
            glLine(0,y+_plotprofile_avgSize,w,y+_plotprofile_avgSize, (1,0,0))
        else:
            glLine(0,y+.5,w,y+.5, (1,0,0))

    vLeftClickDoes(id, callGlFn=fg, callFn=f)

def vLeftClickVertProfile(id, avgBandSize=1, s='-'):
    v = viewers[id]
    h,w = v.img.shape

    global _plotprofile_avgSize
    _plotprofile_avgSize = avgBandSize

    def f(x,y):
        if _plotprofile_avgSize >1:
            vals = N.sum( v.img[ :, x:x+_plotprofile_avgSize ].astype(N.float64), 1 ) / float(_plotprofile_avgSize)
            ploty( vals, s )
        else:
            ploty( v.img[ :, x ], s )
    def fg(x,y):
        if _plotprofile_avgSize >1:
            glLine(x,0,x,h, (1,0,0))
            glLine(x+_plotprofile_avgSize,0,x+_plotprofile_avgSize,h, (1,0,0))

        else:
            glLine(x+.5,0,x+.5,h, (1,0,0))

    vLeftClickDoes(id, callGlFn=fg, callFn=f)

def vLeftClickZProfile(id, avgBoxSize=1, s='-', slice=Ellipsis):
    v = viewers[id]

    data = v.data[slice]

    if data.ndim != 3:
        raise "ZProfile only works for 3D data (TODO: for 4+D)"
    nz = data.shape[0]

    global _plotprofile_avgSize # 20051025
    _plotprofile_avgSize = avgBoxSize # 20051025

     # 20051025 if avgBoxSize >1:
    v.polyLen = 2
    v.polyI = 0
    v.poly = N.zeros(2*v.polyLen, N.float64)
        
    def f(x,y):
        if _plotprofile_avgSize >1:
            w,h = _plotprofile_avgSize,_plotprofile_avgSize
            w2,h2 = w/2., h/2.
            v.poly[:] = x0,y0,x1,y1 = int(x-w2+.5),int(y-h2+.5),  int(x+w2+.5),int(y+h2+.5)
            from useful import mean2d
            prof = N.empty(shape=nz, dtype=N.float)
            for z in range(nz):
                prof[z] = data[z,  y0:y1, x0:x1].mean()
            #prof = mean2d(a[:,  y0:y1, x0:x1])   ##->  TypeError: Can't reshape non-contiguous numarray
            ploty( prof, s )
        else:
            ploty( data[ :, int(y), int(x) ], s )
    def fg(x,y):
        if _plotprofile_avgSize >1:
            x0,y0,x1,y1 = v.poly
            glBox(x0,y0,x1,y1, (1,0,0))
        else:
            glCross(int(x)+0.5, int(y)+0.5, length=50, color=(1,0,0))
    vLeftClickDoes(id, callGlFn=fg, callFn=f, roundCoords2int=(_plotprofile_avgSize==0))

def vLeftClickLineProfile(id, abscissa='line', s='-'):
    """abscissa can be
    'x'       to plot intensity along line against x-coordinate
    'y'       against y-coord
    else      against length
    """
    v = viewers[id]

    v.polyLen = 2
    v.polyI = 0
    v.poly = N.zeros(2*v.polyLen, N.float64)
    def f(x,y):
        v.poly[2*v.polyI : 2*v.polyI+2] = x,y # int(x) +.5, int(y) +.5
        v.polyI = (v.polyI+1) % v.polyLen

        x0,y0,x1,y1 = v.poly
        dx,dy = x1-x0, y1-y0

        l = N.sqrt(dx*dx + dy*dy)
        if l>1:
            ddx = dx/l
            ddy = dy/l
            #print dx,dy,l, x0,y0,x1,y1
            xs = map(int, N.arange(x0, x1, ddx)+.5)
            ys = map(int, N.arange(y0, y1, ddy)+.5)
            #print len(xs), len(ys)
            try:
                vs = v.img[ ys,xs ]
                if abscissa == 'x':
                    plotxy(xs, vs, s)
                elif abscissa == 'y':
                    plotxy(ys, vs, s)
                else:
                    ploty(vs, s)
            except:
                raise #print "line profile bug:", len(xs), len(ys)

        #print v.poly
        
    def fg(x,y):
        x0,y0,x1,y1 = v.poly
        glLine(x0,y0,x1,y1, (1,0,0))

    vLeftClickDoes(id, callGlFn=fg, callFn=f)







def vLeftClickLineMeasure(id, roundCoords2int=0):
    v = viewers[id]

    v.polyLen = 2
    v.polyI = 0
    v.poly = N.zeros(2*v.polyLen, N.float64)
    def f(x,y):
        v.poly[2*v.polyI : 2*v.polyI+2] = x,y # int(x) +.5, int(y) +.5
        v.polyI = (v.polyI+1) % v.polyLen

        x0,y0,x1,y1 = v.poly
        dx,dy = x1-x0, y1-y0

        s = "length: %s" % (N.sqrt(dx*dx+dy*dy), )
        print s
        v.viewer.SetToolTipString(s)
        
    def fg(x,y):
        x0,y0,x1,y1 = v.poly
        glLine(x0,y0,x1,y1, (1,0,0))

    vLeftClickDoes(id, callGlFn=fg, callFn=f,roundCoords2int=roundCoords2int)


def vLeftClickTriangleMeasure(id, roundCoords2int=0):
    v = viewers[id]

    v.polyLen = 3
    v.polyI = 0
    v.poly = N.zeros(2*v.polyLen, N.float64)
    def f(x,y):
        v.poly[2*v.polyI : 2*v.polyI+2] = x,y # int(x) +.5, int(y) +.5
        v.polyI = (v.polyI+1) % v.polyLen

        x0,y0,x1,y1,x2,y2 = v.poly
        dx21,dy21 = x1-x0, y1-y0
        dx31,dy31 = x2-x0, y2-y0
        dx32,dy32 = x2-x1, y2-y1

        a2,b2,c2 =  \
                 dx21**2 + dy21**2, \
                 dx31**2 + dy31**2, \
                 dx32**2 + dy32**2

        try:
            R = N.sqrt(        a2*b2*c2  / \
                                (-a2**2 + 2*a2*b2 - b2**2 + 2*a2*c2 + 2*b2*c2 - c2**2) \
                                )

            px,py = x0+dx21/2.  ,  y0+dy21/2.
            poLen = N.sqrt(1-b2/(4*R*R)) * R

            #nnx     = dx21
            #cx,cy 

        
            area = N.abs(dx21*dy31-dy21*dx31) / 2.

            if area > 0:
                a21 = x1*x1-x0*x0 + y1*y1-y0*y0
                a32 = x2*x2-x1*x1 + y2*y2-y1*y1         

                yyc = ( a21/(2.*dx21*dy21) - a32/(2.*dx32*dy21) ) \
                       / (1.-(dy32/dy21))

                yyc = .5 * ( a32/dx32 - a21/dx21 ) \
                         /( dy32/dx32 - dy21/dx21 )

                xxc = .5*a21/dx21 - yyc*dy21/dx21




                #print "area: %.2f   radius: %.2f    CX,CY: %5.1f %5.1f" % \
                #     (area, R,cx,cy)

                # s=    "outerCircle=> area: %.2f   radius: %.2f   diameter: %.2f" %      (area, R, 2*R)
                # s=    "outerCircle=> area: %.2f   r: %.2f  diameter: %.2f" %    (area, R, 2*R)
                s= "outerCircle=> cx,cy: %.1f %.1f   r: %.1f  diameter: %.1f" %       (xxc,yyc, R, 2*R)
            else:
                s= "outerCircle=> area: %.2f" % (area,)
            print s
            v.viewer.SetToolTipString(s)
        except ZeroDivisionError:
            pass
        
    def fg(x,y):
        x0,y0,x1,y1,x2,y2 = v.poly
        color=(1,0,0)
        #20050520 GL.glDisable(GL.GL_TEXTURE_2D)
        GL.glColor( color )
        GL.glBegin( GL.GL_LINE_LOOP )
        GL.glVertex2f( x0,y0 )
        GL.glVertex2f( x1,y1 )
        GL.glVertex2f( x2,y2 )
        GL.glEnd()
        #20050520 GL.glEnable( GL.GL_TEXTURE_2D)


    vLeftClickDoes(id, callGlFn=fg, callFn=f, roundCoords2int=roundCoords2int)













def vLeftClickBox(id, fixSize=None, roundCoords2int=1):
    """if fixSize is None:
          every click sets one corner (the opposite corner from last click)
       if    fixSize is   (width,height)-tuple
       or if fixSize is   scalar (box is square)
          every click sets center
    """
    v = viewers[id]
    h,w = v.img.shape

    v.polyLen = 2
    v.polyI = 0
    v.poly = N.zeros(2*v.polyLen, N.float64)
    def f(x,y):
        if fixSize is None:
            if roundCoords2int:
                x,y = int(x+.5), int(y+.5)
            v.poly[2*v.polyI : 2*v.polyI+2] = x,y # int(x) +.5, int(y) +.5
            v.polyI = (v.polyI+1) % v.polyLen

        else:
            try:
                w,h = fixSize
            except:
                w,h = fixSize,fixSize

            w2,h2 = w/2., h/2.
            if roundCoords2int:
                v.poly[:] = int(x-w2+.5),int(y-h2+.5),      int(x+w2+.5),int(y+h2+.5)
            else:
                v.poly[:] = x-w2,y-h2,      x+w2,y+h2

        
    def fg(x,y):
        x0,y0,x1,y1 = v.poly
        glBox(x0,y0,x1,y1, (1,0,0))

    vLeftClickDoes(id, callGlFn=fg, callFn=f, roundCoords2int=0)












def vLeftClickDoes(id, callGlFn=None, callFn=None, roundCoords2int=1):
    v = viewers[id]
    vv = v.viewer

    if callGlFn is None:
        def x(x,y):
            pass
        callGlFn = x

    def fff(x,y):
        if roundCoords2int:
            x = int(x)
            y = int(y)
        #20060726 v.data.x = x
        #20060726 v.data.y = y
        import numpy as N
        v.lastLeftClick_atYX = N.array((y,x)) #20060726 
        def ff0():
            callGlFn(x,y)
            
        if callFn is not None:
            callFn(x,y)
        vv.updateGlList( ff0)

    vv.doLDown = fff

def vLeftClickNone(id):
    #vLeftClickDoes(id,None,None)
    v = viewers[id]
    vv = v.viewer
    def x(x,y):
            pass
    vv.doLDown = x 





def vAddGraphics(id, fn): #, where=1):
    """ try e.g. fn=lambda:Y.glCircle(100,100)
    #   where:  1 - append
#          -1 - prepend
#          0  - remove old graphics

if fn is a list of functions each gets called

    Note: remember ... doesnt work in loop !?
    """
    v = viewers[id]
    vv = v.viewer

#   try:
#       n = len(fn)
#       fffn=fn
#       def fn():
#           for f in fffn:
#               f()
#   except:
#       pass

#   old_defGlList = vv.defGlList
#
#
#   if where == 1:
#       def ff0():
#           old_defGlList()
#           fn()
#   elif where == -1:
#       def ff0():
#           fn()
#           old_defGlList()
#   else:
#       def ff0():
#           fn()

    vv.addGlList( fn  )
    

# vFollowMouse: connect mouse pointer of XY-view with a 
#    "moving cross" in other XY or XZ views of same data set

# vFollowMouseReset: disconnect mouse pointer again

# vgMarkIn3D: place marker at 3D position, 
#      above and below markerZ show marker in different color 
#      default: green above (z+), red below (z-)
#      outside z +/- zPlusMinus: don't show marker at all - default: zPlusMinus=1000

try:  
    _vFollowMouse_orig_doOnMouse  
except: 
    _vFollowMouse_orig_doOnMouse = {}

def vFollowMouse(v_id, xyViewers=[], xzViewers=[], yzViewers=[],
                 zAxis=0, crossColor=(1,0,0), setSliderInXYviewers=True):
    '''
    if viewer v_id has more than one z-slider, 
       zAxis specifies which one to use for z coordinate in xzViewers

    TODO: yzViewers
    '''
    if not hasattr(xyViewers, '__len__'):
        xyViewers = [xyViewers]
    if not hasattr(xzViewers, '__len__'):
        xzViewers = [xzViewers]
    if not hasattr(yzViewers, '__len__'):
        yzViewers = [yzViewers]

    v = viewers[v_id]
    if not _vFollowMouse_orig_doOnMouse.has_key(v_id):
        oldDoOnMouse = v.viewer.doOnMouse
        _vFollowMouse_orig_doOnMouse[v_id] = oldDoOnMouse
    else:
        oldDoOnMouse = _vFollowMouse_orig_doOnMouse[v_id]
        
    last_X = [0]
    zAxisSliders=[]
    nx=v.data.shape[-1]
    ny=v.data.shape[-2]
    for vid in xzViewers:
        v1 = viewers[vid]
        try:
            zaxis = list(v1.zshape).index(nx)
        except ValueError:
            zaxis=None
        zAxisSliders.append(zaxis)

    xzViewers__zAxisSliders = zip(xzViewers, zAxisSliders)
    def onMouseFollower(x,y, a):
        last_X[0] = x
        z = v.zsec[zAxis]
        for vid in xyViewers:
           try:
               v1 = viewers[vid]
               vv = v1.viewer   
               def ff0():
                   #Y.glCross(x+.5, y+.5, length=10, color=crossColor)
                   glPlus(x+.5, y+.5, length=10, color=crossColor)
               vv.updateGlList(ff0, refreshNow=True)
           except AttributeError: # viewer might have been closed
               pass
        for vid,zslider in xzViewers__zAxisSliders:
           try:
               v1 = viewers[vid]
               vv = v1.viewer   
               def ff0():
                   glPlus(x+.5, z+.5, length=10, color=crossColor)
               vv.updateGlList(ff0, refreshNow=True)
               if zslider is not None and 0<= y < ny:
                   v1.setSlider(y,zslider)
           except AttributeError: # viewer might have been closed
               pass

        #TODO FIXME - if multiple viewers are "listed" only first one responds fast
        #         def refreshAll():
        #             for vid,zslider in xzViewers__zAxisSliders:
        #                 viewers[vid].viewer.Refresh(0)
        #             for vid in xyViewers:
        #                 viewers[vid].viewer.Refresh(0)
        #         import wx
        #         wx.CallAfter(refreshAll)
        oldDoOnMouse(x,y,a)
    def doNewSec(zTup):
        x = last_X[0]
        z = v.zsec[zAxis]
        if setSliderInXYviewers:
            for vid in xyViewers:
                v1 = viewers[vid]
                try:
                    v1.setSlider(z, zAxis)
                except:
                    pass
        for vid,zslider in xzViewers__zAxisSliders:
            try:
                v1 = viewers[vid]
                vv = v1.viewer   
                def ff0():
                    glPlus(x+.5, z+.5, length=10, color=crossColor)
                vv.updateGlList(ff0, refreshNow=True)
            except AttributeError: # viewer might have been closed
               pass
    v.doSecChanged = doNewSec
    v.viewer.doOnMouse = onMouseFollower

    
def vFollowMouseReset(v_id):
    v = viewers[v_id]
    if not _vFollowMouse_orig_doOnMouse.has_key(v_id):
        print "can't remember on nMouse handler... will set to <do nothing>"
        def ff(x,y,a):
            pass
        v.viewer.doOnMouse = ff
    else: 
       v.viewer.doOnMouse = _vFollowMouse_orig_doOnMouse[v_id]

    def doNewSec(zTup):
        pass
    v.doSecChanged = doNewSec


def vgMarkIn3D(v_id=-1, zyx = (None,200,200), kind='Cross', 
               s=4,
               zPlusMinus=9999,
               colAtZ   = (1,1,1),
               colLessZ = (1,0,0),
               colMoreZ = (0,1,0),
               widthAtZ   = 2,
               widthLessZ = 1,
               widthMoreZ = 1,
               name="mark3D",
               refreshNow=True
               ): # , zAxis = 0):
    '''
    kind is one of 'Cross', 'Circle', 'Box'

    zyx is 3-tuple: if z is None use current

    col: color
    AtZ    - in Z section at z
    LessZ  - in Z section smaller than z
    MoreZ  - in Z section larger than z

    zPlusMinus - how many sections above/below z should be marked (at most)
    '''
    v = viewers[v_id]
    
    nz = v.zshape[0]

    z,y,x = zyx
    yx=y,x

    z = int(z+.5)

    zShown = v.zsec[0]
    if z is None:
        z = zShown

    if kind.lower().startswith('ci'): 
        fffff=vgAddCircles
    if kind.lower().startswith('cr'): 
        fffff=vgAddCrosses
    if kind.lower().startswith('b'): 
        fffff=vgAddBoxes
        s *=.5

    z0 = z-zPlusMinus
    if z0<0:
        z0 = 0
    z1 = z+zPlusMinus
    if z1>nz:
        z1 = nz
    for i in range(z0,z):
        q=fffff(v_id, [yx], s, color=colLessZ, width=widthLessZ, 
                name=["markedIn3D", name,(i,)], idx=None, enable=i==zShown, refreshNow=False)

    for i in range(z+1,z1):
        q=fffff(v_id, [yx], s, color=colMoreZ, width=widthMoreZ, 
                name=["markedIn3D", name,(i,)], idx=None, enable=i==zShown, refreshNow=False)
        
    q=fffff(v_id, [yx], s, color=colAtZ, width=widthAtZ, 
            name=["markedIn3D", name,(z,)], idx=None, enable=z==zShown, refreshNow=refreshNow)











def vm(id):
    """return mountain viewer window of id"""
    return viewers[id].m
def vmScale(id, zscale):
    """scale mountain viewer window of id"""
    return viewers[id].m.setZScale(zscale)



from OpenGL import GL
# def glTex2Don():
#   pass# #20050520 GL.glEnable( GL.GL_TEXTURE_2D)
# def glTex2Doff():
#   pass# #20050520 GL.glDisable(GL.GL_TEXTURE_2D)
def glCross(x0,y0, length=50, color=None):
    if color is not None:
        GL.glColor( color )
    GL.glBegin( GL.GL_LINES )
    GL.glVertex2f( x0-length,y0-length )
    GL.glVertex2f( x0+length,y0+length )
    GL.glVertex2f( x0-length,y0+length )
    GL.glVertex2f( x0+length,y0-length )
    GL.glEnd()
def glPlus(x0,y0, length=50, color=None):
    if color is not None:
        GL.glColor( color )
    GL.glBegin( GL.GL_LINES )
    GL.glVertex2f( x0-length,y0 )
    GL.glVertex2f( x0+length,y0 )
    GL.glVertex2f( x0,y0-length )
    GL.glVertex2f( x0,y0+length )
    GL.glEnd()
def glLine(x0,y0,x1,y1, color=None):
    if color is not None:
        GL.glColor( color )
    GL.glBegin( GL.GL_LINES )
    GL.glVertex2f( x0,y0 )
    GL.glVertex2f( x1,y1 )
    GL.glEnd()

def glLineYxDyx(yx0,dyx, color=None):
    if color is not None:
        GL.glColor( color )
    GL.glBegin( GL.GL_LINES )
    GL.glVertex2f( yx0[1], yx0[0] )
    GL.glVertex2f( yx0[1]+dyx[1], yx0[0]+dyx[0] )
    GL.glEnd()

def glBox(x0,y0,x1,y1, color=None):
    if color is not None:
        GL.glColor( color )
    GL.glBegin( GL.GL_LINE_LOOP )
    GL.glVertex2f( x0,y0 )
    GL.glVertex2f( x0,y1 )
    GL.glVertex2f( x1,y1 )
    GL.glVertex2f( x1,y0 )
    GL.glEnd()

def glCircle(x0,y0,r=10, nEdges=60, color=None):
    if color is not None:
        GL.glColor( color )
    ps = map(lambda a: (x0+r*N.cos(a),
                   y0+r*N.sin(a)), N.arange(0,2*N.pi, 2*N.pi/nEdges))
    GL.glBegin( GL.GL_LINE_LOOP )
    for x,y in ps:
        GL.glVertex2f( x,y )
    GL.glEnd()

def glEllipse(x0,y0,rx=10, ry=5, phi=0, nEdges=60, color=None):
    if color is not None:
        GL.glColor( color )
    ps = map(lambda a: (x0+rx*N.cos(a),
                   y0+ry*N.sin(a)), N.arange(phi,phi+2*N.pi, 2*N.pi/nEdges))
    GL.glBegin( GL.GL_LINE_LOOP )
    for x,y in ps:
        GL.glVertex2f( x,y )
    GL.glEnd()

#  except:
#   print " * trouble with OpenGL stuff"
#   import traceback
#   traceback.print_exc()

def glutText(str, posXYZ=None, size=None, mono=0, color=None, enableLineSmooth=False):
    """
    use GLUT to draw some text
    font type GLUT_STROKE_ROMAN      ( == 0) -> mono=0
    font type GLUT_STROKE_MONO_ROMAN ( == 1) -> mono=1
    if posXYZ is not None: posXYZ is EITHER (x,y) OR (x,y,z)
    if size is not None: set size scale (EITHER scalar, (sx,sy) or (sx,sy,sz)
       [GLUT stroke font size of 1 is 100 "pixels" high for the letter `A`]

    if color is not None: call glColor3f(color)
    if enableLineSmooth  bracket code with glEnable/glDisable GL_LINE_SMOOTH

    # GLUT_STROKE_ROMAN
    #         A proportionally spaced  Roman  Simplex  font  for
    #         ASCII  characters  32 through 127. The maximum top
    #         character in the font is 119.05 units; the  bottom
    #         descends 33.33 units.
    # GLUT_STROKE_MONO_ROMAN
    #         A  mono-spaced  spaced  Roman  Simplex  font (same
    #         characters as GLUT_STROKE_ROMAN) for ASCII charac-
    #         ters  32 through 127. The maximum top character in
    #         the font is  119.05  units;  the  bottom  descends
    #         33.33  units. Each character is 104.76 units wide.
    """
    from OpenGL import GLUT
    if posXYZ is not None:
        try:
            x,y,z = posXYZ
        except:
            x,y = posXYZ
            z=0
    if color is not None:
        GL.glColor3fv( color )
    if enableLineSmooth:
        GL.glEnable(GL.GL_LINE_SMOOTH)
    GL.glPushMatrix()
    if posXYZ is not None:
        GL.glTranslatef(x, y, z)
    if size is not None:
        import numpy as N
        if N.isscalar(size): # type(size) == type(1) or type(size) == type(1.0):
            GL.glScale(size,size,size)
        elif len(size) == 2:
            GL.glScale(size[0],size[1],1)
        else:
            GL.glScale(size[0],size[1],size[2])
            
    for letter in str:
        GLUT.glutStrokeCharacter(mono, ord(letter))
    GL.glPopMatrix()
    if enableLineSmooth:
        GL.glDisable(GL.GL_LINE_SMOOTH)

def crust(showLinesNumbers=True, wrapLongLines=True):
    """open a new pyCrust terminal.
    this combines a shell with an inspect panel (and more)
    """
    #20070715 from wx import py
    import py # from Priithon
    f = py.crust.CrustFrame()
    #20070715(this somehow disappeared from editwindow.py) f.shell.setDisplayLineNumbers(showLinesNumbers)
    f.shell.wrap(wrapLongLines)
    f.Show(1)

def shell(showLinesNumbers=True, wrapLongLines=True):
    """open a new pyShell terminal.
    """
    #20070715 from wx import py
    import py # from Priithon
    f = py.shell.ShellFrame()
    #20070715(this somehow disappeared from editwindow.py)     f.shell.setDisplayLineNumbers(showLinesNumbers)
    f.shell.wrap(wrapLongLines)

    f.Show(1)

def inspect(what=None):
    """
    open a new pyFilling window.
    this is what you want to investigate all the variables, modules,
    and more
    
    if what is None: defautls to `locals()` in `__main__` (i.e. `__main__.__dict__`)
    """
    import py # from Priithon

    if what is None:
        import __main__
        what = __main__
    #     import sys
    #     fr = sys._getframe(1)
    #     #print dir(fr)
    #     # fc = fr.f_code
    #     locs = fr.f_globals
    #     #print locs.keys()

    try:
        whatLabel=what.__name__
    except AttributeError:
        try:
            whatLabel=['__name__']
        except:
            whatLabel=None
    title = 'Inspect: %s'%whatLabel

    c = py.filling.FillingFrame(parent=None, id=-1,
                            title=title,
                            #####pos=wx.wxPoint(-1, -1),
                            #pos=wx.wxPoint(680, 0),
                            ######size=wx.wxSize(-1, -1),
                            #size=wx.wxSize(600, 1000),
                            #style=541068864,
                            rootObject=what, rootLabel=whatLabel,
                            rootIsNamespace=False,
                            static=False)
    c.Show(1)
    

def shellMessage(msg):
    '''
    write a message into (main) shell window - or into terminal if no wx shell exists

    msg should end on r'\\n'
    '''
    import __main__
    try:
        __main__.shell.InsertText(__main__.shell.promptPosStart, msg)
        __main__.shell.promptPosStart += len(msg)
        __main__.shell.promptPosEnd += len(msg)
    except:
        print msg ,# in case there is no main.shell

def assignNdArrToVarname(arr, arrTxt):
    v = wx.GetTextFromUser("assign %dd-data to varname:"%arr.ndim, 'new variable')
    if v=='':
        return
    import __main__
    try:
        exec('__main__.%s = arr' % v)
    except:
        import sys
        e = sys.exc_info()
        wx.MessageBox("Error when assigning data to __main__.%s: %s - %s" %\
                      (v, str(e[0]), str(e[1]) ),
                      "Bad Varname  !?",
                      style=wx.ICON_ERROR)
    else:
        shellMessage("### %s = %s\n"% (v, arrTxt))




def ColourDialog():
    #global dlg
    frame = None # shell.GetParent()
    dlg = wx.ColourDialog(frame)
    #dlg.GetColourData().SetChooseFull(True) #only windows, but default anyway
    if dlg.ShowModal() == wx.ID_OK:
        data = dlg.GetColourData()
    else:
        data = None
    dlg.Destroy()
    #print 'You selected: %s\n' % str(data.GetColour().Get()))
    if data is None:
        return None
    return data.GetColour().Get()



def clipboardGetText():
    '''
    read out system clipboard
    and return string if there was some text to get
    returns None if no text available
    '''
    # inspired by http://wiki.wxpython.org/ClipBoard

    do = wx.TextDataObject()
    if not wx.TheClipboard.Open():
        raise RuntimeError, "cannot open clipboard"
    try:
        success = wx.TheClipboard.GetData(do)
    finally:
        wx.TheClipboard.Close()
    if success:
        return do.GetText()
    else:
        return None
def clipboardSetText(obj, useRepr=False):
    '''
    write text into system clipboard

    if useRepr:  converts any obj into text using repr()
    '''
    # inspired by http://wiki.wxpython.org/ClipBoard

    if useRepr:
        obj = repr(obj)
    do = wx.TextDataObject()
    do.SetText(obj)
    if not wx.TheClipboard.Open():
        raise RuntimeError, "cannot open clipboard"
    try:
        wx.TheClipboard.SetData(do)
    finally:
        wx.TheClipboard.Close()

def clipboardImageSaveToFile(fn=None):
    '''
    save a bitmap currently in the clipboard to an image file
    if fn is None: uses FN()
    '''
    if not wx.TheClipboard.Open():
        raise RuntimeError, "cannot open clipboard"
    try:
        if not wx.TheClipboard.IsSupported(wx.DataFormat(wx.DF_BITMAP)):
            raise RuntimeError, "no bitmap in clipboard"

        if fn is None:
            fn = FN(save=1)
        if not fn:
            return
        do = wx.BitmapDataObject()
        wx.TheClipboard.GetData(do)
        bmp = do.GetBitmap()

        # FIXME should vbe a function in wxPython = but which ?
        if   fn[-4:].lower() == '.png':
            typ = wx.BITMAP_TYPE_PNG
        elif fn[-4:].lower() == '.jpg':
            typ = wx.BITMAP_TYPE_JPEG
        elif fn[-4:].lower() == '.bmp':
            typ = wx.BITMAP_TYPE_BMP
        elif fn[-4:].lower() == '.tif':
            typ = wx.BITMAP_TYPE_TIFF
        elif fn[-4:].lower() == '.gif':
            typ = wx.BITMAP_TYPE_GIF
        else:
            raise ValueError, "Unknow file extention"

        bmp.SaveFile(fn, typ) #, wx.BITMAP_TYPE_PNG
    finally:
        wx.TheClipboard.Close()


try:
 def vtkInit():
    import sys

    p1 = '/jws18/haase/VTK-4.2-20040703/VTK/Wrapping/Python'
    p2 = '/jws18/haase/VTK-4.2-20040703/VTK/bin'
    if not p1 in sys.path:
        sys.path.append(p1)
        sys.path.append(p2)

 def vtkWxDemoCone(resolution=8):
    vtkInit()
        
    import wx, vtkpython

    #A simple VTK widget for wxPython.  Note that wxPython comes
    #with its own wxVTKRenderWindow in wxPython.lib.vtk.  Try both
    #and see which one works better for you.
    from vtk.wx.wxVTKRenderWindow import wxVTKRenderWindow


    # create the widget
    frame = wx.Frame(None, -1, "wxRenderWindow", size=wx.Size(400,400))
    widget = wxVTKRenderWindow(frame, -1)
    
    ren = vtkpython.vtkRenderer()
    widget.GetRenderWindow().AddRenderer(ren)

    cone = vtkpython.vtkConeSource()
    cone.SetResolution( resolution )
    
    coneMapper = vtkpython.vtkPolyDataMapper()
    coneMapper.SetInput(cone.GetOutput())
    
    coneActor = vtkpython.vtkActor()
    coneActor.SetMapper(coneMapper)

    ren.AddActor(coneActor)

    # show the window
    
    frame.Show(1)

 class vtkMountain:
    
    def __init__(self, arr2d, title="wxRenderWindow"):
        self.arr2d = arr2d


        try:
            import vtk
        except:
            vtkInit()
            import vtk
            

        #from vtk.wx.wxVTKRenderWindow import wxVTKRenderWindow
        #from vtk import vtkImageImport

        #global f, w, ren, ii, h,w, mi,ma,  geom,warp, mapper, carpet, _vtktypedict 

        self._vtktypedict = {N.uint8:vtk.VTK_UNSIGNED_CHAR,
                        N.uint16:vtk.VTK_UNSIGNED_SHORT,
                        N.uint32:vtk.VTK_UNSIGNED_INT,
                        N.int8:vtk.VTK_CHAR,
                        N.int16:vtk.VTK_SHORT,
                        N.int32:vtk.VTK_INT,
                        #N.int32:vtk.VTK_LONG,
                        #N.uint8:vtk.VTK_FLOAT,
                        #N.uint8:vtk.VTK_DOUBLE,
                        N.float32:vtk.VTK_FLOAT,
                        N.float64:vtk.VTK_DOUBLE }



        from vtk.wx.wxVTKRenderWindow import wxVTKRenderWindow
        from vtk import vtkImageImport

        self.f = wx.Frame(None, -1, title, size=wx.Size(400,400))
        self.w = wxVTKRenderWindow(self.f, -1)
        self.ren = vtk.vtkRenderer()
        self.w.GetRenderWindow().AddRenderer(self.ren)

        self.ii = vtkImageImport()

        #size = len(a.flat)  * a.itemsize()
        #ii.SetImportVoidPointer(a.flat, size)
        ####use tostring instead    self.ii.SetImportVoidPointer(arr2d._data, len(arr2d._data))
        self.ii.SetImportVoidPointer(arr2d._data, len(arr2d._data))
        self.ii.SetDataScalarType( self._vtktypedict[arr2d.dtype]) 
    
        h,w = arr2d.shape[-2:]
        self.ii.SetDataExtent (0,w-1, 0,h-1, 0,0)
        self.ii.SetWholeExtent(0,w-1, 0,h-1, 0,0)
        import useful as U
        self.mi,self.ma = U.mm( arr2d )
        
        
        self.geom = vtk.vtkImageDataGeometryFilter()
        self.geom.SetInput(self.ii.GetOutput())
        self.warp = vtk.vtkWarpScalar()
        self.warp.SetInput(self.geom.GetOutput())
        self.mapper = vtk.vtkPolyDataMapper()
        self.mapper.SetInput(self.warp.GetPolyDataOutput())
        self.carpet = vtk.vtkActor()
        self.carpet.SetMapper(self.mapper)
        self.carpet.SetScale(1,1, 50)

        
        self.mapper.SetScalarRange(self.mi,self.ma)
        self.ren.AddActor(self.carpet)
    
    def setZScale(self, zscale):
        self.carpet.SetScale(1,1, zscale)
        self.w.Refresh()
        
except:
    import sys
    global exc_info
    exc_info = sys.exc_info()
    #import traceback
    #traceback.print_exc()
    print "* no VTK *"
    pass


# ===========================================================================A
# ===========================================================================A
# line graphics
# ===================
# ===========================================================================A
# implicitly adjusts all coordinates yx  by .5,.5
#      so that a cross would go through the center of pixel yx
#
# ===========================================================================A
#
# if name is not None: add this to a named gfx-list
# if idx is not None: reuse/overwrite existing gfx entry 

# width is open-GL LineWidth
# color is rgb-tuple for color
# if refreshNow: call Refresh(0)  when done

# ===========================================================================A
# function definition uses hand-made "templating" 
#  all function have this scheme
# def vgAdd...(id, .... color=(1,0,0), width=1, name=None, idx=None, enable=True, refreshNow=True):
#     """
#     viewer line graphics - returns GLList index(idx)

#     ...
#     """
#     from OpenGL import GL
#     if type(id) is int:
#         v = viewers[id].viewer
#     else:
#         v=id
#     v.newGLListNow(name,idx)
#     try:
#         GL.glLineWidth(width)
#         GL.glColor( color )
    
#         ....
#     except:
#         import traceback
#         traceback.print_exc() #limit=None, file=None)
#         v.newGLListAbort()
#     else:
#         return v.newGLListDone(enable, refreshNow)

def _define_vgAddXXX(addWhat, extraArgs, extraDoc, extraCode):
    exec '''
def vgAdd%(addWhat)s  (id, %(extraArgs)s 
                       color=(1,0,0), width=1, name=None, idx=None, enable=True, refreshNow=True):
    """
    viewer line graphics - returns GLList index(idx)

    %(extraDoc)s
    """
    from OpenGL import GL
    if type(id) is int:
        v = viewers[id].viewer
    else:
        v=id
    v.newGLListNow(name,idx)
    try:
        GL.glLineWidth(width)
        GL.glColor( color )
        GL.glBlendFunc(GL.GL_ONE, GL.GL_ZERO)
  
        %(extraCode)s
        GL.glBlendFunc(GL.GL_ONE, GL.GL_ONE)
    except:
        import traceback
        traceback.print_exc() #limit=None, file=None)
        v.newGLListAbort()
    else:
        return v.newGLListDone(enable, refreshNow)
''' % locals() in globals()

# vgAddBoxes
# vgAddCircles
# vgAddEllipses
# vgAddCrosses
# vgAddArrows
# vgAddArrowsDelta
# vgAddLineStrip
# vgAddLines
# vgAddRectFilled
# vgAddRect
# vgAddTexts


_define_vgAddXXX('Crosses', 
                 extraArgs='ps, l=4,',
                 extraDoc='''ps is a point list of Y-X tuples  OR
       an entry might contain a third value used as l for that point
    l is the (default) length of the crosses''',
                 extraCode='''for yx in ps:
            y,x = yx[:2]
            if len(yx)>2:
                ll = yx[2]
            else:
                ll=l
            glCross(x+.5,y+.5, ll)
''')

_define_vgAddXXX('Boxes', 
                 extraArgs='ps, l=4,',
                 extraDoc='''ps is a point list of Y-X tuples  OR
       an entry might contain a third value used as l for that point
    l is the (default) half-length of the boxes''',
                 extraCode='''for yx in ps:
            y,x = yx[:2]
            if len(yx)>2:
                ll = yx[2]
            else:
                ll=l
            # old     #20051117 CHECK if boxing bottom-left corner of pixel makes sense
            # (corner!!-)points is ps are _enclosed_ (xy0-.5-l .. xy1+.5+l)
            # --> use -.5 < l < 0 for boxes smaller than 1 pixel

            ll = (ll-1) / 2.  # 20051117  # l=1 means box sidelength 1
            # 20051117 now: box goes around _center_ of pixel at x,y
            glBox(x-ll,y-ll, x+ll+1,y+ll+1)
''')
_define_vgAddXXX('Circles', 
                 extraArgs='ps, r=4, nEdges=20,',
                 extraDoc='''    ps is a point list of Y-X tuples  (circle centers) OR
       an entry might contain a third value used as r for that point
    r is the (default) radius of the circles
 ''',
                 extraCode='''for yx in ps:
            y,x = yx[:2]
            if len(yx)>2:
                rr = yx[2]
            else:
                rr=r
            glCircle(x+.5,y+.5, r, nEdges)
''')
_define_vgAddXXX('Ellipses', 
                 extraArgs='ps, nEdges=20,',
                 extraDoc='''    ps is a point list of tuples (circle centers, radius)
Y-X-R  or Y-X-RY-RX or Y-X-RY-RX-PHI
 ''',
                 extraCode='''for yx in ps:
            y,x = yx[:2]
            ry=yx[2]
            if len(yx)>3:
                rx = yx[3]
            else:
                rx=ry
            if len(yx)>4:
                phi = yx[4]
            else:
                phi=0
            glEllipse(x+.5,y+.5, rx, ry, phi, nEdges=nEdges)
''')
_define_vgAddXXX('Arrows', 
                 extraArgs='ps, qs, factor=1,',
                 extraDoc='''    ps is a point list of Y-X tuples
    qs is a point list of Y-X tuples
    lines are being drawn from a point in ps to the corresponding
    point in qs
    factor  'stretches' the lines "beyond" the b-point
 ''',
                 extraCode='''for yx0,b in zip(ps,qs):
            dyx = b-yx0
            glLineYxDyx(yx0+.5, dyx*factor)
''')
_define_vgAddXXX('ArrowsDelta', 
                 extraArgs='ps, ds, factor=1,',
                 extraDoc='''    ps is a point list of Y-X tuples
    ds is a point list of delta Y-X tuples
    lines are being drawn from a point in ps to the corresponding
    point at p + delta
    factor  'stretches' the lines "beyond" the arrow-end
 ''',
                 extraCode='''for yx0,dyx in zip(ps,ds):
            glLineYxDyx(yx0+.5, dyx*factor)
''')
_define_vgAddXXX('LineStrip', 
                 extraArgs='ps, ',
                 extraDoc='''    ps is a point list of Y-X tuples
    lines are being drawn connecting all points in as from the first to
    the last
 ''',
                 extraCode='''GL.glBegin(GL.GL_LINE_STRIP);
        for yx in ps:
            GL.glVertex2f( yx[1]+.5,yx[0]+.5 )
        GL.glEnd()
''')
_define_vgAddXXX('Lines', 
                 extraArgs='ps, ',
                 extraDoc='''    ps is a point list of Y-X tuples
    lines are being drawn connecting all points in ps; o--o o--o ...
 ''',
                 extraCode='''GL.glBegin(GL.GL_LINES);
        for yx in ps:
            GL.glVertex2f( yx[1]+.5,yx[0]+.5 )
        GL.glEnd()
''')

_rectCode='''
        y0,x0 = ps[0]
        y1,x1 = ps[1]
        if y0>y1:
            y0,y1 = y1,y0
        if x0>x1:
            x0,x1 = x1,x0
        if enclose:
            #20071212 CHECK x0 -=.5
            #20071212 CHECK y0 -=.5
            #20071212 CHECK x1 +=.5
            #20071212 CHECK y1 +=.5
            x1 +=1.
            y1 +=1.
        GL.glVertex2f( x0,y0 )
        GL.glVertex2f( x1,y0 )
        GL.glVertex2f( x1,y1 )
        GL.glVertex2f( x0,y1 )
        GL.glEnd()
'''
_define_vgAddXXX('RectFilled', 
                 extraArgs='ps, enclose=False, ',
                 extraDoc='''    ps is a pair of Y-X tuples
    if enclose: boxes are enlarged by .5 in each direction(CHECK!)
 ''',
                 extraCode='''GL.glBegin(GL.GL_POLYGON);'''+_rectCode
)
_define_vgAddXXX('Rect', 
                 extraArgs='ps, enclose=False, ',
                 extraDoc='''    ps is a pair of Y-X tuples
    if enclose: boxes are enlarged by .5 in each direction(CHECK!)
 ''',
                 extraCode='''GL.glBegin(GL.GL_LINE_LOOP);'''+_rectCode
)
_define_vgAddXXX('Texts', 
                 extraArgs='ps, size=.1, mono=False, ',
                 extraDoc='''    ps is a point list of Y-X-text tuples
    size, mono is for Y.glutText
    [GLUT stroke font size of 1 is 100 "pixels" high for the letter `A`]
 ''',
                 extraCode='''
        for yxt in ps:
            y,x,text = yxt
            glutText(str(text), posXYZ=(x,y), size=size, mono=mono, color=color, enableLineSmooth=False)
''')
    
def vgRemove(id=-1, idx=-1):
    """
    viewer line graphics -

    remove GLList index idx
    """
    if type(id) is int:
        v = viewers[id].viewer
    else:
        v=id
    v.newGLListRemove(idx)

def vgEnabledMaster(id=-1):
    """
    viewer line graphics -

    return if master-enable is on or off (for all GLLists)
    """
    if type(id) is int:
        v = viewers[id].viewer
    else:
        v=id
    return v.m_moreMaster_enabled

def vgEnableMaster(id=-1, on=1, refreshNow=True):
    """
    viewer line graphics -

    dis-/enable all GLList
    """
    if type(id) is int:
        v = viewers[id].viewer
    else:
        v=id
    v.m_moreMaster_enabled = on
    
    if refreshNow:
        v.Refresh(0)

def vgEnable(id=-1, idx=-1, on=1):
    """
    viewer line graphics -

    disable GLList index idx
    """
    if type(id) is int:
        v = viewers[id].viewer
    else:
        v=id
    if type(idx) in (tuple, list):
        for i in idx:
            v.newGLListEnable(i, on)
    else:
        v.newGLListEnable(idx, on)

def vgEnabled(id=-1, idx=-1):
    """
    viewer line graphics -

    return if GLList index idx is enabled
    """
    if type(id) is int:
        v = viewers[id].viewer
    else:
        v=id

    return v.m_moreGlLists_enabled[idx]

def vgNameEnable(id=-1, name='', on=True, refreshNow=True):
    '''
    en-/dis-able all 'viewer line graphics' with given name
    '''
    
    if type(id) is int:
        v = viewers[id].viewer
    else:
        v=id

    v.newGLListEnableByName(name, on, refreshNow)

def vgNameRemove(id=-1, name='', refreshNow=True):
    '''
    remove all 'viewer line graphics' with given name
    '''
    
    if type(id) is int:
        v = viewers[id].viewer
    else:
        v=id

    v.newGLListRemoveByName(name, refreshNow)

def vgRemoveAll(id=-1, refreshNow=True):
    """
    viewer line graphics -

    this really removes(!) all line graphics (GLList) stuff
    idx values will restart at 0
    here nothing gets "only" set to None
    """
    if type(id) is int:
        v = viewers[id].viewer
    else:
        v=id
    v.newGLListRemoveAll(refreshNow)
# ===========================================================================A

try:
    _vDrawing_orig_doOnMouse
except:
    _vDrawing_orig_doOnMouse = {}

def vDrawingReset(v_id):
    v = viewers[v_id]
    if not _vDrawing_orig_doOnMouse.has_key(v_id):
        print "can't remember on nMouse handler... will set to <do nothing>"
        def ff(x,y,a):
            pass
        v.viewer.doOnMouse = ff
    else: 
       v.viewer.doOnMouse = _vDrawing_orig_doOnMouse[v_id]


def vDrawingCircles(v_id=-1, 
                    allZsecs=False,
                    channel=None,  r=10, val = 1, add=False):
    """
    if allZsecs:
        drawing fills all z sections the same
    else:
        draw only into current z-sec

    use channel != None for drawing into that channel of a viewer2 window
    otherwise all channels will be drawn in the same (viewer2 only)

    if add: add value is used as multiplier and then added to image,  
    otherwise image is substituted where brush>0 
    """
    import fftfuncs as F

    v = viewers[v_id]
    if not _vDrawing_orig_doOnMouse.has_key(v_id):
        oldDoOnMouse = v.viewer.doOnMouse
        _vDrawing_orig_doOnMouse[v_id] = oldDoOnMouse
    else:
        oldDoOnMouse = _vDrawing_orig_doOnMouse[v_id]

    from splitND import spv as spv_class
    #from splitND2 import spv as spv2_class
    

    if isinstance(v, spv_class):
        def rel():
            #v.OnReload()
            v.helpNewData(self, doAutoscale=False, setupHistArr=True)
    else:
        def rel():
            v.helpNewData(doAutoscale=False, setupHistArr=True)
        
    def onMouseDraw(x,y, xyval):
        if v.viewer._onMouseEvt.LeftIsDown():
            a = v.data
            if not allZsecs:
                a = a[tuple(v.zsec)]
            if channel is not None:
                a = a[...,channel,:,:]

            brush2D_unity = F.discArr(a.shape[-2:], r, (y,x))

            if add:
                a += brush2D_unity * val
            else:
                for zsec in N.ndindex(a.shape[:-2]):
                    a[zsec] = N.where(brush2D_unity, val, a[zsec])

            rel()
        oldDoOnMouse(x,y,xyval)

    v.viewer.doOnMouse = onMouseDraw

    
