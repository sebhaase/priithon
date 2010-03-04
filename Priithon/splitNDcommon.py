"""
the container of
(2d) viewer, histogram and "z"-slider

common base class for single-color and multi-color version
"""

__author__  = "Sebastian Haase <haase@msg.ucsf.edu>"
__license__ = "BSD license - see LICENSE file"

import wx
import numpy as N
import weakref

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
    
    def doScroll(self, axis, dir):
        ''' dir is -1 OR +1
        '''
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
        import usefulX2 as Y
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
                self.viewer.newGLListEnableByName(tuple(self.zlast), on=False, refreshNow=False)
            except KeyError:
                pass
            try:
                self.viewer.newGLListEnableByName(zsecTuple, on=True, refreshNow=False)
            except KeyError:
                pass

            try:
                self.doSecChanged( zsecTuple )
            except:
                import traceback
                traceback.print_exc()
                
            self.helpNewData(doAutoscale=False, setupHistArr=False)
            self.zlast[i] = zz
            
            
    def setSlider(self, z, zaxis=0):
        '''zaxis specifies "which" zaxis should move to new value z
        '''
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

    def doSecChanged(self, zsecTuple):
        pass #print zsecTuple


