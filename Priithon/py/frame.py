"""Base frame with menu."""

__author__ = "Patrick K. O'Brien <pobrien@orbtech.com>"
__cvsid__ = "$Id: frame.py,v 1.6 2004/02/23 22:36:20 RD Exp $"
__revision__ = "$Revision: 1.6 $"[11:-2]

import wx
from version import VERSION

#20051104 seb remove many meaningless menu points
# ID_NEW = wx.ID_NEW
# ID_OPEN = wx.ID_OPEN
# ID_REVERT = wx.ID_REVERT
ID_CLOSE = wx.ID_CLOSE
# ID_SAVE = wx.ID_SAVE
# ID_SAVEAS = wx.ID_SAVEAS
# ID_PRINT = wx.ID_PRINT
ID_EXIT = wx.ID_EXIT
ID_UNDO = wx.ID_UNDO
ID_REDO = wx.ID_REDO
# ID_CUT = wx.ID_CUT
ID_COPY = wx.ID_COPY
ID_PASTE = wx.ID_PASTE
# ID_CLEAR = wx.ID_CLEAR
# ID_SELECTALL = wx.ID_SELECTALL
ID_ABOUT = wx.ID_ABOUT
ID_AUTOCOMP = wx.NewId()
ID_AUTOCOMP_SHOW = wx.NewId()
ID_AUTOCOMP_MAGIC = wx.NewId()
ID_AUTOCOMP_SINGLE = wx.NewId()
ID_AUTOCOMP_DOUBLE = wx.NewId()
ID_CALLTIPS = wx.NewId()
ID_CALLTIPS_SHOW = wx.NewId()
ID_COPY_PLUS = wx.NewId()
# ID_NAMESPACE = wx.NewId()
ID_PASTE_PLUS = wx.NewId()
ID_WRAP = wx.NewId()
ID_USEAA = wx.NewId()
ID_MARKWINDOWS = wx.NewId()
ID_RAISEWINDOWS = wx.NewId()
ID_MINIMIZEWINDOWS = wx.NewId()
ID_TEST5 = wx.NewId()
ID_TEST2 = wx.NewId()
ID_TESTALL = wx.NewId()

ID_EDITOR = wx.NewId()
ID_INSPECTOR = wx.NewId()
ID_LISTDIR = wx.NewId()
ID_SAVESESSION = wx.NewId()
ID_AUTOSAVESESSION = wx.NewId()
ID_LISTVARS = wx.NewId()
ID_EXECPY   = wx.NewId()
ID_CLONESHELL   = wx.NewId()
ID_VANIMATE   = wx.NewId()
ID_VPLOTSLIDER   = wx.NewId()
ID_OSXBUG = wx.NewId()

