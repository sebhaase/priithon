""" Priithon
# modified version of http://wiki.wxpython.org/AsynchronousSockets 
#                     by Josiah Carlson
#
# seb: what does this mean:
             # remember to validate any possible
             # socket objects recieved from the GUI,
             # they could already be closed
       # this is somehow related to the **kwarg sock=self - but otherwise unused
"""
from __future__ import absolute_import

import wx
import wx.lib.newevent
import socket
import asyncore
import threading
import Queue

to_network = Queue.Queue()
LogEvent, EVT_LOG_EVENT = wx.lib.newevent.NewEvent()

#for high bandwidth applications, you are going to want to handle the
#out_buffer via a different mechanism, perhaps similar to asynchat or
#otherwise
class DispatcherConnection(asyncore.dispatcher_with_send):
    def __init__(self, connection, logFcn=None): # mainwindow):
        """
        seb: logFcn, if None no logging done, otherwise logFcn called for each log-print
        """
        #seb self.mainwindow = mainwindow
        self.logFcn = logFcn # seb
        asyncore.dispatcher_with_send.__init__(self, connection)
    def writable(self):
        return bool(self.out_buffer)
    def handle_write(self):
        self.initiate_send()
    def log(self, message):
        #self.mainwindow.LogString(message, sock=self)
        if self.logFcn is not None:
            self.logFcn(message)
    def log_info(self, message, type='info'):
        if type != 'info':
            self.log(message)
    def handle_close(self):
        self.log("Connection dropped: %s"%(self.addr,))
        self.close()

    #implement your client logic as a subclass

class LineEchoConnection(DispatcherConnection):
    inc_buffer = ''
    def handle_read(self):
        self.inc_buffer += self.recv(512)
        while '\n' in self.inc_buffer:
            snd, self.inc_buffer = self.inc_buffer.split('\n', 1)
            snd += '\n'
            self.log("Line from %s: %r"%(self.addr, snd))
            self.send(snd)

class DispatcherServer(asyncore.dispatcher):
    #seb def __init__(self, host, port, mainwindow, factory=LineEchoConnection):
    def __init__(self, host, port, factory, logFcn=None):
        """
        seb: logFcn, if None no logging done, otherwise logFcn called for each log-print
        """
        #seb self.mainwindow = mainwindow
        self.logFcn = logFcn # seb
        self.factory = factory
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.bind((host, port))
        self.listen(5)
    def handle_accept(self):
        connection, info = self.accept()
        #seb self.mainwindow.LogString("Got connection: %s"%(info,), sock=self)
        if self.logFcn is not None:
            self.logFcn("Got connection: %s"%(info,))
        #seb self.factory(connection, self.mainwindow)
        self.factory(connection, self.logFcn)

def loop():
    while 1:
        while not to_network.empty():
            message = to_network.get()
            #process and handle message
            #
            #remember to validate any possible
            #socket objects recieved from the GUI,
            #they could already be closed
        asyncore.poll(timeout=.01)

class MainWindow(wx.Frame):
    def __init__(self, host, port, threaded=0):
        wx.Frame.__init__(self, None, title="Sample echo server")

        #add any other GUI objects here

        sz = wx.BoxSizer(wx.VERTICAL)
        self.log = wx.TextCtrl(self, -1, '', style=wx.TE_MULTILINE|wx.TE_RICH2)
        sz.Add(self.log, 1, wx.EXPAND|wx.ALL, 3)

        self.Bind(EVT_LOG_EVENT, self.LogEvent)
        DispatcherServer(host, port, LineEchoConnection, self.LogString) #seb self)
        if not threaded:
            self.poller = wx.Timer(self, wx.NewId())
            self.Bind(wx.EVT_TIMER, self.OnPoll)
            #poll 50 times/second, should be enough for low-bandwidth apps
            self.poller.Start(20, wx.TIMER_CONTINUOUS)
        else:
            t = threading.Thread(target=loop)
            t.setDaemon(1)
            t.start()

    def LogString(self, message, **kwargs):
        event = LogEvent(msg=message, **kwargs)
        if threading.activeCount() == 1:
            self.LogEvent(event)
        else:
            wx.PostEvent(self, event)

    def LogEvent(self, evt):
        self.log.AppendText(evt.msg)
        if not evt.msg.endswith('\n'):
            self.log.AppendText('\n')

    def OnPoll(self, evt):
        asyncore.poll(timeout=0)
    #add other methods as necessary

if __name__ == '__main__':
    a = wx.App(0)
    b = MainWindow('localhost', 3399, 0)
    b.Show(1)
    a.MainLoop()


######################################################################
# for Priithon
try:
    _pollers
except NameError:
    _pollers=[]

