"""Shell is an interactive text control in which a user types in
commands to be sent to the interpreter.  This particular shell is
based on wxPython's wxStyledTextCtrl.

Sponsored by Orbtech - Your source for Python programming expertise."""

__author__ = "Patrick K. O'Brien <pobrien@orbtech.com>"
__cvsid__ = "$Id: shell.py,v 1.9 2004/10/15 20:31:23 RD Exp $"
__revision__ = "$Revision: 1.9 $"[11:-2]

import wx
from wx import stc

import keyword
import os
import sys
import time

from buffer import Buffer
import dispatcher
import editwindow
import frame
from pseudo import PseudoFileIn
from pseudo import PseudoFileOut
from pseudo import PseudoFileErr
from version import VERSION

sys.ps3 = '<-- '  # Input prompt.

NAVKEYS = (wx.WXK_END, wx.WXK_LEFT, wx.WXK_RIGHT,
           wx.WXK_UP, wx.WXK_DOWN, wx.WXK_PRIOR, wx.WXK_NEXT)

NO_SPECIAL_GUI_EXCEPT = True # instead rely on Priithon's guiExceptionFrame (Y._fixGuiExceptHook())

class ShellFrame(frame.Frame):
    """Frame containing the shell component."""

    name = 'Shell Frame'
    revision = __revision__

    def __init__(self, parent=None, id=-1, title='PyShell',
                 pos=wx.DefaultPosition, size=wx.DefaultSize,
                 style=wx.DEFAULT_FRAME_STYLE, locals=None,
                 InterpClass=None,
                 introText='', #seb
                 introStatus='', #seb
                 *args, **kwds):
        """Create ShellFrame instance."""
        frame.Frame.__init__(self, parent, id, title, pos, size, style)
        #seb intro = 'PyShell %s - The Flakiest Python Shell' % VERSION
        #seb intro += '\nSponsored by Orbtech - ' + \
        #seb          'Your source for Python programming expertise.'
        #seb self.SetStatusText(intro.replace('\n', ', '))
        self.SetStatusText(introStatus)
        self.shell = Shell(parent=self, id=-1, introText=introText,
                           locals=locals, InterpClass=InterpClass,
                           *args, **kwds)
        # Override the shell so that status messages go to the status bar.
        self.shell.setStatusText = self.SetStatusText

    def OnClose(self, event):
        """Event handler for closing."""
        #
        #before2007: This isn't working the way I want, but I'll leave it for now.

        #20070712 sebVeto
        sebVeto = False
        self.IwantToClose_hack = True # 20080730: otherwise we get into a circle if multiple shell windows are open
        if len(wx.GetTopLevelWindows())>1:
            r= wx.MessageBox("close all other windows ?", 
                             "other open windows !", 
                             style=wx.CENTER|wx.YES_NO|wx.CANCEL|wx.ICON_EXCLAMATION)
            if r == wx.YES:
                for f in wx.GetTopLevelWindows():
                    if (f is not self and (not hasattr(f, "IwantToClose_hack")
                            or not f.IwantToClose_hack)):
                        f.Close()
            elif r == wx.CANCEL:
                self.IwantToClose_hack = False # 20080730 
                sebVeto = True

        if self.shell.waiting or sebVeto:
            if event.CanVeto():
                event.Veto(True)
        else:
            self.shell.destroy()
            self.Destroy()

    def OnAbout(self, event):
        """Display an About window."""
        '''#20091113 seb
        title = 'About PyShell'
        text = 'PyShell %s\n\n' % VERSION + \
               'Yet another Python shell, only flakier.\n\n' + \
               'Half-baked by Patrick K. O\'Brien,\n' + \
               'the other half is still in the oven.\n\n' + \
               'Shell Revision: %s\n' % self.shell.revision + \
               'Interpreter Revision: %s\n\n' % self.shell.interp.revision + \

               'Platform: %s\n' % sys.platform + \
               'Python Version: %s\n' % sys.version.split()[0] + \
               'wxPython Version: %s\n' % wx.VERSION_STRING #sebwx24+ \
                #sebwx24 ('\t(%s)\n' % ", ".join(wx.PlatformInfo[1:]))

        try:#sebwx24
            text += ('\t(%s)\n' % ", ".join(wx.PlatformInfo[1:]))
        except:
            pass
            '''
        
        try:
            import os, glob, stat, operator, time
            from Priithon import useful as U
            d = os.path.dirname(U.__file__)
            ff = glob.glob(os.path.join(d, '*.py'))
            ffdates  = [(f,os.stat(os.path.join(d, f))[stat.ST_MTIME]) for f in ff]
            ffdates.sort(key=operator.itemgetter(1), reverse=True)
            pyfn   = [os.path.basename(f[0]) for f in ffdates[:3]]
            pydate = [time.ctime(f[1]) for f in ffdates[:3]]
        except:  # in case files are not found 
            pyfn = ['???']*3
            pydate = ['???']*3
        try:
            import os # , glob, stat, operator, time
            from Priithon import useful as U
            d = os.path.dirname(U.__file__)
            priDir = d
        except:
            priDir = '???'

        title = "About Priithon"
        text = """
Priithon is a open source platform 
for multi dimensional image analysis 
and algorithm development. 

Priithon is a collection of many other open source projects.
Most Priithon-specific code has been 
written by Sebastian Haase.

Priithon is hosted at
http://code.google.com/p/priithon

The wx python py-shell was originally written by Patrick K. O\'Brien

"""+ (      'Priithon version: the 3 newest py files are\n' +
            '\t\'%s\' dated %s\n'%(pyfn[0],pydate[0]) +
            '\t\'%s\' dated %s\n'%(pyfn[1],pydate[1]) +
            '\t\'%s\' dated %s\n'%(pyfn[2],pydate[2]) +
            'Priithon package base dir:\n\t\'%s\'\n'%(priDir,) +
            '\n' +
            'Platform: %s\n' % sys.platform +
            'Python Version: %s\n' % sys.version.split()[0] +
            'wxPython Version: %s\n' % wx.VERSION_STRING + 
            '\t(%s)\n' % ", ".join(wx.PlatformInfo[1:])
            )
        

        dialog = wx.MessageDialog(self, text, title,
                                  wx.OK | wx.ICON_INFORMATION)
        dialog.ShowModal()
        dialog.Destroy()