class Frame(wx.Frame):
    """Frame with standard menu items."""

    revision = __revision__

    def __init__(self, parent=None, id=-1, title='Editor',
                 pos=wx.DefaultPosition, size=wx.DefaultSize, 
                 style=wx.DEFAULT_FRAME_STYLE):
        """Create a Frame instance."""
        wx.Frame.__init__(self, parent, id, title, pos, size, style)
        self.CreateStatusBar()
        self.SetStatusText('Frame')
        import images
        self.SetIcon(images.getPyIcon())
        self.__createMenus()
        wx.EVT_CLOSE(self, self.OnClose)

    def OnClose(self, event):
        """Event handler for closing."""
        self.Destroy()

    def __createMenus(self):
        m = self.fileMenu = wx.Menu()
        #seb 20051102
        #         m.Append(ID_NEW, '&New \tCtrl+N',
        #                  'New file')
        #         m.Append(ID_OPEN, '&Open... \tCtrl+O',
        #                  'Open file')
        #         m.AppendSeparator()
        #         m.Append(ID_REVERT, '&Revert \tCtrl+R',
        #                  'Revert to last saved version')
        #         m.Append(ID_CLOSE, '&Close \tCtrl+W',
        #                  'Close file')
        #         m.AppendSeparator()
        #         m.Append(ID_SAVE, '&Save... \tCtrl+S',
        #                  'Save file')
        #         m.Append(ID_SAVEAS, 'Save &As \tShift+Ctrl+S',
        #                  'Save file with new name')
        #         m.AppendSeparator()
        #         m.Append(ID_PRINT, '&Print... \tCtrl+P',
        #                  'Print file')
        #         m.AppendSeparator()
        #         m.Append(ID_NAMESPACE, '&Update Namespace \tShift+Ctrl+N',
        #                  'Update namespace for autocompletion and calltips')
        #         m.AppendSeparator()

        #seb 20051102        
        m.Append(ID_LISTDIR, '&Open img file (choose dir)', #'&New \tCtrl+N',
                 'Open file list viewer for a directory')
        m.Append(ID_SAVESESSION, '&Save session text', #'&New \tCtrl+N',
                 'Save all text of the PyShell window into a text file')
        m.Append(ID_AUTOSAVESESSION, '&Auto-save session\tCtrl-S', #'&New \tCtrl+N',
                 'Re-Save all text of the PyShell window into a text file with a "auto generated" name')
        m.Append(ID_LISTVARS, 'List &Vars', #'&New \tCtrl+N',
                 'Open list of all array variables known in the current PyShell session')
        m.Append(ID_EXECPY, '&Execute file', #'&New \tCtrl+N',
                 'Execute a python file in the current PyShell session')
        m.Append(ID_EDITOR, 'Text E&ditor ...', #'&New \tCtrl+N',
                 'Open a text file editor [ Y.editor() ]')
        m.Append(ID_INSPECTOR, '&Inspect ...', #'&New \tCtrl+N',
                 'Open window to inspect all variables, functions, modules, ... [ Y.inspect() ]')
        m.Append(ID_CLONESHELL, 'Open a second &view of Priithon shell window', #'&New \tCtrl+N',
                 'Open a new window also containg the Priithon shell -- second view -- Y.shell(clone=True)')

        m.AppendSeparator()
        m.AppendCheckItem(ID_OSXBUG, 'use OpenGL-bug workaround', #'&New \tCtrl+N',
                 'OSX tends to not implement Float32 2D textures correctly - use workaround')

        m.Append(ID_EXIT, 'E&xit', 'Exit Program')

        m = self.editMenu = wx.Menu()
        m.Append(ID_UNDO, '&Undo \tCtrl+Z',
                 'Undo the last action')
        m.Append(ID_REDO, '&Redo \tCtrl+Y',
                 'Redo the last undone action')
        m.AppendSeparator()
        #         m.Append(ID_CUT, 'Cu&t \tCtrl+X',
        #                  'Cut the selection')
        m.Append(ID_COPY, '&Copy \tCtrl+C',
                 'Copy the selection')
        m.Append(ID_COPY_PLUS, 'Cop&y Plus \tShift+Ctrl+C',
                 'Copy the selection - retaining prompts')
        m.Append(ID_PASTE, '&Paste \tCtrl+V', 'Paste from clipboard')
        m.Append(ID_PASTE_PLUS, 'Past&e Plus \tShift+Ctrl+V',
                 'Paste and run commands')
        #         m.AppendSeparator()
        #         m.Append(ID_CLEAR, 'Cle&ar',
        #                  'Delete the selection')
        #         m.Append(ID_SELECTALL, 'Select A&ll \tCtrl+A',
        #                  'Select all text')

        m = self.autocompMenu = wx.Menu()
        m.Append(ID_AUTOCOMP_SHOW, 'Show Auto Completion',
                 'Show auto completion list', wx.ITEM_CHECK)
        m.Append(ID_AUTOCOMP_MAGIC, 'Include Magic Attributes',
                 'Include attributes visible to __getattr__ and __setattr__',
                 wx.ITEM_CHECK)
        m.Append(ID_AUTOCOMP_SINGLE, 'Include Single Underscores',
                 'Include attibutes prefixed by a single underscore', wx.ITEM_CHECK)
        m.Append(ID_AUTOCOMP_DOUBLE, 'Include Double Underscores',
                 'Include attibutes prefixed by a double underscore', wx.ITEM_CHECK)

        m = self.calltipsMenu = wx.Menu()
        m.Append(ID_CALLTIPS_SHOW, 'Show Call Tips',
                 'Show call tips with argument signature and docstring', wx.ITEM_CHECK)

        m = self.optionsMenu = wx.Menu()
        m.AppendMenu(ID_AUTOCOMP, '&Auto Completion', self.autocompMenu,
                     'Auto Completion Options')
        m.AppendMenu(ID_CALLTIPS, '&Call Tips', self.calltipsMenu,
                     'Call Tip Options')
        m.Append(ID_WRAP, '&Wrap Lines',
                 'Wrap lines at right edge', wx.ITEM_CHECK)
        if wx.Platform == "__WXMAC__":
            m.Append(ID_USEAA, '&Use AntiAliasing',
                     'Use anti-aliased fonts', wx.ITEM_CHECK)

        m = self.priithonMenu = wx.Menu()
        m.Append(ID_VANIMATE, "viewer &animation control", #'&New \tCtrl+N',
                 "Open viewer animation control -- Y.vAnimate()")
        m.Append(ID_VPLOTSLIDER, "use &plot figure as z-slider", #'&New \tCtrl+N',
                 "Open GUI to make a plot figure function as z slider for a viewer -- Y.vPlotAsSliderGUI()")
        m.Append(ID_RAISEWINDOWS, '&Raise all Windows', 
                 "raise all Priithon windows above others")
        m.Append(ID_MINIMIZEWINDOWS, 'M&inimize all Windows', 
                 "minimize (iconize) all Priithon windows")
        m.Append(ID_MARKWINDOWS, '&Mark all Windows ...', 
                 "append marker-string to title of all windows belonging to this Priithon instance")
        m.AppendSeparator()
        m.Append(ID_TEST5, 'show mandel&brot set', 
                 "demonstrate colorful single channel image [ Y.test5() ]")
        m.Append(ID_TEST2, 'test multi &color viewer [ Y.test2() ]', 
                 "test multi color viewer [ Y.test2() ]")
        m.Append(ID_TESTALL, 'do all &tests [ Y.test...() ]', 
                 "call all Y.test[1,2,3,...] functions")

        m = self.helpMenu = wx.Menu()
        m.AppendSeparator()
        m.Append(ID_ABOUT, '&About...', 'About Priithon')

        b = self.menuBar = wx.MenuBar()
        b.Append(self.fileMenu, '&File')
        b.Append(self.editMenu, '&Edit')
        b.Append(self.optionsMenu, '&Options')
        b.Append(self.priithonMenu, '&Priithon')
        b.Append(self.helpMenu, '&Help')
        self.SetMenuBar(b)

        #seb 20051102
        wx.EVT_MENU(self, ID_EDITOR, self.OnEditor)
        wx.EVT_MENU(self, ID_INSPECTOR, self.OnInspect)
        wx.EVT_MENU(self, ID_LISTDIR, self.OnListDir)
        wx.EVT_MENU(self, ID_SAVESESSION, self.OnSaveSession)
        wx.EVT_MENU(self, ID_AUTOSAVESESSION, self.OnAutoSaveSession)
        wx.EVT_MENU(self, ID_LISTVARS, self.OnListVars)
        wx.EVT_MENU(self, ID_EXECPY, self.OnExecPy)        
        wx.EVT_MENU(self, ID_CLONESHELL, self.OnCloneShell)
        wx.EVT_MENU(self, ID_VANIMATE, self.OnVanimate)
        wx.EVT_MENU(self, ID_VPLOTSLIDER, self.OnVplotslider)
        wx.EVT_MENU(self, ID_OSXBUG, self.OnOSXBug)
        
        #seb 20051102
        #         wx.EVT_MENU(self, ID_NEW, self.OnFileNew)
        #         wx.EVT_MENU(self, ID_OPEN, self.OnFileOpen)
        #         wx.EVT_MENU(self, ID_REVERT, self.OnFileRevert)
        #         wx.EVT_MENU(self, ID_CLOSE, self.OnFileClose)
        #         wx.EVT_MENU(self, ID_SAVE, self.OnFileSave)
        #         wx.EVT_MENU(self, ID_SAVEAS, self.OnFileSaveAs)
        #         wx.EVT_MENU(self, ID_NAMESPACE, self.OnFileUpdateNamespace)
        #         wx.EVT_MENU(self, ID_PRINT, self.OnFilePrint)
        wx.EVT_MENU(self, ID_EXIT, self.OnExit)
        wx.EVT_MENU(self, ID_UNDO, self.OnUndo)
        wx.EVT_MENU(self, ID_REDO, self.OnRedo)
        #         wx.EVT_MENU(self, ID_CUT, self.OnCut)
        wx.EVT_MENU(self, ID_COPY, self.OnCopy)
        wx.EVT_MENU(self, ID_COPY_PLUS, self.OnCopyPlus)
        wx.EVT_MENU(self, ID_PASTE, self.OnPaste)
        wx.EVT_MENU(self, ID_PASTE_PLUS, self.OnPastePlus)
        #         wx.EVT_MENU(self, ID_CLEAR, self.OnClear)
        #         wx.EVT_MENU(self, ID_SELECTALL, self.OnSelectAll)
        wx.EVT_MENU(self, ID_ABOUT, self.OnAbout)
        wx.EVT_MENU(self, ID_AUTOCOMP_SHOW, self.OnAutoCompleteShow)
        wx.EVT_MENU(self, ID_AUTOCOMP_MAGIC, self.OnAutoCompleteMagic)
        wx.EVT_MENU(self, ID_AUTOCOMP_SINGLE, self.OnAutoCompleteSingle)
        wx.EVT_MENU(self, ID_AUTOCOMP_DOUBLE, self.OnAutoCompleteDouble)
        wx.EVT_MENU(self, ID_CALLTIPS_SHOW, self.OnCallTipsShow)
        wx.EVT_MENU(self, ID_WRAP, self.OnWrap)
        wx.EVT_MENU(self, ID_USEAA, self.OnUseAA)
        wx.EVT_MENU(self, ID_MARKWINDOWS, self.OnMarkWindows)
        wx.EVT_MENU(self, ID_RAISEWINDOWS, self.OnRaiseWindows)
        wx.EVT_MENU(self, ID_MINIMIZEWINDOWS, self.OnMinimizeWindows)
        wx.EVT_MENU(self, ID_TEST5, self.OnTest5)
        wx.EVT_MENU(self, ID_TEST2, self.OnTest2)
        wx.EVT_MENU(self, ID_TESTALL, self.OnTestAll)
        #seb 20051102
        #         wx.EVT_UPDATE_UI(self, ID_NEW, self.OnUpdateMenu)
        #         wx.EVT_UPDATE_UI(self, ID_OPEN, self.OnUpdateMenu)
        #         wx.EVT_UPDATE_UI(self, ID_REVERT, self.OnUpdateMenu)
        #         wx.EVT_UPDATE_UI(self, ID_CLOSE, self.OnUpdateMenu)
        #         wx.EVT_UPDATE_UI(self, ID_SAVE, self.OnUpdateMenu)
        #         wx.EVT_UPDATE_UI(self, ID_SAVEAS, self.OnUpdateMenu)
        #         wx.EVT_UPDATE_UI(self, ID_NAMESPACE, self.OnUpdateMenu)
        #         wx.EVT_UPDATE_UI(self, ID_PRINT, self.OnUpdateMenu)
        wx.EVT_UPDATE_UI(self, ID_UNDO, self.OnUpdateMenu)
        wx.EVT_UPDATE_UI(self, ID_REDO, self.OnUpdateMenu)
        #         wx.EVT_UPDATE_UI(self, ID_CUT, self.OnUpdateMenu)
        wx.EVT_UPDATE_UI(self, ID_COPY, self.OnUpdateMenu)
        wx.EVT_UPDATE_UI(self, ID_COPY_PLUS, self.OnUpdateMenu)
        wx.EVT_UPDATE_UI(self, ID_PASTE, self.OnUpdateMenu)
        wx.EVT_UPDATE_UI(self, ID_PASTE_PLUS, self.OnUpdateMenu)
        #         wx.EVT_UPDATE_UI(self, ID_CLEAR, self.OnUpdateMenu)
        #         wx.EVT_UPDATE_UI(self, ID_SELECTALL, self.OnUpdateMenu)
        wx.EVT_UPDATE_UI(self, ID_AUTOCOMP_SHOW, self.OnUpdateMenu)
        wx.EVT_UPDATE_UI(self, ID_AUTOCOMP_MAGIC, self.OnUpdateMenu)
        wx.EVT_UPDATE_UI(self, ID_AUTOCOMP_SINGLE, self.OnUpdateMenu)
        wx.EVT_UPDATE_UI(self, ID_AUTOCOMP_DOUBLE, self.OnUpdateMenu)
        wx.EVT_UPDATE_UI(self, ID_CALLTIPS_SHOW, self.OnUpdateMenu)
        wx.EVT_UPDATE_UI(self, ID_WRAP, self.OnUpdateMenu)
        wx.EVT_UPDATE_UI(self, ID_USEAA, self.OnUpdateMenu)
        wx.EVT_UPDATE_UI(self, ID_OSXBUG, self.OnUpdateMenu)
        
    def OnEditor(self, evt=None):
        from Priithon.all import Y
        Y.editor()
    def OnInspect(self, evt=None):
        from Priithon.all import Y
        Y.inspect()
    def OnListDir(self, evt=None):
        from Priithon.all import Y
        Y.listFilesViewer()
    def OnSaveSession(self, evt=None):
        from Priithon.all import Y
        Y.saveSession()
    def OnAutoSaveSession(self, evt=None):
        from Priithon.all import Y
        wx.Bell()
        Y.saveSession(autosave=True)

    def OnListVars(self, evt=None):
        from Priithon.all import Y
        Y.listArrayViewer()
    def OnExecPy(self, evt=None):
        from Priithon.all import Y
        fn = wx.FileSelector("Select python file to execute")
        if fn == '':
            return
        import __main__
        try:
            execfile(fn, __main__.__dict__)
        except:
            import sys
            e = sys.exc_info()
            wx.MessageBox("Error on execfile: %s - %s" %\
                          (str(e[0]), str(e[1]) ),
                          "Bad Varname  !?",
                          style=wx.ICON_ERROR)
        else:
            Y.shellMessage("### execfile('%s')\n"%fn)

    def OnCloneShell(self, evt=None):
        from Priithon.all import Y
        Y.shell(clone=True)
    def OnVanimate(self, evt=None):
        from Priithon.all import Y
        Y.vAnimate()
    def OnVplotslider(self, evt=None):
        from Priithon.all import Y
        Y.vPlotAsSliderGUI()

    def OnOSXBug(self, evt=None):
        from Priithon.all import Y
        Y._bugXiGraphics( evt.GetInt() )
