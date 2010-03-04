__author__  = "Sebastian Haase <haase@msg.ucsf.edu>"
__license__ = "BSD license - see LICENSE file"

import wx
# ID_ZSLIDER = 1000

class ZSlider( wx.Frame):
    def __init__(self, nz, title=""):
        wx.Frame.__init__(self, None, -1, title) # , size=wx.Size(240,250))
        
        self.sizer = wx.BoxSizer(wx.VERTICAL)

        self.zmax = nz-1
        self.lastZ = -1
        self.zslider = wx.Slider(self, 1001, 0, 0, self.zmax,
                          wx.DefaultPosition, wx.DefaultSize,
                             #wx.SL_VERTICAL
                             wx.SL_HORIZONTAL
                             | wx.SL_AUTOTICKS | wx.SL_LABELS )
        self.zslider.SetTickFreq(5, 1)

        self.sizer.Add(self.zslider, 1, wx.EXPAND)
        #         panel = wx.Panel(self, -1)
        
        #         button = wx.Button(panel, 1003, "Close Me")
        #         button.SetPosition(wx.Point(15, 15))
        #         self.button = button       
        #         EVT_BUTTON(self, 1003, self.OnCloseMe)
        #wx.EVT_SCROLL_THUMBRELEASE(self, self.OnSlider)
        wx.EVT_SLIDER(self, self.zslider.GetId(), self.OnSlider)
        wx.EVT_CLOSE(self, self.OnCloseWindow)
        #         self.name = 'bubba'
        
        #     def OnCloseMe(self, event):
        #         print 'hit'
        #         self.Close(True)
        self.sizer.Fit(self)

        self.SetAutoLayout(True)
        self.SetSizer(self.sizer)

        self.zslider.SetBackgroundColour(wx.LIGHT_GREY)
        self.SetBackgroundColour(wx.LIGHT_GREY)

        self.Show()
     
    def OnCloseWindow(self, event):
        # print 'close'
        self.Destroy()

    def OnSlider(self, event):
        zz = event.GetInt()
        if zz != self.lastZ:
            self.lastZ = zz
            self.doOnZchange( zz )
    def doOnZchange(self, newZ):
        print newZ
        ###self.v.setImage(self.data[zz])
     