class ShellFacade:
    """Simplified interface to all shell-related functionality.

    This is a semi-transparent facade, in that all attributes of other
    are accessible, even though only some are visible to the user."""

    name = 'Shell Interface'
    revision = __revision__

    def __init__(self, other):
        """Create a ShellFacade instance."""
        d = self.__dict__
        d['other'] = other
        d['helpText'] = \
"""
* Key bindings:
Home or Ctrl+A    Go to the beginning of the command or line.
Shift+Home        Select to the beginning of the command or line.
Shift+End         Select to the end of the line.
End  or Ctrl+E    Go to the end of the line.
Ctrl+C            Copy selected text, removing prompts.
Ctrl+Shift+C      Copy selected text, retaining prompts.
Ctrl+X            Cut selected text.
Ctrl+V            Paste from clipboard.
Ctrl+Shift+V      Paste and run multiple commands from clipboard.
Ctrl+Up Arrow     Retrieve Previous History item.
Alt+P             Retrieve Previous History item.
Ctrl+Down Arrow   Retrieve Next History item.
Alt+N             Retrieve Next History item.
F8   or Ctrl+R    Command-completion of History item.
                  (Type a few characters of a previous command and press F8.)
Ctrl+Enter        Insert new line into multiline command.
Ctrl+]            Increase font size.
Ctrl+[            Decrease font size.
Ctrl+=            Default font size.
Ctrl+f            Search (backwards) TODO: regexp-wholeWords-...
Ctrl+g            Search next
Ctrl+h            "hide" lines containing selection / "unhide" 
F12 or Ctrl+n     on/off "free-edit" (notebook) mode
"""
#seb: to allow convinient "hide"-selection
#seb took this out Shift+Up Arrow    Insert Previous History item.
#seb took this out Shift+Down Arrow  Insert Next History item.

    def help(self):
        """Display some useful information about how to use the shell."""
        self.write(self.helpText)

    def __getattr__(self, name):
        if hasattr(self.other, name):
            return getattr(self.other, name)
        else:
            raise AttributeError, name

    def __setattr__(self, name, value):
        if self.__dict__.has_key(name):
            self.__dict__[name] = value
        elif hasattr(self.other, name):
            setattr(self.other, name, value)
        else:
            raise AttributeError, name

    def _getAttributeNames(self):
        """Return list of magic attributes to extend introspection."""
        list = [
            'about',
            'ask',
            'autoCallTip',
            'autoComplete',
            'autoCompleteAutoHide',
            'autoCompleteCaseInsensitive',
            'autoCompleteIncludeDouble',
            'autoCompleteIncludeMagic',
            'autoCompleteIncludeSingle',
            'clear',
            'pause',
            'prompt',
            'quit',
            'redirectStderr',
            'redirectStdin',
            'redirectStdout',
            'run',
            'runfile',
            'wrap',
            'zoom',
            ]
        list.sort()
        return list


