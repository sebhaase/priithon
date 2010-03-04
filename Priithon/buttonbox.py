'''
A buttonBox is a list (maybe many rows) of buttons, labels, txtCtrls, checkBoxes

Create a new buttonBox with 
>>> buttonBox(...)
it gets automatically appended to the list of all `buttonBoxes`.

You can (dynamically) add one or more controls with `buttonBoxAdd()`.
Both `buttonBoxAdd()` and `buttonBox()` take the same `itemList` argument
   each `item` in `itemList` is translated into a call of
     1) startNewRow(weight, expand)
   or
     2) addButton(label, cmd, weight, expand)

  if `item` is a list or tuple, up to 4 things can be specified:
     1.) `label` (i.e. text on button or text in textCtrl)
     2.) `command`  (default: None)
     3.) `weight` - items will get screen-space by relative weight (default: 1.0)
     4.) `expand` - adjust size vertically (on resizing buttonBox) (default: True)
  .if `item` is a string, it specifies `label` and uses the above defaults for all others

  `label` has the one of 3 forms (note the SPACE and the TAB):
        "C"  ,  "A\tC"  or   "A B\tC"
  A specifies the wx-control type: 'b','tb','t','c','l','sl'
     default is 'b'
     'b'  button
     'tb' togglebutton
     't'  text-control
     'c'  checkbox
     'l'  static-label
     'sl' slider

  B specifies `exec_to_name_control` - a string that is executed at creation time, 
     exec in execModule - use 'x' to refersto the wx-control, '_' to the execModule
     default is ''
  C specifies the wx-control"s label

  note 0) label without '\t' defaults to control-type button (A => 'b')
  note 1) for button: if cmd is None: use label (part C) as cmd
  note 2) for txtCtrl: if cmd is '--': make read-only, set cmd to None
  note 3) for checkbox: if label (part C) contains (another) '\t' use ALIGN_RIGHT
  note 4) for label: command is ignored #CHECK
  note 5) for slider: label gives value,minValue,maxValue (space separated) - default: 0,0,100
EXAMPLES:
buttonBox('print 666')
buttonBox(('devil', 'print 666'))
buttonBox([('devil', 'print 666'),
           ('xx', 'xx=99'),
          ])
buttonBox([('c\ton/off', 'print x'),
          ])


buttonBox([('l\tx-value:','',0),('t\t1234', '_.x=float(x)')])
buttonBox([('l\tx-value:','',0),('t _.myText=x\t1234', '_.textVal=x;print x')])
'''
import wx
try:
    buttonBoxes
except:
    buttonBoxes=[]