'''
class CustomConnection(DispatcherConnection):
    #inc_buffer = ''

    # def __init__(self, connection, logFcn, handle_read):
    #     self.hr = handle_read
    #     DispatcherConnection.__init__(self, connection, logFcn)
    def handle_read(self):
        self.hr(self)
        # self.inc_buffer += self.recv(512)
        # while '\n' in self.inc_buffer:
        #     snd, self.inc_buffer = self.inc_buffer.split('\n', 1)
        #     snd += '\n'
        #     self.log("Line from %s: %r"%(self.addr, snd))
        #     self.send(snd)
'''

def startSocketServer(onRead,
                      linewise=True,
                      logFcn = None,
                      port=4711, 
                      host='', 
                      wxEvtFrame=None, 
                      threaded=False):
                      #20100301 arg not used: verbose=True):
    """
    install a server to listen on given `port` on given `host`

    onRead is a handler function that is being called with a 
    asyncore.dispatcher_with_send object as argument (`asynDisp`)
    (its type is really a DispatcherConnection, which is derived of that)

    if `linewise`: `onRead` is called for each completed line
                   an `line` is an extra first(!) argument
                   ('\n' is truncated)
                   (`asynDisp.recv(512)` is called for you as needed!)
    otherwise, `onRead` has to do the `asynDisp`.recv(512) calls itself

    `host`='' means "all IPs of local host" (127.0.0.1 + external IP(s))

    `logFcn`: if None no logging done, otherwise `logFcn` called for each 
                                log-print with string message as argument

    if `threaded` is False,
       a timer event is connected to `wxEvtFrame`
    `wxEvtFrame` None means, find and use "first" toplevel parent
    """
    if not threaded:
        if wxEvtFrame is None:
            wxEvtFrame = wx.GetTopLevelWindows()[0]

    handlerFunc_dict = {}
    
    if linewise:
        #'''
        inc_buffer = ['']
        def onRead_helper(asynDisp):
            inc_buffer[0] += asynDisp.recv(512)
            while '\n' in inc_buffer[0]:
                line, inc_buffer[0] = inc_buffer[0].split('\n', 1)
                #line += '\n'
                #asynDisp.log("Line from %s: %r"%(asynDisp.addr, line))
                #asynDisp.send(line)
                try:
                    onRead(line, asynDisp)
                except:
                    from . import PriConfig
                    if PriConfig.raiseEventHandlerExceptions:
                        import sys
                        from .usefulX import _guiExcept
                        wx.CallAfter(_guiExcept, *sys.exc_info())
                    else:
                        import traceback, sys
                        print >>sys.stderr, " *** error in async onRead **"
                        traceback.print_exc()
                        print >>sys.stderr, " *** error in async onRead **"

        #'''
        '''
        class onRead_helper_cls:
            def __init__(s):
                s.inc_buffer = ''

            #@staticmethod
            def __call__(s): # asynDisp):
                print s
                s.inc_buffer += asynDisp.recv(512)
                while '\n' in inc_buffer:
                    line, s.inc_buffer = s.inc_buffer.split('\n', 1)
                    #line += '\n'
                    #asynDisp.log("Line from %s: %r"%(self.addr, line))
                    #asynDisp.send(line)
                    onRead(line, asynDisp)
        '''

        handlerFunc_dict["handle_read"] = onRead_helper # onRead_helper_cls()
    else:
        handlerFunc_dict["handle_read"] = onRead

    import new
    factory = new.classobj("Custom_DispatcherConnection", 
                           (DispatcherConnection,), 
                           handlerFunc_dict)
    DispatcherServer(host, port, factory, logFcn)

    if not threaded:

        def OnPoll(evt):
            asyncore.poll(timeout=0)

        poller = wx.Timer(wxEvtFrame, wx.NewId())
        wxEvtFrame.Bind(wx.EVT_TIMER, OnPoll)
        #poll 50 times/second, should be enough for low-bandwidth apps
        poller.Start(20, wx.TIMER_CONTINUOUS)
        poller._id_in_pollers_list = len(_pollers) # so that it can be set to None later
        _pollers.append( poller )
    else:
        t = threading.Thread(target=loop)
        t.setDaemon(1)
        t.start()
        t._id_in_pollers_list = len(_pollers) # so that it can be set to None later
        _pollers.append( t )  # check type - HACK not really a poller but a thread


def startSocketServer_demo(port=4711, host='localhost', threaded=False):
    b = MainWindow(host, port, threaded)
    b.Show(1)

def startSocketServer_clearAll(closeAllSockets=True, stopAllPolling=True):
    """
    use this to stop all prior started servers
    """
    if closeAllSockets:
        asyncore.close_all()
    if stopAllPolling:
        global _pollers
        for p in _pollers:
            try:
                p.Stop
            except:
                import traceback
                traceback.print_exc()

        _pollers = []