class Shell(editwindow.EditWindow):
    """Shell based on StyledTextCtrl."""

    name = 'Shell'
    revision = __revision__

    def __init__(self, parent, id=-1, pos=wx.DefaultPosition,
                 size=wx.DefaultSize, style=wx.CLIP_CHILDREN,
                 introText='', locals=None, InterpClass=None, *args, **kwds):
        """Create Shell instance."""
        editwindow.EditWindow.__init__(self, parent, id, pos, size, style)
        self.wrap()
        if locals is None:
            import __main__
            locals = __main__.__dict__
        # Grab these so they can be restored by self.redirect* methods.
        self.stdin = sys.stdin
        self.stdout = sys.stdout
        self.stderr = sys.stderr
        # Import a default interpreter class if one isn't provided.
        if InterpClass == None:
            from interpreter import Interpreter
        else:
            Interpreter = InterpClass
        # Create a replacement for stdin.
        self.reader = PseudoFileIn(self.readline, self.readlines)
        self.reader.input = ''
        self.reader.isreading = False
        # Set up the interpreter.
        self.interp = Interpreter(locals=locals,
                                  rawin=self.raw_input,
                                  stdin=self.reader,
                                  stdout=PseudoFileOut(self.writeOut),
                                  stderr=PseudoFileErr(self.writeErr),
                                  *args, **kwds)
        # Set up the buffer.
        self.buffer = Buffer()
        # Find out for which keycodes the interpreter will autocomplete.
        self.autoCompleteKeys = self.interp.getAutoCompleteKeys()
        # Keep track of the last non-continuation prompt positions.
        self.promptPosStart = 0
        self.promptPosEnd = 0
        # Keep track of multi-line commands.
        self.more = False
        # Create the command history.  Commands are added into the
        # front of the list (ie. at index 0) as they are entered.
        # self.historyIndex is the current position in the history; it
        # gets incremented as you retrieve the previous command,
        # decremented as you retrieve the next, and reset when you hit
        # Enter.  self.historyIndex == -1 means you're on the current
        # command, not in the history.
        self.history = []
        self.historyIndex = -1

        #seb add mode for "free edit"
        self.sebNoteMode = 0
        self.MarkerDefine(0,stc.STC_MARK_ROUNDRECT)  # seb's marker for hidden
        self.searchTxt = ""

        #20070927: seb:  make Ctrl-D behave like DELETE (unix/emacs) - default was: duplicate line
        self.CmdKeyAssign(ord('D'), wx.stc.STC_SCMOD_CTRL, wx.stc.STC_CMD_CLEAR)


        # Assign handlers for keyboard events.
        wx.EVT_CHAR(self, self.OnChar)
        wx.EVT_KEY_DOWN(self, self.OnKeyDown)
        # Assign handler for idle time.
        self.waiting = False
        wx.EVT_IDLE(self, self.OnIdle)
        # Display the introductory banner information.
        self.showIntro(introText)
        #seb 20070126  # Assign some pseudo keywords to the interpreter's namespace.
        #seb 20070126  self.setBuiltinKeywords()
        # Add 'shell' to the interpreter's local namespace.
        if not self.interp.locals.has_key('shell'): # 20080729: added "if"
            self.setLocalShell()

        # Do this last so the user has complete control over their
        # environment.  They can override anything they want.
        self.execStartupScript(self.interp.startupScript)
        wx.CallAfter(self.ScrollToLine, 0)

        ##seb: File drag and drop
        from Priithon import fileDropPopup
        self.SetDropTarget( fileDropPopup.FileDropTarget(self, self) )


    def destroy(self):
        del self.interp

    def setFocus(self):
        """Set focus to the shell."""
        self.SetFocus()

    def OnIdle(self, event):
        """Free the CPU to do other things."""
        if self.waiting:
            time.sleep(0.05)
        event.Skip()

    def showIntro(self, text=''):
        """Display introductory text in the shell."""
        if text:
            #seb if not text.endswith(os.linesep):
            #seb      text += os.linesep
            #seb note:  here the next command is push()(in execStartupScript)(which starts with '\n')
            self.write(text)
        try:
            self.write(self.interp.introText)
        except AttributeError:
            pass

    #seb 20070126   this now not used anymore
    def setBuiltinKeywords(self):
        """Create pseudo keywords as part of builtins.

        This sets `close`, `exit` and `quit` to a helpful string.
        """
        import __builtin__
        __builtin__.close = __builtin__.exit = __builtin__.quit = \
            'Click on the close button to leave the application.'

    def quit(self):
        """Quit the application."""

        # XXX Good enough for now but later we want to send a close event.

        # In the close event handler we can make sure they want to
        # quit.  Other applications, like PythonCard, may choose to
        # hide rather than quit so we should just post the event and
        # let the surrounding app decide what it wants to do.
        self.write('Click on the close button to leave the application.')

    def setLocalShell(self):
        """Add 'shell' to locals as reference to ShellFacade instance."""
        self.interp.locals['shell'] = ShellFacade(other=self)

    def execStartupScript(self, startupScript):
        """Execute the user's PYTHONSTARTUP script if they have one."""
        if startupScript and os.path.isfile(startupScript):
            text = 'Startup script executed: ' + startupScript
            self.push('print %r; execfile(%r)' % (text, startupScript))
        else:
            self.push('')

    def about(self):
        """Display information about Py."""
        text = """
Author: %r
Py Version: %s
Py Shell Revision: %s
Py Interpreter Revision: %s
Python Version: %s
wxPython Version: %s
Platform: %s""" % \
        (__author__, VERSION, self.revision, self.interp.revision,
         sys.version.split()[0], wx.VERSION_STRING, sys.platform)
        self.write(text.strip())

    def OnChar(self, event):
        """Keypress event handler.

        Only receives an event if OnKeyDown calls event.Skip() for the
        corresponding event."""

        #seb
        if self.sebNoteMode:
            event.Skip()
            return
        # Prevent modification of previously submitted
        # commands/responses.
        if not self.CanEdit():
            return
        key = event.GetKeyCode()
        currpos = self.GetCurrentPos()
        stoppos = self.promptPosEnd
        # Return (Enter) needs to be ignored in this handler.
        if key == wx.WXK_RETURN:
            pass
        elif key in self.autoCompleteKeys:
            # Usually the dot (period) key activates auto completion.
            # Get the command between the prompt and the cursor.  Add
            # the autocomplete character to the end of the command.
            if self.AutoCompActive():
                self.AutoCompCancel()
            command = self.GetTextRange(stoppos, currpos) + chr(key)
            self.write(chr(key))
            if self.autoComplete:
                self.autoCompleteShow(command)
        elif key == ord('('):
            # The left paren activates a call tip and cancels an
            # active auto completion.
            if self.AutoCompActive():
                self.AutoCompCancel()
            # Get the command between the prompt and the cursor.  Add
            # the '(' to the end of the command.
            self.ReplaceSelection('')
            command = self.GetTextRange(stoppos, currpos) + '('
            self.write('(')
            self.autoCallTipShow(command)
        else:
            # Allow the normal event handling to take place.
            event.Skip()

    def OnKeyDown(self, event):
        """Key down event handler."""

        key = event.GetKeyCode()
        # If the auto-complete window is up let it do its thing.
        if self.AutoCompActive():
            event.Skip()
            return
        # Prevent modification of previously submitted
        # commands/responses.
        controlDown = event.CmdDown() or event.ControlDown() # 20080407: added CmdDown
        altDown = event.AltDown()
        shiftDown = event.ShiftDown()
        currpos = self.GetCurrentPos()
        endpos = self.GetTextLength()
        selecting = self.GetSelectionStart() != self.GetSelectionEnd()
        # Return (Enter) is used to submit a command to the
        # interpreter.

        #seb
        #noSebFreeMode = not self.sebNoteMode:
        if controlDown and key in (ord('F'), ord('f')): # pressing 'f' gives 'F' on Windows
            dialog = wx.TextEntryDialog(None, "search for:",
                                    'search', '')
            try:
                if dialog.ShowModal() == wx.ID_OK:
                    txt=self.searchTxt = dialog.GetValue()
                    l=len(txt)
                    #search-forward self.SetTargetStart(0)
                    #search-forward self.SetTargetEnd  (self.GetTextLength())
                    self.SetTargetStart(self.GetTextLength())
                    self.SetTargetEnd  (0)
                    pp = self.SearchInTarget( txt )
                    #self.SetCurrentPos( pp )
                    #search-forward self.SetSelection(pp,pp+l)
                    self.SetSelection(pp+l,pp)
            finally:
                dialog.Destroy()
            return
        if controlDown and key in (ord('G'), ord('g')): # pressing 'f' gives 'F' on Windows
            txt=self.searchTxt
            l=len(txt)
            pp = self.GetCurrentPos();
            #search-forward self.SetSelection(pp,pp)
            self.SetSelection(pp-l,pp-l)
            self.SearchAnchor()
            #search-forward pp = self.SearchNext(0, txt)
            pp = self.SearchPrev(0, txt)
            #self.SetCurrentPos( pp )
            #search-forward self.SetSelection(pp,pp+l)
            self.SetSelection(pp+l,pp)
            return
        if controlDown and key in (ord('H'), ord('h')): # pressing 'f' gives 'F' on Windows
            li = self.GetCurrentLine()
            m = self.MarkerGet(li)
            if m & 1<<0:
                startP = self.PositionFromLine(li)
                self.MarkerDelete(li, 0)
                maxli = self.GetLineCount()
                li += 1 # li stayed visible as header-line
                li0 = li 
                while li<maxli and self.GetLineVisible(li) == 0:
                    li += 1
                endP = self.GetLineEndPosition(li-1)
                self.ShowLines(li0, li-1)
                self.SetSelection( startP, endP ) # select reappearing text to allow "hide again"
                return
            startP,endP = self.GetSelection()
            endP-=1
            startL,endL = self.LineFromPosition(startP), self.LineFromPosition(endP)

            if endL == self.LineFromPosition(self.promptPosEnd): # never hide last prompt
                endL -= 1

            m = self.MarkerGet(startL)
            self.MarkerAdd(startL, 0)
            self.HideLines(startL+1,endL)
            self.SetCurrentPos( startP ) # to ensure caret stays visible !

        if key == wx.WXK_F12 or controlDown and key in (ord('N'), ord('n')): #seb
            if self.sebNoteMode:
                # self.promptPosStart not used anyway - or ? 
                self.promptPosEnd = self.PositionFromLine( self.GetLineCount()-1 ) + len(str(sys.ps1))
                self.SetCaretForeground("black")
                self.SetCaretWidth(1)    #default
                self.SetCaretPeriod(500) #default
            else:
                self.SetCaretForeground("red")
                self.SetCaretWidth(4)
                self.SetCaretPeriod(0) #steady

            self.sebNoteMode = not self.sebNoteMode
            #seb print "self.sebNoteMode=", self.sebNoteMode
            return
        if self.sebNoteMode:
            event.Skip()
            return

        if not controlDown and key == wx.WXK_RETURN:
            if self.CallTipActive():
                self.CallTipCancel()
            self.processLine()
        # Ctrl+Return (Cntrl+Enter) is used to insert a line break.
        elif controlDown and key == wx.WXK_RETURN:
            if self.CallTipActive():
                self.CallTipCancel()
            #seb 20070106 if currpos == endpos:
            #seb 20070106     self.processLine()
            #seb 20070106 else:
            self.insertLineBreak() # seb: insert always
        # Let Ctrl-Alt-* get handled normally.
        elif controlDown and altDown:
            event.Skip()
        # Clear the current, unexecuted command.
        elif key == wx.WXK_ESCAPE:
            if self.CallTipActive():
                event.Skip()
            else:
                self.clearCommand()

        #seb 20070106: autocompletion 
        elif not controlDown and key == wx.WXK_TAB:
            #wx.Bell()
            if self.AutoCompActive():
                self.AutoCompCancel()

            stoppos = self.promptPosEnd
            command = self.GetTextRange(stoppos, currpos)
            #self.autoCompleteShow(command)

            if len(command) and command[-1] in ('(',):
                self.ReplaceSelection('')
                self.autoCallTipShow(command, alwaysShow=True)
            else:
                import introspect, __main__, __builtin__
                root = introspect.getRoot(command)
                if self.more and root=='': # pressing TAB to indent multi-line commands
                    event.Skip()
                    return                           


                #print >> __main__.shell.stderr, "DEBUG root:", root
                #print >> __main__.shell.stderr, "DEBUG command:", command
                #print >> __main__.shell.stderr, "DEBUG command tokens:", '\n'.join(map(str,introspect.getTokens(command)))
                # 20080908:  experiment with argument name completion
                if root=='' and command:
                    beforeParenthesis = command.rpartition('(')[0]
                    if beforeParenthesis:
                        #print >> __main__.shell.stderr, "DEBUG beforeParenthesis:", beforeParenthesis
                        try:
                            object = eval(beforeParenthesis, __main__.__dict__)
                        except:
                            #for debugging
                            pass
                            #import traceback
                            #traceback.print_exc(file=__main__.shell.stderr)
                        else:
                            import inspect
                            (args, varargs, varkw, defaults)=inspect.getargspec(object)
                            if  varargs is not None:
                                args.append( varargs )
                            if  varkw is not None:
                                args.append( varkw )
                            #print >> __main__.shell.stderr, ' '.join(args)
                            options = ' '.join([(s+'=') for s in args])
                            offset=0
                            self.AutoCompShow(offset, options)
                else: # 20080908


                    hasDot = root.rfind('.')
                    if hasDot>=0:
                        self.autoCompleteShow(command, offset=len(root)-hasDot-1)
                    else:
                        rootLower = root.lower()
                        _list = [s for s in __main__.__dict__ if s.lower().startswith(rootLower)]
                        _list.sort()

                        _list2 = [s for s in __builtin__.__dict__ if s.lower().startswith(rootLower)]
                        _list2.sort()

                        # first matches from __main__ then from __builtin__
                        #   TODO: add separator between the two
                        #if len(_list):
                        #    _list3 = _list + [] + _list2
                        #else:
                        #    _list3 = _list2
                        if len(_list) or len(_list2):
                            _list3 = _list + ['=====__builtins__:'] + _list2

                            options = ' '.join(_list3)
                            offset = len(root)
                            self.AutoCompShow(offset, options)
                            #if self.GetCurrentPos()<self.promptPosEnd:
                            #    #self.SetCurrentPos(self.promptPosEnd+1)
                            #    self.AppendText(' ')

        # Increase font size.
        elif controlDown and key in (ord(']'),):
            dispatcher.send(signal='FontIncrease')
        # Decrease font size.
        elif controlDown and key in (ord('['),):
            dispatcher.send(signal='FontDecrease')
        # Default font size.
        elif controlDown and key in (ord('='),):
            dispatcher.send(signal='FontDefault')
        # Cut to the clipboard.
        elif (controlDown and key in (ord('X'), ord('x'))) \
        or (shiftDown and key == wx.WXK_DELETE):
            self.Cut()
        # Copy to the clipboard.
        elif controlDown and not shiftDown \
            and key in (ord('C'), ord('c'), wx.WXK_INSERT):
            self.Copy()
        # Copy to the clipboard, including prompts.
        elif controlDown and shiftDown \
            and key in (ord('C'), ord('c'), wx.WXK_INSERT):
            self.CopyWithPrompts()
        # Copy to the clipboard, including prefixed prompts.
        elif altDown and not controlDown \
            and key in (ord('C'), ord('c'), wx.WXK_INSERT):
            self.CopyWithPromptsPrefixed()
        elif controlDown and key in (ord('E'), ord('e')):#20051104 seb
            event.m_controlDown = False
            event.m_keyCode = wx.WXK_END
            event.Skip()
            return                     
        # Home needs to be aware of the prompt.
        elif key == wx.WXK_HOME \
                 or controlDown and key in (ord('A'), ord('a')):#20051104 seb
            home = self.promptPosEnd
            if currpos >= home: # 20051101 '>' changed to '>='
                self.SetCurrentPos(home)
                if not selecting and not shiftDown:
                    self.SetAnchor(home)
                    self.EnsureCaretVisible()
            else:
                event.m_controlDown = False#20051104 seb
                event.m_keyCode = wx.WXK_HOME#20051104 seb
                event.Skip()
        #
        # The following handlers modify text, so we need to see if
        # there is a selection that includes text prior to the prompt.
        #
        # Don't modify a selection with text prior to the prompt.
        elif selecting and key not in NAVKEYS and not self.CanEdit():
            pass
        # Paste from the clipboard.
        elif (controlDown and not shiftDown and key in (ord('V'), ord('v'))) \
                 or (shiftDown and not controlDown and key == wx.WXK_INSERT):
            self.Paste()
        # Paste from the clipboard, run commands.
        elif controlDown and shiftDown and key in (ord('V'), ord('v')):
            self.PasteAndRun()
        # Replace with the previous command from the history buffer.
        elif (controlDown and key == wx.WXK_UP) \
                 or (altDown and key in (ord('P'), ord('p'))):
            self.OnHistoryReplace(step=+1)
        # Replace with the next command from the history buffer.
        elif (controlDown and key == wx.WXK_DOWN) \
                 or (altDown and key in (ord('N'), ord('n'))):
            self.OnHistoryReplace(step=-1)
