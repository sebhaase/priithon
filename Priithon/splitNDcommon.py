"""
the container of
(2d) viewer, histogram and "z"-slider

common base class for single-color and multi-color version
"""
from __future__ import absolute_import
__author__  = "Sebastian Haase <haase@msg.ucsf.edu>"
__license__ = "BSD license - see LICENSE file"

import wx
import numpy as N
from . import fftfuncs as F  # for mockNDarray, fft2d,...
import weakref
from . import PriConfig

##thrd   import  threading
##thrd   ccc=0
##thrd   workerInterval = 1000 # 500 #msec
##thrd   # Define notification event for thread completion
##thrd   EVT_RESULT_ID = wx.NewId()

Menu_AutoHistSec0 = 3310
Menu_AutoHistSec1 = 3311
Menu_AutoHistSec2 = 3312

Menu_WheelWhatMenu = 2013
Menu_ScrollIncrementMenu = 1013 ## scrollIncrL
scrollIncrL= [ 1,2,3,5,6,10,20,30,50,60,100,200,"..." ]

Menu_LeftClickMenu = 1070
Menu_SaveND   = wx.NewId()
Menu_AssignND = wx.NewId()



class spvCommon:
    """
    "split panel viewer"
    """
    def __init__(self):
        self.doOnSecChanged = [] # (zTuple, self)
        self.showFloatCoordsWhenZoomingIn = PriConfig.viewerShowFloatCoordsWhenZoomingIn
        self.keyShortcutTable = {}

        
    def doScroll(self, axis, dir):
        """ dir is -1 OR +1
        """
        if self.zndim < 1:
            return
        force1Incr = False
        if axis >= self.zndim:
            axis = self.zndim-1
            force1Incr = True
            
        zz = self.zsec[axis]
        if axis != 0 or force1Incr:
            zz += dir
            if dir < 0:
                if zz <0:
                    zz = self.zshape[axis]-1
            else:
                if zz >=self.zshape[axis]:
                    zz = 0
        else: # scroll by self.scrollIncr
            zz += self.scrollIncr * dir
            if dir < 0:
                if zz <0:
                    ni = self.zshape[axis] // self.scrollIncr
                    niTInc = ni * self.scrollIncr
                    zz += niTInc + self.scrollIncr
                    if zz >= self.zshape[axis]:
                        zz -= self.scrollIncr
            else:
                if zz >=self.zshape[axis]:
                    zz = zz % self.scrollIncr #20051115:  0
                
        self.setSlider(zz, axis)

    def OnWheelWhat(self, ev):
        what = ev.GetId() - (Menu_WheelWhatMenu+1)
        if what < self.zndim:
            def OnWheel(evt):
                rot = evt.GetWheelRotation()      / 120. #HACK
                self.doScroll(axis=what, dir=rot)
            self.viewer.OnWheel = OnWheel
        else:
            self.viewer.OnWheel = self.vOnWheel_zoom
        wx.EVT_MOUSEWHEEL(self.viewer, self.viewer.OnWheel)

    def OnScrollIncr(self, ev):
        i = ev.GetId() - (Menu_ScrollIncrementMenu+1)
        self.scrollIncr = scrollIncrL[i]
        if type(self.scrollIncr) is type("ss") and self.scrollIncr[-3:] == '...':
            i= wx.GetNumberFromUser("scroll step increment:", 'step', "scroll step increment:", 10, 1, 1000)
            self.scrollIncr = i

    def OnMenuAutoHistSec(self, ev):
        self.autoHistEachSect = ev.GetId() - Menu_AutoHistSec0

    def OnMenuAssignND(self, ev=None):
        from . import usefulX as Y
        Y.assignNdArrToVarname(self.data, "Y.vd(%s)"%(self.id,))

    def OnZZSlider(self, event):
        i = event.GetId()-1001
        zz = event.GetInt()
        self.zsec[i] = zz
        if zz != self.zlast[i]:
            #self.doOnZchange( zz )
            zsecTuple = tuple(self.zsec)

            #section-wise gfx:  name=tuple(zsec)
            try:
                self.viewer.newGLListEnableByName(tuple(self.zlast), on=False, 
                                                  skipBlacklisted=True, refreshNow=False)
            except KeyError:
                pass
            try:
                self.viewer.newGLListEnableByName(zsecTuple, on=True, 
                                                  skipBlacklisted=True, refreshNow=False)
            except KeyError:
                pass

            self.helpNewData(doAutoscale=False, setupHistArr=False)
            
            for f in self.doOnSecChanged:
                try:
                    f( zsecTuple, self )
                except:
                    if PriConfig.raiseEventHandlerExceptions:
                        raise
                    else:
                        import traceback, sys
                        print >>sys.stderr, " *** error in doOnSecChanged **"
                        traceback.print_exc()
                        print >>sys.stderr, " *** error in doOnSecChanged **"

            self.zlast[i] = zz
                
            
            
    def setSlider(self, z, zaxis=0):
        """zaxis specifies "which" zaxis should move to new value z
        """
        self.zsec[zaxis] = z
        self.zzslider[zaxis].SetValue(self.zsec[zaxis])
        e = wx.CommandEvent(wx.wxEVT_COMMAND_SLIDER_UPDATED, 1001+zaxis)
        e.SetInt( self.zsec[zaxis] )
        wx.PostEvent(self.zzslider[zaxis], e)
        #self.OnSlider(e)

        # #         e = wx.CommandEvent(wx.wxEVT_COMMAND_SLIDER_UPDATED, self.zzslider[zaxis].GetId())
        # #         e.SetInt(z)
        # #         #CHECK -- was commented out -- 2007-MDC put back in (win)
        # #         self.OnSlider(e)
        # #         #wx.PostEvent(self.zzslider[zaxis], e)
        # #         self.zzslider[zaxis].SetValue(z)



    def OnMenuSaveND(self, ev=None):
        if self.data.dtype.type in (N.complex64, N.complex128):
            dat = self.dataCplx
            datX = abs(self.data) #CHECK 
        else:
            dat = datX = self.data

        from .all import Mrc, U, FN, Y
        fn = FN(1,0)
        if not fn:
            return
        if fn[-4:] in [ ".mrc",  ".dat" ]:
            Mrc.save(dat, fn)
        elif fn[-5:] in [ ".fits" ]:
            U.saveFits(dat, fn)
        else:
            # save as sequence of image files
            # if fn does contain something like '%0d' auto-insert '_%0NNd'
            #      with NN to just fit the needed number of digits
            datX = datX.view()
            datX.shape = (-1,)+datX.shape[-2:]
            U.saveImg8_seq(datX, fn)
        Y.shellMessage("### Y.vd(%d) saved to '%s'\n"%(self.id, fn))




    def normalizeKeyShortcutTable(self):
        for k in self.keyShortcutTable.keys():
            if isinstance(k[1], basestring):
                if k[1].islower():
                    new_k = (k[0], ord(k[1])-ord('a')+ord('A'))
                else: #if k[1].isupper():
                    new_k = (k[0], ord(k[1]))
                #else:   #note: there are keys like '0', '9'
                #    raise ValueError, "invalid shortcut key (%s)"%(k[1],)
                self.keyShortcutTable[new_k] = self.keyShortcutTable[k]
                del self.keyShortcutTable[k]

    def installKeyCommands(self, frame):
        from .usefulX import iterChildrenTree
        for p in iterChildrenTree(frame):
            p.Bind(wx.EVT_KEY_DOWN, self.OnKeyDown)

    def OnKeyDown(self, evt):
        #modifiers = ""
        #for mod, ch in [(evt.ControlDown(), 'C'),
        #                (evt.AltDown(),     'A'),
        #                (evt.ShiftDown(),   'S'),
        #                (evt.MetaDown(),    'M')]:
        #    if mod:
        #        modifiers += ch
        #    else:
        #        modifiers += '-'
        #
        #print modifiers, evt.GetModifiers(), evt.GetKeyCode(), evt.GetRawKeyCode(), evt.GetUnicodeKey(), evt.GetX(), evt.GetY()
        
        f = self.keyShortcutTable.get((evt.GetModifiers(), evt.GetKeyCode()))
        if f is not None:
            f()
        else:
            evt.Skip() # this this maybe be always called ! CHECK

    
    def setDefaultKeyShortcuts(self):
        self.keyShortcutTable[ 0, wx.WXK_NUMPAD_MULTIPLY] = self.OnAutoHistScale
        self.keyShortcutTable[ 0, 'l' ] = self.OnHistLog
        self.keyShortcutTable[ 0, 'f' ] = self.OnViewFFT  # CHECK view2
        self.keyShortcutTable[ wx.MOD_SHIFT, 'f' ] = self.OnViewFFTInv # CHECK view2
        self.keyShortcutTable[ 0, 'a' ] = self.OnViewCplxAsAbs # CHECK view2
        self.keyShortcutTable[ 0, 'p' ] = self.OnViewCplxAsPhase # CHECK view2
        self.keyShortcutTable[ 0, 'x' ] = self.OnViewFlipXZ
        self.keyShortcutTable[ 0, 'y' ] = self.OnViewFlipYZ
        self.keyShortcutTable[ 0, 'v' ] = self.OnViewMaxProj
        self.keyShortcutTable[ wx.MOD_SHIFT, 'v' ] = self.OnViewMeanProj


        #self.keyShortcutTable[ 0, 'm' ] = self.OnViewVTK
        #self.keyShortcutTable[ 0, wx.WXK_F1 ] = self.OnShowPopupTransient

        # z-slider
        self.keyShortcutTable[ 0, wx.WXK_LEFT ] = lambda :self.doScroll(axis=0, dir=-1)
        self.keyShortcutTable[ 0, wx.WXK_RIGHT ]= lambda :self.doScroll(axis=0, dir=+1)
        self.keyShortcutTable[ 0, wx.WXK_UP ]   = lambda :self.doScroll(axis=1, dir=+1)
        self.keyShortcutTable[ 0, wx.WXK_DOWN ] = lambda :self.doScroll(axis=1, dir=-1)


        self.keyShortcutTable[ 0, 'c' ] = self.viewer.OnColor
        self.keyShortcutTable[ 0, 'o' ] = self.viewer.OnChgOrig
        self.keyShortcutTable[ 0, 'g' ] = self.viewer.setPixelGrid
        self.keyShortcutTable[ 0, 'b' ] = self.viewer.OnChgNoGfx

        # panning
        self.keyShortcutTable[ wx.MOD_CMD|wx.MOD_SHIFT, wx.WXK_LEFT ] = self.viewer.quaterShiftOffsetLeft
        self.keyShortcutTable[ wx.MOD_CMD|wx.MOD_SHIFT, wx.WXK_RIGHT ]= self.viewer.quaterShiftOffsetRight
        self.keyShortcutTable[ wx.MOD_CMD|wx.MOD_SHIFT, wx.WXK_UP ]   = self.viewer.quaterShiftOffsetUp
        self.keyShortcutTable[ wx.MOD_CMD|wx.MOD_SHIFT, wx.WXK_DOWN ] = self.viewer.quaterShiftOffsetDown
        self.keyShortcutTable[ wx.MOD_CMD, wx.WXK_LEFT ] = lambda :self.viewer.doShift(-PriConfig.viewerArrowKeysShiftBy,0)
        self.keyShortcutTable[ wx.MOD_CMD, wx.WXK_RIGHT ]= lambda :self.viewer.doShift(+PriConfig.viewerArrowKeysShiftBy,0)
        self.keyShortcutTable[ wx.MOD_CMD, wx.WXK_UP ]   = lambda :self.viewer.doShift(0,+PriConfig.viewerArrowKeysShiftBy)
        self.keyShortcutTable[ wx.MOD_CMD, wx.WXK_DOWN ] = lambda :self.viewer.doShift(0,-PriConfig.viewerArrowKeysShiftBy)

        # zooming
        self.keyShortcutTable[ 0, '1' ] = lambda: self.viewer.zoom(1)
        self.keyShortcutTable[ 0, '0' ] = self.viewer.doReset
        self.keyShortcutTable[ 0, '9' ] = self.viewer.OnCenter
        self.keyShortcutTable[ 0, wx.WXK_HOME ] = self.viewer.OnCenter
        self.keyShortcutTable[ 0, wx.WXK_NEXT ] = self.viewer.OnZoomOut
        self.keyShortcutTable[ 0, wx.WXK_PRIOR] = self.viewer.OnZoomIn
        self.keyShortcutTable[ 0, 'd' ] = lambda :self.viewer.zoom(2., absolute=False)
        self.keyShortcutTable[ 0, 'h' ] = lambda :self.viewer.zoom(.5, absolute=False)

        self.keyShortcutTable[ 0, 'r' ] = self.viewer.OnReload

        self.normalizeKeyShortcutTable()

    def putZSlidersIntoTopBox(self, parent, boxSizer, skipAxes=[]):
        [si.GetWindow().Destroy() for si in boxSizer.GetChildren()] # needed with Y.viewInViewer

        if type(skipAxes) is type(1):
            skipAxes = [skipAxes]

        self.zzslider = [None]*self.zndim
        for i in range(self.zndim-1,-1,-1):
            if i in skipAxes:
                continue
            self.zzslider[i] = wx.Slider(parent, 1001+i, self.zsec[i], 0, self.zshape[i]-1,
                               wx.DefaultPosition, wx.DefaultSize,
                               #wx.SL_VERTICAL
                               wx.SL_HORIZONTAL
                               | wx.SL_AUTOTICKS | wx.SL_LABELS )
            if self.zshape[i] > 1:
                self.zzslider[i].SetTickFreq(5, 1)
                ##boxSizer.Add(vslider, 1, wx.EXPAND)
                boxSizer.Insert(0, self.zzslider[i], 1, wx.EXPAND)
                wx.EVT_SLIDER(parent, self.zzslider[i].GetId(), self.OnZZSlider)
            else: # still good to create the slider - just to no have special handling
                # self.zzslider[i].Show(0) # 
                boxSizer.Insert(0, self.zzslider[i], 0, 0)

            self.zzslider[i].Bind(wx.EVT_RIGHT_DOWN, self.onPixelValInfoLabelRightClick)

        if self.zndim == 0:
            label = wx.StaticText(parent, -1, "")
            #label.SetHelpText("This is the help text for the label")
            boxSizer.Add(label, 0, wx.GROW|wx.ALL, 2)

            
        self.label = wx.StaticText(parent, -1, "----move mouse over image----") # HACK find better way to reserve space to have "val: 1234" always visible 
        self.label.Bind(wx.EVT_RIGHT_DOWN, self.onPixelValInfoLabelRightClick)

    
        boxSizer.Add(self.label, 0, wx.GROW|wx.ALL, 2)
        boxSizer.Layout()
        parent.Layout()

    def onPixelValInfoLabelRightClick(self, ev):
        from . import usefulX as Y
        topparent = wx.GetTopLevelParent(self.viewer)
        pos=ev.GetPosition()
        pos = topparent.ClientToScreen(pos)

        try:
            gp = self._onPixelValInfoLabelRightClick_gp
            gp._buttBox.frame.Raise()
            gp._buttBox.frame.SetPosition( pos )
            #wx.Bell()
            return
        except: # (AttributeError OR PyDeadObjectError)
            self._onPixelValInfoLabelRightClick_gp = gp = Y.guiParams()

        Y.buttonBox(itemList=
                    gp._bboxBool("frac coords", 'floatCoords', v=self.showFloatCoordsWhenZoomingIn, 
                                 controls="cb", newLine=False, 
                                 tooltip="show fractional pixel coordinates if zoom > 1", 
                                 regFcn=lambda v,n:
                                     Y.vSetCoordsDisplayFormat(v_id=self.id, 
                                                               showAsFloat=v, width=None), 
                                 regFcnName=None) +
                    gp._bboxInt("width", 'width', v=100, slider=True, slmin=0, slmax=500, 
                                newLine=False, tooltip="width of pixel info panel", 
                                regFcn=lambda v,n:
                                    Y.vSetCoordsDisplayFormat(v_id=self.id, showAsFloat=None, width=v), 
                                regFcnName=None),
                    title="format pixel info (viewer %d)"%(self.id,),
                    execModule=gp, 
                    layout="boxHoriz", panel=None, 
                    parent=topparent, 
                    pos=pos, )
        gp._buttBox = Y.buttonBoxes[-1]