class _buttonBox:
    def __init__(self, title="button box",
                 parent=None,
                 pos=wx.DefaultPosition,
                 style=wx.DEFAULT_FRAME_STYLE,
                 verticalLayout = False,
                 execModule=None):
        '''
        if verticalLayout: switch columns <-> rows
           -- all other documentation assumes verticalLayout=False !!
        if execModule is None: use __main__
        '''
        global buttonBoxes
        self.i = len(buttonBoxes)

        #self.frame = wx.Frame(parent, -1, title + " (%d)", style=style)
        self.frame = wx.Frame(parent, -1, title, style=style,
                              pos=pos)
        if verticalLayout:
           self.sizer0Vert= wx.BoxSizer(wx.HORIZONTAL)
        else:
           self.sizer0Vert= wx.BoxSizer(wx.VERTICAL)
        #self.row=0
        self.sizers=[]
        self.startNewRow()
        self.frame.SetSizer(self.sizer0Vert)
        self.sizer0Vert.SetSizeHints(self.frame)
        self.frame.SetAutoLayout(1)
        self.sizer0Vert.Fit(self.frame)
        self.frame.Show()

        if execModule is None:
            import __main__
            self.execModule = __main__
        else:
            self.execModule = execModule

        buttonBoxes.append(self)
        
        wx.EVT_CLOSE(self.frame, self.onClose)

    def onClose(self, ev):
        try:
            global buttonBoxes
            buttonBoxes[self.i] = None
        except:
            pass
        self.frame.Destroy()
        
    def startNewRow(self, weight=1,expand=True):
        if expand:
            expand=wx.EXPAND
        if self.sizer0Vert.GetOrientation() == wx.VERTICAL:
           self.sizers.append( wx.BoxSizer(wx.HORIZONTAL) )
        else:
           self.sizers.append( wx.BoxSizer(wx.VERTICAL) )
        ss=self.sizers[-1]
        self.sizer0Vert.Add(ss, weight, expand|wx.ALL, 0)

    def addButton(self, label, cmd=None, refitFrame=True, weight=1,expand=True):
        '''
        if label is of form "X\\t...":
           if X is 'b'  a button will be created (that;s also the default)
               cmd will be executed on button-press
               if cmd is None:
                   cmd = label

           if X is 'tb'  a toggle-button will be created
               cmd will be executed on button-press
                  (variable 'x' will contain the button status)
               if cmd is None:
                   cmd = label

           if X is 't'  a TextCtrl field will be created
               cmd will be executed on EVERY text change
                  (variable 'x' will contain the text as string)
               unless if cmd[:2] == '--':
                   this means: text field is NOT editable
               ...-part of label is the default value put in the text-field 
               #todo if ...-part of label is of form '...\t...':
               #todo    the first part will be used as a "label" for the text field
               #todo    the second part will be the default text
               
           if X is 'c'  a CheckBox field will be created
               cmd will be executed on on click
                  (variable 'x' will contain True/False [isChecked])
               ...-part of label is a text label
                     'CheckBox' will be left-of 'text label'
                         except if ...-part contains '\t', then
                     'CheckBox' will be right-of 'text label'
           if X is 'l'  a StaticText label will be created
               label will be aligned to 'right'
               cmd will never be executed

            if X contains a ' ' the part after ' ' will be executed with 'x' being the control-object
               use this to keep a reference to the respective wxControl
               example: "b myButton=x"
               
        if weight is 0 button gets set to minimum size (horizontally)
           otherwise size gets distributed between all buttons
        if expand is True button expands in vertical diection with buttonBox


        NOTE:
            all execs are done in a given `execModule` as globals()
            to modify the module"s namespace the module is accessible as '_'
               e.g.: _.x = x
                     _.myTextControl = x
            (in cmd for buttons there is no 'g' - just use names directly instead: e.g. x = 5)
        '''
        if '\t' in label:
            typ, label = label.split('\t',1)
        else:
            typ = 'b'

        if ' ' in typ:
            typ, exec_to_name_control = typ.split(' ', 1)
        else:
            exec_to_name_control = ''

        typ = typ.lower()
        if   typ == 'b':
            b = wx.Button(self.frame, wx.ID_ANY, label)
            if cmd is None:
                cmd = label
        elif typ == 'tb':
            b = wx.ToggleButton(self.frame, wx.ID_ANY, label)
            if cmd is None:
                cmd = label
        elif typ == 'sl':
            if label:
                value,minVal,maxVal = map(int, label.split())
            else:
                value,minVal,maxVal = 0,0,100
            b = wx.Slider(self.frame, wx.ID_ANY, value,minVal,maxVal)

        elif typ == 't':
            b = wx.TextCtrl(self.frame, wx.ID_ANY) # see below: , label)
            if type(cmd) == type("--") and len(cmd)>1 and cmd[:2] == '--':
                b.SetEditable( False )
                cmd = None
        elif typ == 'c':
            if '\t' in label:
                label, xxxx = label.split('\t',1)
                s = wx.ALIGN_RIGHT
            else:
                s=0
            b = wx.CheckBox(self.frame, wx.ID_ANY, label, style=s)
        elif typ == 'l':
            # http://lists.wxwidgets.org/archive/wx-users/msg31553.html
            # SK> Is there no way to set the vertical alignment of the label within the
            # SK> wxStaticText?
            #      No.
            # SK> If not, do any of you know of any ways to fake it?
            #      Always create the static text of the minimal suitable size (i.e. use
            # wxDefaultSize when creating it) and then pack it into a sizer using
            # spacers:
            #         wxSizer *sizer = new wxBoxSizer(wxVERTICAL);
            #         // centre the text vertically
            #         sizer->Add(0, 1, 1);
            #         sizer->Add(text);
            #         sizer->Add(0, 1, 1);

            
            b = wx.StaticText(self.frame, wx.ID_ANY, label, style=wx.ALIGN_RIGHT)
        else:
            raise ValueError, "unknown control type (%s)"% typ
        if exec_to_name_control:
            exec exec_to_name_control in self.execModule.__dict__, {'x':b, '_':self.execModule}

        if cmd:
            b.SetToolTipString( cmd )
        if expand:
            expand=wx.EXPAND

        ss=self.sizers[-1]
        ss.Add(b, weight, expand|wx.ALL, 0)
        
        if   typ == 'b':
            if cmd:
                def OnB(ev):
                    exec cmd in self.execModule.__dict__, {'x':ev.GetString(), '_':self.execModule}
                wx.EVT_BUTTON(self.frame, b.GetId(), OnB)
        elif typ == 'tb':
            if cmd:
                def OnB(ev):
                    exec cmd in self.execModule.__dict__, {'x':ev.GetInt(), '_':self.execModule}
                wx.EVT_TOGGLEBUTTON(self.frame, b.GetId(), OnB)
        elif typ == 'sl':
            if cmd:
                def OnB(ev):
                    exec cmd in self.execModule.__dict__, {'x':ev.GetInt(), '_':self.execModule}
                wx.EVT_SLIDER(self.frame, b.GetId(), OnB)
        elif typ == 't':
            if cmd:
                def OnT(ev):
                    exec cmd in self.execModule.__dict__, {'x':ev.GetString(), '_':self.execModule}
                wx.EVT_TEXT(self.frame, b.GetId(), OnT)
            b.SetValue(label) # we set "label" here so that the function is triggered already for the default value !!
        elif typ == 'c':
            if cmd:
                def OnC(ev):
                    exec cmd in self.execModule.__dict__, {'x':ev.IsChecked(), '_':self.execModule}
                wx.EVT_CHECKBOX(self.frame, b.GetId(), OnC)
            

        if refitFrame:
            self.frame.Fit()