#seb took this out         # Insert the previous command from the history buffer.
#seb took this out         elif (shiftDown and key == wx.WXK_UP) and self.CanEdit():
#seb took this out             self.OnHistoryInsert(step=+1)
#seb took this out         # Insert the next command from the history buffer.
#seb took this out         elif (shiftDown and key == wx.WXK_DOWN) and self.CanEdit():
#seb took this out             self.OnHistoryInsert(step=-1)
#seb took this out         # Search up the history for the text in front of the cursor.
        elif key == wx.WXK_F8 \
                 or controlDown and key in (ord('R'), ord('r')):#20051104 seb
            self.OnHistorySearch()
        # Don't backspace over the latest non-continuation prompt.
        elif key == wx.WXK_BACK:
            if selecting and self.CanEdit():
                event.Skip()
            elif currpos > self.promptPosEnd:
                event.Skip()
        # Only allow these keys after the latest prompt.
        elif key in (wx.WXK_TAB, wx.WXK_DELETE):
            if self.CanEdit():
                event.Skip()
        #seb 20070106 # Don't toggle between insert mode and overwrite mode.
        #seb 20070106 elif key == wx.WXK_INSERT:
        #seb 20070106     pass
        # Don't allow line deletion.
        elif controlDown and key in (ord('L'), ord('l')):
            pass
        # Don't allow line transposition.
        elif controlDown and key in (ord('T'), ord('t')):
            pass
        # Basic navigation keys should work anywhere.
        elif key in NAVKEYS:
            event.Skip()
        # Protect the readonly portion of the shell.
        elif not self.CanEdit():
            pass
        else:
            event.Skip()

    def clearCommand(self):
        """Delete the current, unexecuted command."""
        startpos = self.promptPosEnd
        endpos = self.GetTextLength()
        self.SetSelection(startpos, endpos)
        self.ReplaceSelection('')
        self.more = False

    def OnHistoryReplace(self, step):
        """Replace with the previous/next command from the history buffer."""

        #seb F8 is too clumsy... CHECK if we can call OnHistorySearch
        #seb                IF there are some character already typed !?
        #fixme: for empty line would only work once - then alway go
        #   into OnHistorySearch mode
        if 1: # self.GetTextLength() == self.promptPosEnd:
            self.clearCommand()
            self.replaceFromHistory(step)
        else:
            self.OnHistorySearch()
        #only two original line here:  self.clearCommand()
        #only two original line here:  self.replaceFromHistory(step)

    def replaceFromHistory(self, step):
        """Replace selection with command from the history buffer."""
        ps2 = str(sys.ps2)
        self.ReplaceSelection('')
        newindex = self.historyIndex + step
        if -1 <= newindex <= len(self.history):
            self.historyIndex = newindex
        if 0 <= newindex <= len(self.history)-1:
            command = self.history[self.historyIndex]
            command = command.replace('\n', os.linesep + ps2)
            self.ReplaceSelection(command)

    def OnHistoryInsert(self, step):
        """Insert the previous/next command from the history buffer."""
        if not self.CanEdit():
            return
        startpos = self.GetCurrentPos()
        self.replaceFromHistory(step)
        endpos = self.GetCurrentPos()
        self.SetSelection(endpos, startpos)

    def OnHistorySearch(self):
        """Search up the history buffer for the text in front of the cursor."""
        if not self.CanEdit():
            return
        startpos = self.GetCurrentPos()

        #seb
        if self.GetTextLength() != self.GetSelectionEnd():
            return #seb otherwise it would fill history stuff in - probably  unexpected !

        # The text up to the cursor is what we search for.
        numCharsAfterCursor = self.GetTextLength() - startpos
        searchText = self.getCommand(rstrip=False)
        if numCharsAfterCursor > 0:
            searchText = searchText[:-numCharsAfterCursor]
        if not searchText:
            return
        # Search upwards from the current history position and loop
        # back to the beginning if we don't find anything.
        if (self.historyIndex <= -1) \
        or (self.historyIndex >= len(self.history)-2):
            searchOrder = range(len(self.history))
        else:
            searchOrder = range(self.historyIndex+1, len(self.history)) + \
                          range(self.historyIndex)
        for i in searchOrder:
            command = self.history[i]
            if command[:len(searchText)] == searchText:
                # Replace the current selection with the one we found.
                self.ReplaceSelection(command[len(searchText):])
                endpos = self.GetCurrentPos()
                self.SetSelection(endpos, startpos)
                # We've now warped into middle of the history.
                self.historyIndex = i
                break

    def setStatusText(self, text):
        """Display status information."""

        # This method will likely be replaced by the enclosing app to
        # do something more interesting, like write to a status bar.
        print text

    def insertLineBreak(self):
        """Insert a new line break."""
        if self.CanEdit():
            self.write(os.linesep)
            self.more = True
            self.prompt()

    def processLine(self):
        """Process the line of text at which the user hit Enter."""

        # The user hit ENTER and we need to decide what to do. They
        # could be sitting on any line in the shell.

        thepos = self.GetCurrentPos()
        startpos = self.promptPosEnd
        endpos = self.GetTextLength()
        ps2 = str(sys.ps2)
        # If they hit RETURN inside the current command, execute the
        # command.
        if self.CanEdit():
            self.SetCurrentPos(endpos)
            self.interp.more = False
            command = self.GetTextRange(startpos, endpos)
            lines = command.split(os.linesep + ps2)
            lines = [line.rstrip() for line in lines]
            command = '\n'.join(lines)

            # seb: 20100121 - first attempt to make a os.system *magic* - just start line with a 'space'
            if len(command)>1 and command[0] == ' ':
                from Priithon import useful as U
                #self.SetCurrentPos(thepos)
                #self.SetAnchor(thepos)
                self.write(os.linesep)
                try:
                    command_1 = command.strip()
                    suppress_output = command_1[-1] in ("#",";")
                    if suppress_output:
                        command_1 = command_1[:-1]
                        
                    ret = U.exe( command_1 )
                except OSError, e:
                    self.write("# " + repr(e) + os.linesep)
                else:
                    if ret and not suppress_output:
                        self.write(os.linesep.join(ret) + os.linesep)
                    import __main__
                    __main__._ = ret
                self.addHistory(command)
                self.prompt()
                return
            if self.reader.isreading:
                if not command:
                    # Match the behavior of the standard Python shell
                    # when the user hits return without entering a
                    # value.
                    command = '\n'
                self.reader.input = command
                self.write(os.linesep)
            else:
                self.push(command)
        # Or replace the current command with the other command.
        else:
            # If the line contains a command (even an invalid one).
            if self.getCommand(rstrip=False):
                command = self.getMultilineCommand()
                self.clearCommand()
                self.write(command)
            # Otherwise, put the cursor back where we started.
            else:
                self.SetCurrentPos(thepos)
                self.SetAnchor(thepos)

    def getMultilineCommand(self, rstrip=True):
        """Extract a multi-line command from the editor.

        The command may not necessarily be valid Python syntax."""
        # XXX Need to extract real prompts here. Need to keep track of
        # the prompt every time a command is issued.
        ps1 = str(sys.ps1)
        ps1size = len(ps1)
        ps2 = str(sys.ps2)
        ps2size = len(ps2)
        # This is a total hack job, but it works.
        text = self.GetCurLine()[0]
        line = self.GetCurrentLine()
        while text[:ps2size] == ps2 and line > 0:
            line -= 1
            self.GotoLine(line)
            text = self.GetCurLine()[0]
        if text[:ps1size] == ps1:
            line = self.GetCurrentLine()
            self.GotoLine(line)
            startpos = self.GetCurrentPos() + ps1size
            line += 1
            self.GotoLine(line)
            while self.GetCurLine()[0][:ps2size] == ps2:
                line += 1
                self.GotoLine(line)
            stoppos = self.GetCurrentPos()
            command = self.GetTextRange(startpos, stoppos)
            command = command.replace(os.linesep + ps2, '\n')
            command = command.rstrip()
            command = command.replace('\n', os.linesep + ps2)
        else:
            command = ''
        if rstrip:
            command = command.rstrip()
        return command

    def getCommand(self, text=None, rstrip=True):
        """Extract a command from text which may include a shell prompt.

        The command may not necessarily be valid Python syntax."""
        if not text:
            text = self.GetCurLine()[0]
        # Strip the prompt off the front leaving just the command.
        command = self.lstripPrompt(text)
        if command == text:
            command = ''  # Real commands have prompts.
        if rstrip:
            command = command.rstrip()
        return command

    def lstripPrompt(self, text):
        """Return text without a leading prompt."""
        ps1 = str(sys.ps1)
        ps1size = len(ps1)
        ps2 = str(sys.ps2)
        ps2size = len(ps2)
        # Strip the prompt off the front of text.
        if text[:ps1size] == ps1:
            text = text[ps1size:]
        elif text[:ps2size] == ps2:
            text = text[ps2size:]
        return text

    #20070723: seb added newPrompt - to allow "externally triggert exec of commands, without new pompt)
    def push(self, command, newPrompt=True):
        """Send command to the interpreter for execution."""

        if newPrompt == 'ifNeeded':
            endpos = self.GetTextLength()
        elif newPrompt:
            self.write(os.linesep)
        busy = wx.BusyCursor()
        self.waiting = True
        self.more = self.interp.push(command)
        self.waiting = False
        del busy
        if not self.more:
            self.addHistory(command.rstrip())
        if newPrompt is True:
            self.prompt()
        elif newPrompt == 'ifNeeded':
            if endpos < self.GetTextLength():
                self.prompt()

    def addHistory(self, command):
        """Add command to the command history."""
        # Reset the history position.
        self.historyIndex = -1
        # Insert this command into the history, unless it's a blank
        # line or the same as the last command.
        if command != '' \
        and (len(self.history) == 0 or command != self.history[0]):
            self.history.insert(0, command)

    def write(self, text):
        """Display text in the shell.

        Replace line endings with OS-specific endings."""
        text = self.fixLineEndings(text)
        self.AddText(text)
        self.EnsureCaretVisible()

    def fixLineEndings(self, text):
        """Return text with line endings replaced by OS-specific endings."""
        lines = text.split('\r\n')
        for l in range(len(lines)):
            chunks = lines[l].split('\r')
            for c in range(len(chunks)):
                chunks[c] = os.linesep.join(chunks[c].split('\n'))
            lines[l] = os.linesep.join(chunks)
        text = os.linesep.join(lines)
        return text

    def prompt(self):
        """Display proper prompt for the context: ps1, ps2 or ps3.

        If this is a continuation line, autoindent as necessary."""
        isreading = self.reader.isreading
        skip = False
        if isreading:
            prompt = str(sys.ps3)
        elif self.more:
            prompt = str(sys.ps2)
        else:
            prompt = str(sys.ps1)
        pos = self.GetCurLine()[1]
        if pos > 0:
            if isreading:
                skip = True
            else:
                self.write(os.linesep)
        if not self.more:
            self.promptPosStart = self.GetCurrentPos()
        if not skip:
            self.write(prompt)
        if not self.more:
            self.promptPosEnd = self.GetCurrentPos()
            # Keep the undo feature from undoing previous responses.
            self.EmptyUndoBuffer()
        # XXX Add some autoindent magic here if more.
        if self.more:
            self.write(' '*4)  # Temporary hack indentation.
        self.EnsureCaretVisible()
        self.ScrollToColumn(0)

    def readline(self):
        """Replacement for stdin.readline()."""
        input = ''
        reader = self.reader
        reader.isreading = True
        self.prompt()
        try:
            while not reader.input:
                wx.YieldIfNeeded()
            input = reader.input
        finally:
            reader.input = ''
            reader.isreading = False
        input = str(input)  # In case of Unicode.
        return input

    def readlines(self):
        """Replacement for stdin.readlines()."""
        lines = []
        while lines[-1:] != ['\n']:
            lines.append(self.readline())
        return lines

    def raw_input(self, prompt=''):
        """Return string based on user input."""
        if prompt:
            self.write(prompt)
        return self.readline()

    def ask(self, prompt='Please enter your response:'):
        """Get response from the user using a dialog box."""
        dialog = wx.TextEntryDialog(None, prompt,
                                    'Input Dialog (Raw)', '')
        try:
            if dialog.ShowModal() == wx.ID_OK:
                text = dialog.GetValue()
                return text
        finally:
            dialog.Destroy()
        return ''

    def pause(self):
        """Halt execution pending a response from the user."""
        self.ask('Press enter to continue:')

    def clear(self):
        """Delete all text from the shell."""
        self.ClearAll()

    def run(self, command, prompt=True, verbose=True):
        """Execute command as if it was typed in directly.
        >>> shell.run('print "this"')
        >>> print "this"
        this
        >>>
        """
        # Go to the very bottom of the text.
        endpos = self.GetTextLength()
        self.SetCurrentPos(endpos)
        command = command.rstrip()
        if prompt: self.prompt()
        if verbose: self.write(command)
        self.push(command)

    def runfile(self, filename):
        """Execute all commands in file as if they were typed into the
        shell."""
        file = open(filename)
        try:
            self.prompt()
            for command in file.readlines():
                if command[:6] == 'shell.':
                    # Run shell methods silently.
                    self.run(command, prompt=False, verbose=False)
                else:
                    self.run(command, prompt=False, verbose=True)
        finally:
            file.close()

    def autoCompleteShow(self, command, offset = 0): # seb20070712: moved offset into arguments
        """Display auto-completion popup list."""
        self.AutoCompSetAutoHide(self.autoCompleteAutoHide)
        self.AutoCompSetIgnoreCase(self.autoCompleteCaseInsensitive)
        list = self.interp.getAutoCompleteList(command,
                    includeMagic=self.autoCompleteIncludeMagic,
                    includeSingle=self.autoCompleteIncludeSingle,
                    includeDouble=self.autoCompleteIncludeDouble)
        if list:
            options = ' '.join(list)
            #seb offset = 0
            self.AutoCompShow(offset, options)

    def autoCallTipShow(self, command, alwaysShow=False): #seb: added alwaysShow for 'tab'-key
        """Display argument spec and docstring in a popup window."""
        if self.CallTipActive():
            self.CallTipCancel()
        (name, argspec, tip) = self.interp.getCallTip(command)
        if tip:
            dispatcher.send(signal='Shell.calltip', sender=self, calltip=tip)
        if not alwaysShow and not self.autoCallTip:
            return
        if argspec:
            startpos = self.GetCurrentPos()
            self.write(argspec + ')')
            endpos = self.GetCurrentPos()
            self.SetSelection(endpos, startpos)
        if tip:
            curpos = self.GetCurrentPos()
            tippos = curpos - (len(name) + 1)
            fallback = curpos - self.GetColumn(curpos)
            # In case there isn't enough room, only go back to the
            # fallback.
            tippos = max(tippos, fallback)
            self.CallTipShow(tippos, tip)

    def writeOut(self, text):
        """Replacement for stdout."""
        self.write(text)

    def writeErr(self, text):
        """Replacement for stderr."""
        self.write(text)

    def redirectStdin(self, redirect=True):
        """If redirect is true then sys.stdin will come from the shell."""
        if redirect:
            sys.stdin = self.reader
        else:
            sys.stdin = self.stdin

    def redirectStdout(self, redirect=True):
        """If redirect is true then sys.stdout will go to the shell."""
        if redirect:
            sys.stdout = PseudoFileOut(self.writeOut)
        else:
            sys.stdout = self.stdout

    def redirectStderr(self, redirect=True):
        """If redirect is true then sys.stderr will go to the shell."""
        if redirect:
            sys.stderr = PseudoFileErr(self.writeErr)
        else:
            sys.stderr = self.stderr

    def CanCut(self):
        """Return true if text is selected and can be cut."""
        if self.GetSelectionStart() != self.GetSelectionEnd() \
               and self.GetSelectionStart() >= self.promptPosEnd \
               and self.GetSelectionEnd() >= self.promptPosEnd:
            return True
        else:
            return False

    def CanPaste(self):
        """Return true if a paste should succeed."""
        if self.CanEdit() and editwindow.EditWindow.CanPaste(self):
            return True
        else:
            return False

    def CanEdit(self):
        """Return true if editing should succeed."""
        if self.GetSelectionStart() != self.GetSelectionEnd():
            if self.GetSelectionStart() >= self.promptPosEnd \
                   and self.GetSelectionEnd() >= self.promptPosEnd:
                return True
            else:
                return False
        else:
            return self.GetCurrentPos() >= self.promptPosEnd

    def Cut(self):
        """Remove selection and place it on the clipboard."""
        if self.CanCut() and self.CanCopy():
            if self.AutoCompActive():
                self.AutoCompCancel()
            if self.CallTipActive():
                self.CallTipCancel()
            self.Copy()
            self.ReplaceSelection('')

    def Copy(self):
        """Copy selection and place it on the clipboard."""
        if self.CanCopy():
            ps1 = str(sys.ps1)
            ps2 = str(sys.ps2)
            command = self.GetSelectedText()
            command = command.replace(os.linesep + ps2, os.linesep)
            command = command.replace(os.linesep + ps1, os.linesep)
            command = self.lstripPrompt(text=command)
            data = wx.TextDataObject(command)
            self._clip(data)

    def CopyWithPrompts(self):
        """Copy selection, including prompts, and place it on the clipboard."""
        if self.CanCopy():
            command = self.GetSelectedText()
            data = wx.TextDataObject(command)
            self._clip(data)

    def CopyWithPromptsPrefixed(self):
        """Copy selection, including prompts prefixed with four
        spaces, and place it on the clipboard."""
        if self.CanCopy():
            command = self.GetSelectedText()
            spaces = ' ' * 4
            command = spaces + command.replace(os.linesep,
                                               os.linesep + spaces)
            data = wx.TextDataObject(command)
            self._clip(data)

    def _clip(self, data):
        # seb: failed on OSX
        #         if wx.TheClipboard.Open():
        #             wx.TheClipboard.UsePrimarySelection(False)
        #             wx.TheClipboard.SetData(data)
        #             wx.TheClipboard.Flush()
        #             wx.TheClipboard.Close()
        if not wx.TheClipboard.Open():
            wx.Bell()
            return
        try:
            wx.TheClipboard.UsePrimarySelection(False)
            wx.TheClipboard.SetData(data)
            wx.TheClipboard.Flush()
        finally:
            wx.TheClipboard.Close()

    def Paste(self):
        """Replace selection with clipboard contents."""
        if self.CanPaste() and wx.TheClipboard.Open():
            ps2 = str(sys.ps2)
            if wx.TheClipboard.IsSupported(wx.DataFormat(wx.DF_TEXT)):
                data = wx.TextDataObject()
                if wx.TheClipboard.GetData(data):
                    self.ReplaceSelection('')
                    command = data.GetText()
                    command = command.rstrip()
                    command = self.fixLineEndings(command)
                    command = self.lstripPrompt(text=command)
                    command = command.replace(os.linesep + ps2, '\n')
                    command = command.replace(os.linesep, '\n')
                    command = command.replace('\n', os.linesep + ps2)
                    self.write(command)
            wx.TheClipboard.Close()

    def PasteAndRun(self):
        """Replace selection with clipboard contents, run commands."""
        if wx.TheClipboard.Open():
            ps1 = str(sys.ps1)
            ps2 = str(sys.ps2)
            if wx.TheClipboard.IsSupported(wx.DataFormat(wx.DF_TEXT)):
                data = wx.TextDataObject()
                if wx.TheClipboard.GetData(data):
                    endpos = self.GetTextLength()
                    self.SetCurrentPos(endpos)
                    startpos = self.promptPosEnd
                    self.SetSelection(startpos, endpos)
                    self.ReplaceSelection('')
                    text = data.GetText()
                    text = text.lstrip()
                    text = self.fixLineEndings(text)
                    text = self.lstripPrompt(text)
                    text = text.replace(os.linesep + ps1, '\n')
                    text = text.replace(os.linesep + ps2, '\n')
                    text = text.replace(os.linesep, '\n')
                    lines = text.split('\n')
                    commands = []
                    command = ''
                    for line in lines:
                        if line.strip() == ps2.strip():
                            # If we are pasting from something like a
                            # web page that drops the trailing space
                            # from the ps2 prompt of a blank line.
                            line = ''
                        if line.strip() != '' and line.lstrip() == line:
                            # New command.
                            if command:
                                # Add the previous command to the list.
                                commands.append(command)
                            # Start a new command, which may be multiline.
                            command = line
                        else:
                            # Multiline command. Add to the command.
                            command += '\n'
                            command += line
                    commands.append(command)
                    for command in commands:
                        command = command.replace('\n', os.linesep + ps2)
                        self.write(command)
                        self.processLine()
            wx.TheClipboard.Close()

    def wrap(self, wrap=True):
        """Sets whether text is word wrapped."""
        try:
            self.SetWrapMode(wrap)
        except AttributeError:
            return 'Wrapping is not available in this version.'

    def zoom(self, points=0):
        """Set the zoom level.

        This number of points is added to the size of all fonts.  It
        may be positive to magnify or negative to reduce."""
        self.SetZoom(points)