#         Y.listArrayViewer()
    #     def OnFileNew(self, event):
    #         self.bufferNew()
    
    #     def OnFileOpen(self, event):
    #         self.bufferOpen()
    
    #     def OnFileRevert(self, event):
    #         self.bufferRevert()
    
    #     def OnFileClose(self, event):
    #         self.bufferClose()
    
    #     def OnFileSave(self, event):
    #         self.bufferSave()
    
    #     def OnFileSaveAs(self, event):
    #         self.bufferSaveAs()
    
    #     def OnFileUpdateNamespace(self, event):
    #         self.updateNamespace()
    
    #     def OnFilePrint(self, event):
    #         self.bufferPrint()
    
    def OnExit(self, event):
        self.Close(False)

    def OnUndo(self, event):
        win = wx.Window_FindFocus()
        win.Undo()

    def OnRedo(self, event):
        win = wx.Window_FindFocus()
        win.Redo()

    #     def OnCut(self, event):
    #         win = wx.Window_FindFocus()
    #         win.Cut()

    def OnCopy(self, event):
        win = wx.Window_FindFocus()
        win.Copy()

    def OnCopyPlus(self, event):
        win = wx.Window_FindFocus()
        win.CopyWithPrompts()

    def OnPaste(self, event):
        win = wx.Window_FindFocus()
        win.Paste()

    def OnPastePlus(self, event):
        win = wx.Window_FindFocus()
        win.PasteAndRun()

    #     def OnClear(self, event):
    #         win = wx.Window_FindFocus()
    #         win.Clear()
    
    #     def OnSelectAll(self, event):
    #         win = wx.Window_FindFocus()
    #         win.SelectAll()
        
    def OnAbout(self, event):
        """Display an About window."""
        title = 'About'
        text = 'Your message here.'
        dialog = wx.MessageDialog(self, text, title,
                                  wx.OK | wx.ICON_INFORMATION)
        dialog.ShowModal()
        dialog.Destroy()

    def OnAutoCompleteShow(self, event):
        win = wx.Window_FindFocus()
        win.autoComplete = event.IsChecked()

    def OnAutoCompleteMagic(self, event):
        win = wx.Window_FindFocus()
        win.autoCompleteIncludeMagic = event.IsChecked()

    def OnAutoCompleteSingle(self, event):
        win = wx.Window_FindFocus()
        win.autoCompleteIncludeSingle = event.IsChecked()

    def OnAutoCompleteDouble(self, event):
        win = wx.Window_FindFocus()
        win.autoCompleteIncludeDouble = event.IsChecked()

    def OnCallTipsShow(self, event):
        win = wx.Window_FindFocus()
        win.autoCallTip = event.IsChecked()

    def OnWrap(self, event):
        win = wx.Window_FindFocus()
        win.SetWrapMode(event.IsChecked())

    def OnUseAA(self, event):
        win = wx.Window_FindFocus()
        win.SetUseAntiAliasing(event.IsChecked())
        
    def OnRaiseWindows(self, event):
        for f in wx.GetTopLevelWindows():
            f.Raise()
    def OnMinimizeWindows(self, event):
        for f in wx.GetTopLevelWindows():
            f.Iconize()

    def OnMarkWindows(self, event):
        try:
            oldLen = len(self._lastUsedMarkerString)
            oldMarker = defaultMarker = self._lastUsedMarkerString
        except AttributeError:
            oldLen = 0
            defaultMarker = '------'

        txt = wx.GetTextFromUser("Enter marker string:", "marker string", defaultMarker)
        if txt and txt[0] != ' ':
            txt = ' ' + txt
            
        for f in wx.GetTopLevelWindows():
            oldTitle = f.GetTitle()
            if oldLen:
                if oldTitle.endswith(oldMarker):
                    oldTitle=oldTitle[:-oldLen]
            f.SetTitle(oldTitle+txt)
        self._lastUsedMarkerString = txt
    def OnTest5(self, event):
        from Priithon.all import Y
        Y.test5()
    def OnTest2(self, event):
        from Priithon.all import Y
        Y.test2()
    def OnTestAll(self, event):
        from Priithon.all import Y
        for i in range(1,7):
            exec "Y.test%d()"%(i,)


    def OnUpdateMenu(self, event):
        """Update menu items based on current status and context."""
        win = wx.Window_FindFocus()
        id = event.GetId()
        event.Enable(True)
        try:
            #seb 20051102            
            #             if id == ID_NEW:
            #                 event.Enable(hasattr(self, 'bufferNew'))
            #             elif id == ID_OPEN:
            #                 event.Enable(hasattr(self, 'bufferOpen'))
            #             elif id == ID_REVERT:
            #                 event.Enable(hasattr(self, 'bufferRevert')
            #                              and self.hasBuffer())
            #             elif id == ID_CLOSE:
            #                 event.Enable(hasattr(self, 'bufferClose')
            #                              and self.hasBuffer())
            #             elif id == ID_SAVE:
            #                 event.Enable(hasattr(self, 'bufferSave')
            #                              and self.bufferHasChanged())
            #             elif id == ID_SAVEAS:
            #                 event.Enable(hasattr(self, 'bufferSaveAs')
            #                              and self.hasBuffer())
            #             elif id == ID_NAMESPACE:
            #                 event.Enable(hasattr(self, 'updateNamespace')
            #                              and self.hasBuffer())
            #             elif id == ID_PRINT:
            #                 event.Enable(hasattr(self, 'bufferPrint')
            #                              and self.hasBuffer())
            if 0: pass
            elif id == ID_UNDO:
                event.Enable(win.CanUndo())
            elif id == ID_REDO:
                event.Enable(win.CanRedo())
            #             elif id == ID_CUT:
            #                 event.Enable(win.CanCut())
            elif id == ID_COPY:
                event.Enable(win.CanCopy())
            elif id == ID_COPY_PLUS:
                event.Enable(win.CanCopy() and hasattr(win, 'CopyWithPrompts'))
            elif id == ID_PASTE:
                event.Enable(win.CanPaste())
            elif id == ID_PASTE_PLUS:
                event.Enable(win.CanPaste() and hasattr(win, 'PasteAndRun'))
            #             elif id == ID_CLEAR:
            #                 event.Enable(win.CanCut())
            #             elif id == ID_SELECTALL:
            #                 event.Enable(hasattr(win, 'SelectAll'))
            elif id == ID_AUTOCOMP_SHOW:
                event.Check(win.autoComplete)
            elif id == ID_AUTOCOMP_MAGIC:
                event.Check(win.autoCompleteIncludeMagic)
            elif id == ID_AUTOCOMP_SINGLE:
                event.Check(win.autoCompleteIncludeSingle)
            elif id == ID_AUTOCOMP_DOUBLE:
                event.Check(win.autoCompleteIncludeDouble)
            elif id == ID_CALLTIPS_SHOW:
                event.Check(win.autoCallTip)
            elif id == ID_WRAP:
                event.Check(win.GetWrapMode())
            elif id == ID_USEAA:
                event.Check(win.GetUseAntiAliasing())
            elif id == ID_OSXBUG:
                from Priithon.viewer import bugXiGraphics
                event.Check(bugXiGraphics)
            else:
                event.Enable(False)
        except AttributeError:
            # This menu option is not supported in the current context.
            event.Enable(False)