def buttonBox(itemList=[], title="button box",
              parent=None,
              pos=wx.DefaultPosition,
              style=wx.DEFAULT_FRAME_STYLE,
              verticalLayout = False,
              execModule=None):
    '''create new button box

    itemList is a list of cmd s
    cmd can be:
       + a string that is both button label and command to execute
       + a tuple of (label, commandString)

       if the string == '\n' : that means start a new row

    title: window title (buttonBox id will be added in parenthesis)

    if verticalLayout: switch columns <-> rows
           -- all other documentation assumes verticalLayout=False !!
    if execModule is None: use __main__
    '''
    bb = _buttonBox(title, parent, pos, style, verticalLayout, execModule)
    buttonBoxAdd(itemList)

def buttonBoxAdd(itemList, bb_id=-1):
    '''
    add button to existing buttonBox

    itemList is a list of cmd s
    cmd can be:
       + a string that is both button label and command to execute
       + a tuple of (label, commandString [, weight=1[, expand=True]]) (i.e.: 2,3 or 4 elements) 

       if the string == '\n' : that means start a new row

    bb_id is the id of the buttonBox
    '''
    bb = buttonBoxes[bb_id]
    if not type(itemList) in (list, tuple):
        itemList=[itemList]

    for it in itemList:
        if type(it) in (list, tuple):
            try:
                expand=int(it[3])
            except:
                expand=True
            try:
                weight = float(it[2])
            except:
                weight=1
            try:
                cmd = it[1]
            except:
                cmd = None
            label = it[0]
        else:
            label = it
            cmd=None
            weight=1
            expand=True
        if label == '\n':
            bb.startNewRow(weight=weight,expand=expand)
        else:
            bb.addButton(label, cmd, refitFrame=False, weight=weight,expand=expand)


    bb.frame.Fit()

def buttonBox_setFocus(buttonNum=0, bb_id=-1):
    '''
    set a button given as "active focus" -
    hitting space or return should trigger the button
    
    buttonNum is the number of button in buttonBox (-1 is last button)

    bb_id is the id of the buttonBox
    '''
    bb = buttonBoxes[bb_id]
    b = bb.frame.GetChildren()[buttonNum]
    b.SetFocus()

def buttonBox_clickButton(label, bb_id=-1):
    '''
    postEvent to button with given label
    '''
    bb = buttonBoxes[bb_id]
    b=wx.FindWindowByLabel(label, bb.frame)
    e=wx.CommandEvent(wx.wxEVT_COMMAND_BUTTON_CLICKED, b.GetId())
    wx.PostEvent(b, e)
