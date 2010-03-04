"""Priithon U modules: lot's of simple 'useful' (shortcut) functions
"""
__author__  = "Sebastian Haase <haase@msg.ucsf.edu>"
__license__ = "BSD license - see LICENSE file"

#from __future__ import generators

import numpy as N
try:
    from scipy import ndimage as nd
except ImportError:
    pass
#20060722  import numarray as na
######from numarray import nd_image as nd
#20060722  from numarray import linear_algebra as la
#20060722  from numarray import random_array as ra

import pdb # useful for U.pdb.pm()  # no time to first import: exception would get lost

import seb as S
from usefulGeo import *

#  >>> dir(A)
#  ['TextFile', '__builtins__', '__doc__', '__file__', '__name__', 'numarray', 'readArray', 'readFloatArray', 'readIntegerArray', 'string', 'writeArray', 'writeDataSets']

from ArrayIO import readArray_conv, readArray, readFloatArray, readIntegerArray, writeArray, writeDataSets

from sifreader import readSIF as loadSIF # uses memmap

def _fixDisplayHook():
    """
    change default displayHook: print .3 instead of .299999
    """

    import sys, __main__
    def myStr(a):
        import types, string #, __builtin__
        if type(a) is types.UnicodeType:
            return "u'"+a+"'"
        if type(a) is types.StringType:
            return "'"+a+"'"
        if type(a) is types.TupleType:
            return '(' + string.join(map(myStr,a), ', ') +')'
        if type(a) is types.ListType:
            return '[' + string.join(map(myStr,a), ', ') +']'
        if type(a) is N.dtype and a.isbuiltin:
            return a.name  # 20060720 

        try:
            s = str(a)
        except:
            return repr(a)
        if s =='':
            return repr(a)
        else:
            return s
    def _sebsDisplHook(v):
        if not v is None: # != None:
            import __main__ #global _
            #_ = v
            __main__._ = v
            print myStr(v)
    sys.displayhook = _sebsDisplHook

def _execPriithonRunCommands():
    """
    http://en.wikipedia.org/wiki/Run_Commands
    Rc stands for the phrase "run commands"
    It is used for any file that contains startup information for a command.
    While not historically precise, rc may also be pronounced as "run control", because an rc file controls how a program runs.

    Similarely to matplotlib (ref. matplotlib_fname()), we look for a "user customization" file,
    ".priithonrc.py" in the following order:
    1. currentworking directory
    2. environment variable PRIITHONRC
    3. HOME/.priithonrc.py
    4. windows only:  TODO FIXME
    """
    rcFN = _getRCfile()
    if rcFN:
        import sys,__main__
        #try:
            #stdout = sys.stdout
            #try:
            #    sys.stdout = __main__.shell
            #except:
            #    pass
        try:
            execfile(rcFN,__main__.__dict__)
        except:
            import traceback
            traceback.print_exc()
        #finally:
        #    sys.stdout = stdout

def _getRCfile():
    import os
    rcFN = os.path.join( os.getcwd(), '.priithonrc.py')
    if os.path.exists(rcFN):
        return rcFN

    try:
        path =  os.environ['PRIITHONRCRC']
    except KeyError:
        pass
    else:
        rcFN = os.path.join( path, '.priithonrc.py')
        if os.path.exists(rcFN):
            return rcFN

    path = getHomeDir(defaultToCwd=False)
    if path:
        rcFN = os.path.join( path, '.priithonrc.py')
        if os.path.exists(rcFN):
            return rcFN

    return ""
    
def getHomeDir(defaultToCwd=False):
    """
    Try to find user's home directory, otherwise return current directory.
    If defaultToCwd is False, returns "" in case nothing else works
    """
    #original: http://mail.python.org/pipermail/python-list/2005-February/305394.html
    #          Subject: Finding user's home dir
    #          From: Nemesis nemesis at nowhere.invalid 
    #          Date: Wed Feb 2 20:26:00 CET 2005
    #          def getHomeDir():
    #              ''' Try to find user's home directory, otherwise return current directory.'''
    import os
    try:
        path1=os.path.expanduser("~")
    except:
        path1=""
    try:
        path2=os.environ["HOME"]
    except:
        path2=""
    try:
        path3=os.environ["USERPROFILE"]
    except:
        path3=""

    if not os.path.exists(path1):
        if not os.path.exists(path2):
            if not os.path.exists(path3):
                if defaultToCwd:
                    return os.getcwd()
                else: return ""
            else: return path3
        else: return path2
    else: return path1


def _getGoodifiedArray(arr):
    """
    return "well behaved" version of a numpy array
    1) convert lists or tuple to numpy-array
    2) make copy of numpy arrays if non-contigous or non-native

    (used in conjunction with SWIGed functions)
    """
    try:
        if arr.dtype.isnative:
            arr = N.ascontiguousarray(arr)
        else:
            arr = N.ascontiguousarray(arr, arr.dtype.newbyteorder('='))
    except AttributeError:
            arr = N.ascontiguousarray(arr)

    if arr.dtype == N.bool:  # no SWIGed function for bool, use uint8
        arr = arr.view(N.uint8)

    return arr

def naSetArrayPrintMode(precision=4, suppress_small=1):
    #import sys
    #sys.float_output_suppress_small=suppress_small
    #na.arrayprint.set_precision(precision)
    N.set_printoptions(precision=precision, threshold=None,
                       edgeitems=None, linewidth=None,
                       suppress=suppress_small)

def debug():
    """calls post-mortem-debugger  pdm.pm()
    commands:
        q - quit
        l - list
        p - print 'variable'
        u - up in calling stack
        d - down in calling stack
        h - help
        ...
    """
    pdb.pm()

def DEBUG_HERE():
    """calls debugger  pdm.set_trace()
       go into debugger mode once execution reaches this line
    """
    pdb.set_trace()


def timeIt(execStr, nReps=1):
    """calls exec(execStr)  nReps times
    returns "cpu-time-after"-"cpu-time-before"
    if nReps > 1  the it calls it nReps times
                  and return mmms over all (each separately timed!)
    """
    import sys, time
    global fr,fc, argsn, args
    fr = sys._getframe(1)
    # fc = fr.f_code
    #gs = fr.f_locals   #gs = fr.f_globals
    

    if nReps==1:
        t0 = time.clock()
        exec execStr in fr.f_locals, fr.f_globals
        return time.clock() - t0
    else:
        _ttt = N.empty(shape=nReps, dtype=N.float64)
        for _i in range(nReps):
            t0 = time.clock()
            exec execStr  in fr.f_locals, fr.f_globals
            _ttt[_i] = time.clock() - t0
        return mmms(_ttt)

def reloadAll(verbose=False, repeat=1, hiddenPriithon=True):
    '''
    reload all modules known in __main__

    repeat 'repeat' times - in case of dependencies

    if hiddenPriithon is True:
    also reload
       viewer.py
       viewer2.py
       viewerCommon.py
       splitND.py
       splitND2.py
       splitNDCommon.py
    '''
    import __main__, types, __builtin__
    for i in range(1+repeat):
        for m,mm in __main__.__dict__.iteritems():
            if type(mm) == types.ModuleType and not mm in (__builtin__, __main__):
                if verbose:
                    print m,
                reload(mm)
        if hiddenPriithon:
            mods = ['viewerCommon',
                    'viewer',
                    'viewer2',
                    'splitNDcommon',
                    'splitND',
                    'splitND2', 
                    'usefulX2', 
                    'usefulX', 
                    ]
            for m in mods:
                exec "import %s; reload(%s)" %(m,m)

def localsAsOneObject(*args):
    """
    useful for rapid code development / debugging:

    create and return a classObject containing some/all local variables
    taken from the calling function-frame

    if no args given: return all local vars
    """
    import sys
    fr = sys._getframe(1)

    class _someLocalVars:
        pass
    
    retDict = _someLocalVars()
    if len(args) == 0:
        for varname,varvalue in fr.f_locals.iteritems():
            retDict.__dict__[varname] = varvalue
    else:
        for v in args:
            for varname,varvalue in fr.f_locals.iteritems():
                if v is varvalue:
                    retDict.__dict__[varname] = varvalue
                    break

    return retDict
                




import string
# http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/303342
def strTranslate(s, frm='', to='', delete='', keep=None):
    '''
    translate chars in string `s`
    each `c` in `frm` is translated into the respective `c` in `to`
      (`to` can be length 1)
    each `c` in `keep` is kept
     UNLESS(!) it is also in `delete`
    each `c` in `delete` is taken out

    seb: instead of a class we have a function - ref. ASPN/Cookbook/Python/Recipe/303342

    This class handles the three most common cases where I find myself having to stop and think about how to use translate:

    1) Keeping only a given set of characters.
    >>> strTranslate('Chris Perkins : 224-7992', keep=U.string.digits)
    '2247992'

    2) Deleting a given set of characters.
    >>> strTranslate('Chris Perkins : 224-7992', delete=U.string.digits)
    'Chris Perkins : -'

    3) Replacing a set of characters with a single character.
    >>> trans = Translator(string.digits, '%')
    >>> strTranslate('Chris Perkins : 224-7992', (string.digits, '%')
    'Chris Perkins : %%%-%%%%'

    Note that the delete parameter trumps the keep parameter if they overlap:
    >>> strTranslate('abcdef', delete='abcd', keep='cdef')
    'ef'
    This is an arbitrary design choice - makes as much sense as anything, I suppose.
    '''
    allchars = string.maketrans('','')
    if len(to) == 1:
        to = to * len(frm)
    trans = string.maketrans(frm, to)
    if keep is not None:
        delete = allchars.translate(allchars, keep.translate(allchars, delete))
    #def callable(s):

    if type(s) is unicode: # HACK workaround for unicode (occurred with TextCrtl unicode-version of wxPython)
        s = str(s)
    return s.translate(trans, delete)
    #return callable

def memNAprofile(dicts=[],
                 addHere=3,
                 verbose=True):
    """
    report on numarray mem usage in given dictinoaries (or modules)
    if addHere is
       1 include locals() dict from where memNAprofile is called
       2 include globals() dict from where memNAprofile is called
       3 both

    if verbose: print stats for each numarray found

    returns tuple( number of numarrays, total MB mem usage, timeString)
    """
    print "TODO: memNAprofile"
    return 
    global arrs # HACK for sebsort
    gs = {}
    if addHere:
        import sys
        fr = sys._getframe(1)
        if addHere & 2:
            gs.update(fr.f_globals)
        if addHere & 1:
            gs.update(fr.f_locals)
    for d in dicts:
        if type(d) is dict:
            gs.update( d )
        else: # assume it is a module
            gs.update( d.__dict__ )
        

    #global gs, k, o,f,fs, arrs, totsize, totnum
    f=''   # RuntimeError: dictionary changed size during iteration
    fs=''
    o=''
    k=''
    arrs = {}
    totsize = 0
    totnum = 0
    kStringMaxLen = 0
    t_naa = N.ndarray
    import string

    nonMemFakeAddr = -1

    for k in gs:
        if len(k) > kStringMaxLen:
            kStringMaxLen = len(k)
        o = gs[k]
        t = type(o)
        if t == t_naa:
            #print k # , t
            f = string.split( repr(o._data) )
            if f[0] == '<memory': # '<memory at 0x50a66008 with size:0x006f5400 held by object 0x092772e8 aliasing object 0x00000000>'
                fs = string.split( f[4],':' )
                size   = eval( fs[1] )
                memAt  = f[2]
                objNum = f[8]
            elif f[0] == '<MemmapSlice': # '<MemmapSlice of length:7290000 readonly>'
                fs = string.split( f[2],':' )
                size   = eval( fs[1] )
                memAt  = nonMemFakeAddr
                nonMemFakeAddr -= 1
                objNum = 0
            else:
                if verbose:
                    print "# DON'T KNOW: ",  k, repr(o._data)
                continue

            #print repr(o._data)
            #print objNum, memAt, size

            try:
                arrs[ memAt ][0] += 1
                arrs[ memAt ][1].append( k )
                arrs[ memAt ][2].append( size )
            except:
                arrs[ memAt ] = [ 1, [k], [size] ]
                totsize += size
                totnum  += 1
                
    def sebsort(m1,m2):
        global arrs
        import __builtin__
        k1 = arrs[ m1 ][1]
        k2 = arrs[ m2 ][1]
        return __builtin__.cmp(k1,  k2)

    if verbose:
        ms = arrs.keys()
        ms.sort( sebsort )
        #print kStringMaxLen
        for memAt in ms:
            ks   = arrs[ memAt ][1]
            size = arrs[ memAt ][2][0]
            o = gs[ ks[0] ]
            if len(ks) == 1:
                ks = ks[0]
            print "%8.2fk %-*s %-14s %-15s %-10s" %(size/1024., kStringMaxLen, ks, o.type(), o.shape, memAt)

    del arrs # HACK for sebsort
    import time
    return totnum, int(totsize/1024./1024. * 1000) / 1000.,  time.asctime()

def dirNA(inclSize=0):
    import sys, time
    global fr,fc, argsn, args
    fr = sys._getframe(1)
    fc = fr.f_code
        
    print "TODO: dirNA"
    return 
    #           modname = fr.f_globals['__name__']
    #    #print "=== Module:", modname, "==="
    
    #           if modname != None:
    #               exec "import " + modname
    #           else:
    #               print "DEBUG: modname is None  -- why !?"

    global gs, k, o,f,fs, arrs, totsize, totnum
    f=''   # RuntimeError: dictionary changed size during iteration
    fs=''
    o=''
    k=''
    arrs = {}
    totsize = 0
    totnum = 0
    #gs = fr.f_globals # .keys()
    gs = fr.f_locals # .keys()
    kStringMaxLen = 0
    t_naa = N.ndarray
    import string


    gsF = []
    for k in gs:
        o = gs[k]
        t = type(o)
        if t == t_naa:
            if inclSize:
                f = string.split( repr(o._data) )
                if f[0] == '<memory':
                    fs = string.split( f[4],':' )
                    size   = eval( fs[1] )
                    memAt  = f[2]
                    objNum = f[8]
                else:
                    fs = string.split( f[2],':' )
                    size   = eval( fs[1] )
                    memAt  = 0
                    objNum = 0
                    gsF += [(k, size)]
            else:
                gsF += k
        gsF.sort()
        print gsF
        '''
    for k in gs:
        if len(k) < kStringMaxLen:
            kStringMaxLen = len(k)
        o = gs[k]
        t = type(o)
        if t == t_naa:
            #print k # , t

            #print repr(o._data)
            #print objNum, memAt, size

            try:
                arrs[ memAt ][0] += 1
                arrs[ memAt ][2].append( size )
            except:
                arrs[ memAt ] = [ 1, k, [size] ]
                totsize += size
                totnum  += 1

    def sebsort(m1,m2):
        global arrs
        import __builtin__
        k1 = arrs[ m1 ][1]
        k2 = arrs[ m2 ][1]
        return __builtin__.cmp(k1,    k2)

    ms = arrs.keys()
    ms.sort( sebsort )
    for memAt in ms:
        k     = arrs[ memAt ][1]
        size = arrs[ memAt ][2][0]
        o = gs[k]
        
        print "%8.2fk %-*s %14s %15s %10s" %(size/1024., kStringMaxLen, k, o.type(), o.shape, memAt)
        '''

def deriv1D(arr, reverse=0):
    """poor mans derivative:
    if reverse:
        returns arr[:-1] - arr[1:]
    else
        returns arr[1:] - arr[:-1]
    """
    arr = N.asarray(arr)
    if reverse:
        return arr[:-1] - arr[1:]
    else:
        return arr[1:] - arr[:-1]

   

def checkGoodArrayF(arr, argnum, shape=None):
    if not arr.flags.carray:
        raise RuntimeError, "*** non contiguous arg %s ** maybe use zeroArrF" % argnum
    if arr.dtype.type != N.float32:
        raise RuntimeError, "*** non Float32 arg %s ** maybe use zeroArrF" % argnum
    if not arr.dtype.isnative:
        raise RuntimeError, "*** non native byteorder: arg %s ** maybe use zeroArrF" % argnum
    if shape is not None and shape != arr.shape:
        raise RuntimeError, "*** arg %d should have shape %s, but has shape %s" \
                   % (argnum, shape, arr.shape)


def arrSharedMemory(shape, dtype, tag="PriithonSharedMemory"):
    """
    Windows only !
    share memory between different processes if same `tag` is used.
    """
    itemsize = N.dtype(dtype).itemsize
    count = N.product(shape)
    size =  count * itemsize
    
    import mmap
    sharedmem = mmap.mmap(0, size, tag)
    a=N.frombuffer(sharedmem, dtype, count)
    a.shape = shape
    return a


def arr(dtype=None, *args):
    """return args tuple as array
    if dtype is None use "default/automatic" dtype
    """
    return N.array(args, dtype=dtype)
def arrF(*args):
    """return args tuple as array dtype=Float32
    """
    return N.array(args, dtype=N.float32)
def arrD(*args):
    """return args tuple as array dtype=Float64
    """
    return N.array(args, dtype=N.float64)
def arrI(*args):
    """return args tuple as array dtype=Int32
    """
    return N.array(args, dtype=N.int32)
def arrU(*args):
    """return args tuple as array dtype=UInt16
    """
    return N.array(args, dtype=N.uint16)
def arrS(*args):
    """return args tuple as array dtype=Int16
    """
    return N.array(args, dtype=N.int16)
def arrC(*args):
    """return args tuple as array dtype=Complex64 (single prec)
    """
    return N.array(args, dtype=N.complex64)
def arrCC(*args):
    """return args tuple as array dtype=Complex128 (double prec)
    """
    return N.array(args, dtype=N.complex128)

def asFloat32(a):
    """returns N.asarray(a, N.Float32)"""
    return N.asarray(a, N.float32)

def norm(arr, axis=-1):
    """return array with ndim arr.ndim-1
        return N.sqrt(N.sum(arr**2, axis)

U.norm([3,4])
5.0
U.timeIt("U.norm([3,4])", 100000)
(0.0, 0.02, 0.000384, 0.00192211966329)
U.timeIt("U.norm([3])", 100000)
(0.0, 0.02, 0.0003597, 0.00186269050301)
a = na.asarray([3,4])
U.timeIt("U.norm(a)", 100000)
(0.0, 0.01, 0.0001728, 0.00130312706978)
a = na.asarray([3])
U.timeIt("U.norm(a)", 100000)
(0.0, 0.01, 0.0001689, 0.00128859333771)
U.timeIt("na.abs(a)", 100000)
(0.0, 0.02, 0.0001107, 0.00104725618165)
U.timeIt("abs(a)", 100000)
(0.0, 0.01, 0.0001092, 0.00103926674151)
    """
    arr = N.asarray(arr)
    return N.sqrt(N.sum(arr**2, axis))

def clip(arr,min,max):
    """clips arr *inplace*
    returns arr
    """
    import seb as S
    arr = _getGoodifiedArray(arr)
    S.clip( arr, min, max )
    return arr

def findMax(arr):
    """returns value and position of maximum in arr
    assumes 3D array, so returned is a 4-tuple: [val,z,y,x]
    for 2D or 1D z,y would be respectively 0
    """
    import seb as S
    arr = _getGoodifiedArray(arr)
    return S.findMax( arr )
def findMin(arr):
    """returns value and position of minimum in arr
    assumes 3D array, so returned is a 4-tuple: [val,z,y,x]
    for 2D or 1D z,y would be respectively 0
    """
    import seb as S
    arr = _getGoodifiedArray(arr)
    return S.findMin( arr )

def min(arr):
    arr = N.asarray(arr)
    return arr.min()

def max(arr):
    arr = N.asarray(arr)
    return arr.max()

def median(arr):
    import seb as S
    arr = _getGoodifiedArray(arr)
    return S.median( arr )
def median2(arr):
    """returns both median and "median deviation" (tuple)
    (broken on windows !!! returns always -999, see 'seb1.cpp')
    """
    import seb as S
    arr = _getGoodifiedArray(arr)
    return S.median2( arr )


def mean(arr):
    import seb as S
    arr = _getGoodifiedArray(arr)
    return S.mean( arr )  # CHECK if should use ns.mean

def stddev(arr):
    arr = N.asarray(arr)
    return N.std(arr.flat)

_FWHM_over_gaussStddev = 2. * N.sqrt(2.*N.log(2.)) 

def FWHM(arr):
    """returns Full-Width-Half-Max for gaussian distributions"""
    return _FWHM_over_gaussStddev * stddev(arr)

def FWHM_s(gaussStddev):
    """returns Full-Width-Half-Max for gaussian distributions
    gaussStddev is the stddev of arr"""
    return _FWHM_over_gaussStddev * gaussStddev

_pi_over_180 = N.pi/180
def deg2rad(angle):
    """return angle(given in degree) converted to randians"""
    return angle * _pi_over_180
def rad2deg(angle):
    """return angle(given in randians) converted to degree"""
    return angle / _pi_over_180


def mm(arr):
    arr = N.asarray(arr)
    return (N.minimum.reduce(arr.flat), N.maximum.reduce(arr.flat))

def mmm(arr):
    import seb as S
    arr = _getGoodifiedArray(arr)
    #TODO: make nice for memmap
    m = S.mean(arr)
    return (N.minimum.reduce(arr.flat), N.maximum.reduce(arr.flat), m)

def mmms(arr):
    import seb as S
    arr = _getGoodifiedArray(arr)
    #TODO: make nice for memmap
    mi,ma,me,st = S.mmms( arr )
    return (mi,ma,me,st)

def mean2d(arr, outtype=N.float32):
    """
    returns an array of shape arr.shape[:-2] and dtype outtype
    """
    b = N.empty(shape=arr.shape[:-2], dtype=outtype)
    bb = b.view()
    bb.shape = (-1,)
    aarr = arr.view()
    aarr.shape = (-1,) + arr.shape[-2:]

    import seb as S
    for i in range( bb.shape[0] ):
        #bb[i] = S.mean( aarr[i] )
        bb[i] = aarr[i].mean()

    return b

def max2d(arr, outtype=None):
    """returns an array of shape arr.shape[:-2] and dtype outtype
    if outtype=None it uses arr.dtype
    """
    if outtype is None:
        outtype = arr.dtype

    b = N.empty(shape=arr.shape[:-2], dtype=outtype)
    bb = b.view()
    bb.shape = (-1,)
    aarr = arr.view()
    aarr.shape = (-1,) + arr.shape[-2:]

    import seb as S
    for i in range( bb.shape[0] ):
        bb[i] = aarr[i].max()

    return b
def min2d(arr, outtype=None):
    """returns an array of shape arr.shape[:-2] and dtype outtype
    if outtype=None it uses arr.dtype
    """
    if outtype is None:
        outtype = arr.dtype

    b = N.empty(shape=arr.shape[:-2], dtype=outtype)
    bb = b.view()
    bb.shape = (-1,)
    aarr = arr.view()
    aarr.shape = (-1,) + arr.shape[-2:]

    import seb as S
    for i in range( bb.shape[0] ):
        bb[i] = aarr[i].min()

    return b

def mmm2d(arr, outtype=None):
    """min-max-mean: returns an array of shape (3,)+arr.shape[:-2] and dtype outtype
    if outtype=None it uses arr.dtype
    """
    if outtype is None:
        outtype = arr.dtype

    b = N.empty(shape=(3,)+arr.shape[:-2], dtype=outtype)
    bb = b.view()
    bb.shape = (3, -1)
    aarr = arr.view()
    aarr.shape = (-1,) + arr.shape[-2:]

    import seb as S
    for i in range( bb.shape[1] ):
        arr = _getGoodifiedArray(aarr[i])

        bb[:, i] = S.mmm( aar )

    return b

def mmms2d(arr, outtype=N.float32):
    """min-max-mean-stddev: returns an array of shape (4,)+arr.shape[:-2] and dtype outtype
    if outtype=None it uses arr.dtype
    """
    if outtype is None:
        outtype = arr.dtype

    b = N.empty(shape=(4,)+arr.shape[:-2], dtype=outtype)
    bb = b.view()
    bb.shape = (4, -1)
    aarr = arr.view()
    aarr.shape = (-1,) + arr.shape[-2:]

    import seb as S
    for i in range( bb.shape[1] ):
        arr = _getGoodifiedArray(aarr[i])
        bb[:, i] = S.mmms( arr )

    return b

def mm2d(arr, outtype=None):
    """min-max: returns an array of shape (2,)+arr.shape[:-2] and dtype outtype
    if outtype=None it uses arr.dtype
    """
    if outtype is None:
        outtype = arr.dtype

    b = N.empty(shape=(2,)+arr.shape[:-2], dtype=outtype)
    bb = b.view()
    bb.shape = (2, -1)
    aarr = arr.view()
    aarr.shape = (-1,) + arr.shape[-2:]

    for i in range( bb.shape[1] ):
        bb[0, i] = aarr[i].min()
        bb[1, i] = aarr[i].max()

    return b
def median2d(arr, outtype=None):
    """median per 2d section

    returns an array of shape arr.shape[:-2] and dtype outtype
    if outtype=None it uses arr.dtype
    """
    if outtype is None:
        outtype = arr.dtype

    b = N.empty(shape=arr.shape[:-2], dtype=outtype)
    bb = b.view()
    bb.shape = (-1,)
    aarr = arr.view()
    aarr.shape = (-1,) + arr.shape[-2:]

    import seb as S
    for i in range( bb.shape[0] ):
        arr = _getGoodifiedArray(aarr[i])
        bb[i] = S.median( arr )

    return b
def median22d(arr, outtype=None):
    """median2 per 2d section [median is (median,meddev)]

    returns an array of shape (2,)+arr.shape[:-2] and dtype outtype
    if outtype=None it uses arr.dtype
    """
    if outtype is None:
        outtype = arr.dtype

    b = N.empty(shape=(2,)+arr.shape[:-2], dtype=outtype)
    bb = b.view()
    bb.shape = (2, -1)
    aarr = arr.view()
    aarr.shape = (-1,) + arr.shape[-2:]

    import seb as S
    for i in range( bb.shape[1] ):
        arr = _getGoodifiedArray(aarr[i])
        bb[:, i] = S.median2( arr )

    return b

def topPercentile2d(arr, percentile=1, outtype=None):
    """find Intens. for highest percentile  per section


    returns an array of shape (2,)+arr.shape[:-2] and dtype outtype
    if outtype=None it uses arr.dtype

    slow!! ****** might only work for UInt16 arr *********
    """
    if outtype is None:
        outtype = arr.dtype

    b = N.empty(shape=arr.shape[:-2], dtype=outtype)
    bb = b.view()
    bb.shape = (-1,)
    aarr = arr.view()
    aarr.shape = (-1,) + arr.shape[-2:]

    import seb as S
    hist = N.empty( shape=(1<<16), dtype=N.int32 )
    nPix = N.prod( aarr[0].shape )
    for i in range( bb.shape[0] ):
        arr = _getGoodifiedArray(aarr[i])

        (mi,ma,mean,stddev) = S.histogram2(arr, 0, (1<<16), hist)
        tp = S.toppercentile(hist, nPix, int(ma), percentile)
        bb[i] = tp

    return b


def fitLine(yy,xx=None):
    """returns (a,b, yDeltaSumPerVal) for least-sqare-fit of axx(i) + b = yy(i)
    yDeltaSumPerVal= sum[(axx+ b - yy)**2] **.5 / numPoints

    if xx is None it defaults to 0,1,2,3,4,...
    """
    if xx is None:
       xx= N.arange( len(yy) )
    
    xm = N.mean(xx)
    ym = N.mean(yy)
    xym = N.mean(xx*yy)
    xxm= N.mean(xx*xx)
    a = (xm * ym - xym) / (xm*xm - xxm)
    b = ym-a*xm

    deltaSumPerVal = N.sum( (a*xx+b - yy) ** 2 ) **.5   / xx.shape[0]
    
    return (a, b, deltaSumPerVal)

'''
def _line(a,b, t):
    """model function to test fitLine
    a,b  are the first to values return from fitLine (as is y= at+b)
    t could be e.g. N.arange(0,100,.1)
    """
    return b+a*t

def fitAny(f, parmTuple0, data, max_iterations=1000):
    """
    data should be list of (x,y) or (x,y,deltaY) tuples
    (instead of 'list' you can of course have an array w/
    shape=(n,2) or shape=(n,3), n beeing the number of data points

    if data.ndim == 1 or data.shape = (n,1) it fits w/ x=1,2,3,...n

    f is your 'model' function that takes two arguments:
    a tuple of parameters and x
    
    The function returns a list containing the optimal parameter values
    and the chi-squared value describing the quality of the fit.
    """

    from Scientific.Functions.LeastSquares import leastSquaresFit

    data = Num.asarray(data)

    if len(data.shape) == 1:
        #BUG in Numeric24.2 
        #        TypeError: Array can not be safely cast to required dtype
        #     data = Num.transpose(Num.array([Num.arange(len(data)), data]))
        data = Num.transpose(Num.array([list(Num.arange(len(data))), data]))
    elif data.shape[1] == 1:
        #BUG in Numeric24.2 
        #        TypeError: Array can not be safely cast to required dtype
        #     data = Num.transpose(Num.array([Num.arange(len(data)), data][0]))
        data = Num.transpose(Num.array([list(Num.arange(len(data))), data[0]]))

    return leastSquaresFit(f,parmTuple0,data, max_iterations)

# def polynomialModel
def _poly(params, t):
    r = 0.0
    for i in range(len(params)):
        r = r + params[i]*Num.power(t, i)
    return r

def fitPoly(parmTuple0, data, max_iterations=1000):
    """
    data should be list of y or (x,y)- or (x,y,deltaY)-tuples
    (instead of 'list' you can of course have an array w/
    shape=(n,2) or shape=(n,3), n beeing the number of data points

    uses polynomial 'model' ( U._poly )
    
    The function returns a list containing the optimal parameter values
    and the chi-squared value describing the quality of the fit.
    """


    return fitAny(_poly, parmTuple0, data, max_iterations)

#   def decayModel(params, t):
def _decay(params, t):
    if len(params) % 2==0:
        raise "number of parms must be odd: one offset and 2 more for each exponential"
    try:
        r = Num.array(len(t)*(params[0],))
    except: # t has no len
        r = params[0]

    halfTimeScaler = N.log(2.)
    n = int( (len(params)-1) / 2 )
    for i in range(n):
        r = r + params[1+2*i] * Num.exp(-t *halfTimeScaler/ params[2+2*i])
#       r = r + params[1+2*i] * Num.exp(-t *halfTimeScaler/ float(params[2+2*i]))
    return r


def fitDecay(parmTuple0, data, max_iterations=1000):
    """
    data should be list of y or (x,y)- or (x,y,deltaY)-tuples
    (instead of 'list' you can of course have an array w/
    shape=(n,2) or shape=(n,3), n beeing the number of data points

    uses model: p[0] + p[i]*exp(-t / p[i+1])  w/ i=1..(len(p)+1)/2
     ( U._decay )
    
    The function returns a list containing the optimal parameter values
    and the chi-squared value describing the quality of the fit.
    """

    return fitAny(_decay, parmTuple0, data, max_iterations)

def _gaussian1D_2(p, x):
    """p tuple is [sigma, peakVal]
    """
    from fftfuncs import gaussian_N 
    return gaussian_N(x, dim=1, sigma=p[0], integralScale=None, peakVal=p[1])
    
def _gaussian1D_3(p, x):
    """p tuple is [x0, sigma, peakVal]
    """
    from fftfuncs import gaussian_N 
    return gaussian_N(x-p[0], dim=1, sigma=p[1], integralScale=None, peakVal=p[2])
    
def _gaussian1D_4(p, x):
    """p tuple is [y0, x0, sigma, peakVal]
    """
    from fftfuncs import gaussian_N 
    return p[0]+gaussian_N(x-p[1], dim=1, sigma=p[2], integralScale=None, peakVal=p[3]-p[0])
    
def fitGaussian1D(parmTuple0, data, max_iterations=None):
    """
    data should be list of (x,y) or (x,y,deltaY) tuples
    (instead of 'list' you can of course have an array w/
    shape=(n,2) or shape=(n,3), n beeing the number of data points

    uses model:  ... (U._gaussian)
    
    The function returns a list containing the optimal parameter values
    and the chi-squared value describing the quality of the fit.

    parmTuple0 is either
    [sigma, peakVal]
    [x0, sigma, peakVal]
    [y0, x0, sigma, peakVal]

    x0 is center of gaussian (default 0)
    y0 is baseline offset gaussian (default 0)
    sigma is sigma (stddev) of gaussian
    peakval is  "center height" above baseline
    """

    if len(parmTuple0) == 2:
        return fitAny(_gaussian1D_2, parmTuple0, data, max_iterations)
    if len(parmTuple0) == 3:
        return fitAny(_gaussian1D_3, parmTuple0, data, max_iterations)
    if len(parmTuple0) == 4:
        return fitAny(_gaussian1D_4, parmTuple0, data, max_iterations)


def fitAnyND(f, parmTuple0, arr, max_iterations=None):
    """
    arr is an nd-array
    todo: optional "delta-Y"-array
    
    f is your 'model' function that takes two arguments:
    a tuple of parameters and x
    
    The function returns a list containing the optimal parameter values
    and the chi-squared value describing the quality of the fit.
    """

    from Scientific.Functions.LeastSquares import leastSquaresFit

    coords = N.transpose(N.indices(arr.shape), range(1,arr.ndim+1)+[0]).copy() # 'x' (tuples)
    coords.shape=(-1,arr.ndim)

    data = [(p, arr[tuple(p)]) for p in coords]

    return leastSquaresFit(f,parmTuple0,data, max_iterations)

def _gaussian2D_5_N(parms, coor_tuple):
    """parms: peakValue, sigmay,x,centery,x"""
    import Numeric as Num
    amp = parms[0]
    sig_y = parms[1]
    sig_x = parms[2]
    y0 = parms[3]
    x0 = parms[4]
    y = coor_tuple[-2]
    x = coor_tuple[-1]
    dy = (y-y0)/sig_y
    dx = (x-x0)/sig_x

    return amp*Num.exp(-0.5*( dy*dy + dx*dx) )
def _gaussian3D_7_N(parms, coor_tuple):
    """parms: peakValue, sigmaz,y,x,centerz,y,x"""
    import Numeric as Num
    amp = parms[0]
    sig_z = parms[1]
    sig_y = parms[2]
    sig_x = parms[3]
    z0 = parms[4]
    y0 = parms[5]
    x0 = parms[6]
    z = coor_tuple[-3]
    y = coor_tuple[-2]
    x = coor_tuple[-1]
    dz = (z-z0)/sig_z
    dy = (y-y0)/sig_y
    dx = (x-x0)/sig_x

    return amp*Num.exp(-0.5*( dz*dz + dy*dy + dx*dx) )
    

def fitGaussian2D(parmTuple0, arr, max_iterations=None):
    """parms: peakValue, sigmay,x,centery,x"""
    if arr.ndim != 2:
        raise ValueError, "arr must be of ndim 2"
    if len(parmTuple0) != 5:
        raise ValueError, "parmTuple0 must be a 5-tuple: peakValue, sigmay,x,centery,x"
    return fitAnyND(_gaussian2D_5_N, parmTuple0, arr, max_iterations)    
def fitGaussian3D(parmTuple0, arr, max_iterations=None):
    """parms: peakValue, sigmaz,y,x,centerz,y,x"""
    if arr.ndim != 3:
        raise ValueError, "arr must be of ndim 3"
    if len(parmTuple0) != 7:
        raise ValueError, "parmTuple0 must be a 7-tuple: peakValue, sigmaz,y,x,centerz,y,x"
    return fitAnyND(_gaussian3D_7_N, parmTuple0, arr, max_iterations)    


'''



def yGaussian(parms=(10,100), t=0):
    '''
    t can be a scalar or a vector
    returns y value(s) of a 1D-gaussian model

    parms can be tuple of ltength 2,3 or 4, with
    2: tuple is [sigma, peakVal]
    3: tuple is [x0, sigma, peakVal]
    4: tuple is [y0, x0, sigma, peakVal]

    x0 is center of gaussian (default 0)
    y0 is baseline offset gaussian (default 0)
    sigma is sigma (stddev) of gaussian
    peakval is  "center height" above baseline
    '''
    import fftfuncs as F

    if len(parms) == 4:
        y0,x0 = parms[:2]
    elif len(parms) == 3:
        y0,x0 = 0.0, parms[0]
    else:
        y0,x0 = 0.0, 0.0
    sigma, peakVal = parms[-2:]

    return y0+F.gaussian(t-x0, dim=1, sigma=sigma, peakVal=peakVal)

def yDecay(parms=(1000,10000,10), t=0):
    '''
    t can be a scalar or a vector
    returns y value(s) of a decay model
    parms:
        tuple of 1 or 3 or 5 or .. values
        first baseline = asymtote =y for t-> inf
        then pairs:
          first:  intercept of an exponetial decay
          second: half-time of an exponetial decay

        for more than 3 parameters: sum multiple such decay terms
     '''
    if len(parms) % 2==0:
        raise "number of parms must be odd: one offset and 2 more for each exponential"
    try:
        r = N.array(len(t)*(parms[0],))
    except: # t has no len
        r = parms[0]

    halfTimeScaler = N.log(2.)
    n = int( (len(parms)-1) / 2 )
    for i in range(n):
        r = r + parms[1+2*i] * N.exp(-t *halfTimeScaler/ parms[2+2*i])
#       r = r + parms[1+2*i] * N.exp(-t *halfTimeScaler/ float(parms[2+2*i]))
    return r
def yPoly(parms=(1,1,0), t=0):
    '''
    t can be a scalar or a vector
    returns y value(s) of a polygon model
    parms:
      baseline, first-order coeff, 2nd, ...
    '''
    r = 0.0
    for i in range(len(parms)):
        r = r + parms[i]*N.power(t, i)
    return r
def yLine(abTuple=(1,1), t=0):
    '''
    t can be a scalar or a vector
    returns y value(s) of a line model
    parms:
      abTuple: a,b  - as in y= ax + b
    '''
    a,b = abTuple
    return b+a*t





def fitAny(f, parmTuple0, data):
    '''
    data should be list of (x,y)  tuples
    TODO: or (x,y,deltaY)
    (instead of 'list' you can of course have an array w/
    shape=(n,2) or shape=(n,3), n beeing the number of data points

    if data.ndim == 1 or data.shape = (n,1) it fits w/ x=1,2,3,...n

    f is your 'model' function that takes two arguments:
    a tuple of parameters and x
    
    The function returns a list containing the optimal parameter values
    and the chi-squared value describing the quality of the fit.
    '''
    from scipy.optimize import leastsq

    data = N.asarray(data, dtype=N.float64)

    if len(data.shape) == 1:
        data = N.transpose(N.array([N.arange(len(data)), data]))
    elif data.shape[1] == 1:
        data = N.transpose(N.array([N.arange(len(data)), data][0]))

    x,y = data.T
    def func(p):
        return f(p, x)-y
    
    x0 = parmTuple0
    return leastsq(func, x0)#, args=(), Dfun=None,
                   #full_output=0, col_deriv=0,
                   #ftol=1.49012e-08, xtol=1.49012e-08, gtol=0.0, maxfev=0, epsfcn=0.0, factor=100, diag=None)
    
def fitDecay(y, p=(1000,10000,10)):
    '''
    see yDecay.
    p initial guess
    y vector of data points to be fit
    '''
    return fitAny(yDecay, p, y)

def fitGaussian(y, p=(0,10,100)):
    '''
    see yGaussian.
    p initial guess
    y vector of data points to be fit
    '''
    return fitAny(yGaussian, p, y)
#     from scipy.optimize import leastsq
    
#     n = len(y)
#     x = N.arange(n)
    
#     def func(p):
#         return yDecay(p, x)-y
    
#     x0 = p
#     return leastsq(func, x0)#, args=(), Dfun=None,
#                    #full_output=0, col_deriv=0,
#                    #ftol=1.49012e-08, xtol=1.49012e-08, gtol=0.0, maxfev=0, epsfcn=0.0, factor=100, diag=None)


def fitPoly(y, p=(1,1,1)):
    """
    see yPoly

    data should be list of y or (x,y)- or (x,y,deltaY)-tuples
    (instead of 'list' you can of course have an array w/
    shape=(n,2) or shape=(n,3), n beeing the number of data points

    uses polynomial 'model' ( U.yPoly )
    
    The function returns a list containing the optimal parameter values
    and the chi-squared value describing the quality of the fit.
    """


    return fitAny(yPoly, p, y)




























def noiseSigma(arr, backgroundMean=None):
    """ask Erik"""
    from numarray import nd_image as nd
    if backgroundMean is None:
        m = arr.mean() #20040707 nd.mean(arr)
        #       s = nd.standard_deviation(arr)
        #       nd.standard_deviation(d, d<m+s)
    else:
        m=backgroundMean
    mm = nd.mean(arr, labels=arr<m, index=None) - m

    #ask Erik:
    return N.sqrt( (mm**2) * N.pi * .5 )

def signal2noise(arr):
    from numarray import nd_image as nd
    ma = nd.maximum(arr)

    m = nd.mean(arr)
    #       s = nd.standard_deviation(arr)
    #       nd.standard_deviation(d, d<m+s)
    mm = nd.mean(arr, labels=arr<m, index=None) - m

    sigma = N.sqrt( (mm**2) * N.pi * .5 )
    #from Priithon import seb as S
    #print "debug:", S.median(arr)
    #from numarray import image
    #global med
    #med = arr
    #while not type(med) == type(1) or med.ndim > 0:
    #     med = image.median(med)
    #med = image.median(N.ravel(arr))
    #print "debug:", med
    print "debug - mean: %s      max: %s  meanLeft: %d     sigma: %s" %( m, ma, mm, sigma)
    return (ma-m) / sigma


def interpolate1d(x0, y, x=None):
    """
    assume a function f(x) = y
    defined by value-pairs in y,x
    evaluate this at x=x0

    note: x0 does not need to be one of the given values in x

    if x is None: use N.arange(len(y))

    more repeated evaluations 
    this is slow - because it remakes the spline fit every time
    """
    import scipy.interpolate
    if x is None:
        x = N.arange(len(y))
    else:
        ii = N.argsort(x)
        x = x[ii]
        y = y[ii]

    rep = scipy.interpolate.splrep(x, y, 
                                   w=None, xb=None, xe=None, 
                                   k=3, task=0, s=0.001, t=None, 
                                   full_output=0, per=0, quiet=1)

    return scipy.interpolate.splev(x0,rep)
        





def histogram(a, nBins=None, amin=None,amax=None, histArr=None, norm=False, returnTuple=False):
    """
    creates/returns  array with nBins int32 entries
       fills it with histogram of 'a'
    if amin and/or amax is None it calculates the min/max of a and uses that
    if nBins is None:
        nBins = int(amax-amin+1)
        if nBins < 10:
            nBins = 100
    if histArr is given it is used to fill in the histogram values
        then nBins must be None and histArr of dtype N.int32

    if norm:
       divide bins (=histArr) by sum of bins and convert to float64
    if returnTuple:
        return (histArr, nBins, amin, amax)
    """
    a = N.asarray(a)
    
    if amin is None and amax is None:
        amin = a.min()  
        amax = a.max()
    elif amin is None:
        amin = a.min()
    elif amax is None:
        amax = a.max()

    if histArr is not None:
        if nBins is not None:
            raise "only one of histArr and nBins can be given"
        if histArr.dtype != N.int32:
            raise "histArr must of dtype N.int32"
        if not histArr.flags.carray or  not histArr.dtype.isnative:
            raise RuntimeError, 'histArr must be a "native c(ordered)-array"'
        nBins = len(histArr)
    else:
        if nBins is None:
            nBins = int(amax-amin+1)
            if nBins < 10:
                nBins = 100

        histArr = N.empty( shape=(nBins,), dtype=N.int32 )

    a = _getGoodifiedArray(a)

    # NOTE: S.histogram *ignores* all values outside range (it does not count amax !!)
    #       it only count amin<= val < amax
    
    amaxTweaked = amin+nBins*(amax-amin)/(nBins-1)
    # CHECK numpy - why type(a.min())=numpy.float32 not SWIG compatible to float!
    S.histogram(a, float(amin),float(amaxTweaked), histArr)

    if norm:
        histArrNormed = N.empty( shape=(nBins,), dtype=N.float64 )
        histArrNormed[:] = histArr
        histArrNormed /= histArr.sum()
        histArr = histArrNormed

    if returnTuple:
        return (histArr, nBins, amin, amax)
    else:
        return histArr

def histogramXY(a, nBins=None, amin=None,amax=None, histArr=None, norm=False):
    '''returns flipped version of histogramYX
    use this e.g. in
     Y.plotxy( U.histogramXY( a ) )
    '''
    b,x = histogramYX(a, nBins, amin,amax, histArr, norm)
    return x,b

def histogramYX(a, nBins=None, amin=None,amax=None, histArr=None, norm=False):
    """returns same as U.histogram
       but also a "range array" amin,...amax with nBins entries
       """
    b,nBins,amin,amax = histogram(a,nBins,amin,amax, histArr, norm=norm, returnTuple=True)
    if norm:
        x,step = N.linspace(amin,amax, nBins, endpoint=True, retstep=True)
        b /= step
    else:
        x = N.linspace(amin,amax, nBins, endpoint=True)

    return b, x

def generalhistogram(a, weightImg, nBins=None, amin=None,amax=None):
    """
    creates/returns ("histogram") array with nBins entries of same dtype as weightImg
    while for a standard histogram one adds up 1s in bins for
          each time you encouter a certain value in a
    generalhistogram  adds the pixel value found in weightImg 
          each time it encouters a certain value in a (for that pixel)
    
    if amin and/or amax is None it calculates the min/max of a and uses that
    if nBins is None:
        nBins = int(amax-amin+1)
        if nBins < 10:
            nBins = 100
    """
    if amin is None and amax is None:
        amin = a.min()
        amax = a.max()
    elif amin is None:
        amin = a.min()
    elif amax is None:
        amax = a.max()

    if nBins is None:
        nBins = int(amax-amin+1)
        if nBins < 10:
            nBins = 100
    b = N.empty( shape=(nBins,), dtype=weightImg.dtype )

    a = _getGoodifiedArray(a)
    weightImg = _getGoodifiedArray(weightImg)

    # NOTE: S.histogram *ignores* all values outside range (it does not count amax !!)
    #       it only count amin<= val < amax
    
    amaxTweaked = amin+nBins*(amax-amin)/(nBins-1)
    # CHECK numpy - why type(a.min())=numpy.float32 not SWIG compatible to float!
    S.generalhist(a, weightImg, float(amin),float(amaxTweaked), b)

    return b
    

def topPercentile(img, percentile=1):
    """find Intens. for highest percentile

        slow!! ****** might only work for uint16 arr *********
    """
    import seb as S
    a = N.empty( shape=(1<<16), dtype=N.int32 ) # bins
    (mi,ma,mean,stddev) = S.histogram2(img, 0, (1<<16), a)
    nPix = N.prod( img.shape )


    a = _getGoodifiedArray(a)

    tp = S.toppercentile(a, nPix, int(ma), percentile)
    return tp

'''
def ffta(img):
    if len(img.shape) != 2:
        raise "2d only"


    import numarray as na
    from numarray import fft

    #f = fft.fft2d(img)
    #fr = na. abs( fft.real_fft2d(img).astype(na.Float32) ) 
    #if img.type

    fa = fft.fft2d(img).astype(na.Complex32) # fixme single float fft ?
    fa = na.abs(fa) # we want Float     - copy...
    na.log10(fa,fa)
    fa[0,0] = 1
    return fa

def fftc(img):
    if len(img.shape) != 2:
        raise "2d only"


    import numarray as na
    from numarray import fft

    #f = fft.fft2d(img)
    #fr = na. abs( fft.real_fft2d(img).astype(na.Float32) ) 
    #if img.type

    fa = fft.fft2d(img).astype(na.Complex32) # fixme single float fft ?
    #na.abs(fa, fa)
    #na.log10(fa,fa)
    fa[0,0] = 0
    return fa
def fftcinv(img):
    if len(img.shape) != 2:
        raise "2d only"


    import numarray as na
    from numarray import fft

    #f = fft.fft2d(img)
    #fr = na. abs( fft.real_fft2d(img).astype(na.Float32) ) 
    #if img.type

    fa = fft.inverse_fft2d(img).astype(na.Complex32) # fixme single float fft ?
    #na.abs(fa, fa)
    #na.log10(fa,fa)
    fa[0,0] = 0
    return fa
'''
def l2norm(a):
    """
    return the euclidian length of vector a
    return N.sqrt(a**2).sum())
    """
    a = N.asarray(a)
    return N.sqrt(a**2).sum()

def l1norm(a):
    """
    return the "abs"-norm of vector a
    return N.sum(abs(a))
    """
    a = N.asarray(a)
    return N.sum(abs(a))





def phase(a):
    """
    returns N.arctan2(a.imag, a.real)
    """
    return N.arctan2(a.imag, a.real)

def polar2cplx(aAbs,aPhase):
    """
    returns new complex array 'a' with
    a.real = aAbs * N.cos(aPhase)
    a.imag = aAbs * N.sin(aPhase)
    """
    if aAbs.dtype.type == N.float32:
        dtype = N.complex64
    else:   # HACK FIXME
        dtype = N.complex128

    a = N.empty(shape=aAbs.shape, dtype=dtype)
    a.real[:] = aAbs * N.cos(aPhase)
    a.imag[:] = aAbs * N.sin(aPhase)
    return a



def rot90(a, n):
    """return a.copy() rotated
    n == 1 --> counter-clockwise
    n == 2 --> 180 degrees
    n == 3 --> clockwise
    n ==-1 --> clockwise
    """
    if n == 2:
        b = a.copy()
        return b[::-1,::-1]
    else:
        b = N.transpose( a )
        if n == 1:
            return b[::-1]
        elif n==3 or n==-1:
            return b[:,::-1]
    raise "cannot rotated with n == %s"%n
    

def project(a, axis=0):
    """
    returns maximum projection along given [old: 'first'(e.g. z)] axis
    """
    if axis < 0:
        axis += a.ndim
    return N.maximum.reduce(a, axis)


def insert(arr, i, entry, axis=0):
    """returns new array with new element inserted at index i along axis
    if arr.ndim>1 and if entry is scalar it gets filled in (ref. broadcasting)

    note: (original) arr does not get affected
    """
    if i > arr.shape[axis]:
        raise IndexError, "index i larger than arr size"
    shape = list(arr.shape)
    shape[axis] += 1
    a= N.empty(dtype=arr.dtype, shape=shape)
    aa=N.transpose(a, [axis]+range(axis)+range(axis+1,a.ndim))
    aarr=N.transpose(arr, [axis]+range(axis)+range(axis+1,arr.ndim))
    aa[:i] = aarr[:i]
    aa[i+1:] = aarr[i:]
    aa[i] = entry
    return a


#######################################################################
######### stuff that works with float32 array (was: ... that uses Bettina's FORTRAN)
#######################################################################

def trans2d(inArr, outArr, (tx,ty,rot,mag,gmag2_axis,gmag2)):
    """
    first translates by tx,ty
    THEN rotate and mag and aniso-mag
        (rotation relative to img-center !
         positive angle moves object counter-clockwise)

    if outArr is None ret
    NOTE: tx,ty go positive for right/up
    (bettinas Fortran goes left/down !!!) 
"""
    # , (tx=0,ty=0,rot=0,mag=1,gmag2_axis=0,gmag2=1)):
    ret = 0
    if outArr is None:
        outArr = N.empty(shape=inArr.shape, dtype=N.float32)
        ret = 1
    checkGoodArrayF(outArr, 1, inArr.shape)

    inArr = _getGoodifiedArray(inArr)

    S.trans2d(inArr,outArr,(-tx,-ty,  rot,mag, gmag2_axis,gmag2) )
    if ret:
        return outArr


def translate2d(a,b,tx,ty):
    """ shift a in to b

    use bi-linear interpolation

    if b is None
      output array b is allocated and returned

    NOTE: tx,ty go positive for right/up
    (bettina's Fortran goes left/down !!!) 
    """
    rot,gmag,axis,gmag2 = 0, 1,0,1
    return trans2d(a,b,(tx,ty,  rot,gmag,axis,gmag2) )

def transmat2d(a,b,tx,ty, m11,m12,m21,m22, tx2=0,ty2=0):
    """
    transform a(input) into b(output) :
    first translates by tx,ty
    THEN apply rotate/skew
        (rotation relative to img-center !
         positive angle moves object counter-clockwise)

    (m11 m12)  is the 2d transformation matrix
    (m21 m22) 

    use bi-linear interpolation

    NOTE: tx,ty go positive for right/up
    (bettinas Fortran goes left/down !!!)

    tx2,ty2 is for an extra translating ?? before OR after ?>??
    """
    checkGoodArrayF(b, 1, a.shape)

    ny,nx = a.shape
    #20050502  # now we have a '-' here !!!!
    xc = (nx - 1.)*.5 + -tx  # ! Center of image.
    yc = (ny - 1.)*.5 + -ty

    a = _getGoodifiedArray(a)

    S.binterp2d(a,b, (m11,m12,m21,m22), xc,yc,  tx2,ty2)



def rot3d(a,b, angle, rot_axis=0):
    """ angle: in degree,
        rot_axis: axis to rotate the object about"""

    checkGoodArrayF(b, 1, a.shape)
    a = _getGoodifiedArray(a)
    
    import Priithon.seb as S
    cdr = N.arctan(1)/ 45
    c = N.cos(angle*cdr)
    s = N.sin(angle*cdr)

    tx=ty=tz=0

    if a.ndim == 2:
        a = a.view()
        b = b.view()        
        b.shape = a.shape = (1,) + a.shape

    xoff=0.5*(a.shape[2]-1)
    yoff=0.5*(a.shape[1]-1)
    zoff=0.5*(a.shape[0]-1)
    xc=xoff+tx                                    # Shift by -xt, -yt,-zt.
    yc=yoff+ty
    zc=zoff+tz 

    if rot_axis==0:
        S.rot3d(a,b,
                ( c,-s, 0,
                  s, c, 0,
                  0, 0, 1),
                1, xoff,yoff,zoff,xc,yc,zc)
    elif rot_axis==1:
        S.rot3d(a,b,
                ( c, 0, s,
                  0, 1, 0,
                 -s, 0, c),
                1, xoff,yoff,zoff,xc,yc,zc)
    elif rot_axis==2:
        S.rot3d(a,b,
                ( 1, 0, 0,
                  0, c,-s,
                  0, s, c),
                1, xoff,yoff,zoff,xc,yc,zc)
    else:
        print "*** bad rot_axis ***"
        

#######################################################################
######### stuff that used PIL
#######################################################################

def _getImgMode(im):
    cols = 1
    BigEndian = False
    if im.mode   == "1":
        t = N.uint8
        cols = -1
    elif im.mode == "L" or \
         im.mode == "P": #(8-bit pixels, mapped to any other mode using a colour palette)
        t = N.uint8
    elif im.mode == "I;16":
        t = N.uint16
    elif im.mode == "I":
        t = N.uint32
    elif im.mode == "F":
        t = N.float32
    elif im.mode == "RGB":
        t = N.uint8
        cols = 3
    elif im.mode == "RGBA":
        t = N.uint8
        cols = 4
    elif im.mode == "CMYK":
        t = N.uint8
        cols = 4
    elif im.mode == "I;16B":  ## big endian
        t = N.uint16
        BigEndian = True
    else:
        raise ValueError, "can only convert single-layer images (mode: %s)" % (im.mode,)

    nx,ny = im.size
    import sys
    isSwapped = (BigEndian and sys.byteorder=='little' or not BigEndian and sys.byteorder == 'big')
        
    return t,cols, ny,nx, isSwapped


def image2array(im, i0=0, iDelta=1, squeezeGreyRGB=True):
    """
    Convert image to numpy array

    if squeezeGreyRGB:
       test if an RGB (RGBA) image really just grey - 
         then return only one channel (others are identical)
    """
    
    import Image

    #HACK for multipage images
    nn = 0
    for i in range(i0, 100000, iDelta):
        try:
            im.seek(i)
            nn+=1
        except EOFError:
            break
    #def getLayerlayerToArray

    im.seek(i0)
    t,cols,ny,nx,isSwapped = _getImgMode(im)



    if nn == 1:
        #global a
        a = N.fromstring(im.tostring(), t)
        if cols == -1:
            raise NotImplementedError, "TODO: bit array: image size: %s  but array shape: %s" % (im.size, a.shape)
            # s = im.size[0]
            # return a
           
        elif cols>1:
            s = ( ny, nx, cols)
            #print "# multi color image [PIL mode: '%s']: orig shape=%s" % (im.mode,s), \
            #" --> return transposed! "
            a.shape = s
            a=a.transpose((2,0,1))
            #special treatment of "grey scale" images saved as RGB or RGBA
            if squeezeGreyRGB:
                if cols==3:
                    if (a[0] == a[1]).all() and \
                       (a[0] == a[2]).all():
                        a=a[0]
                elif cols==4:
                    if (a[0] == a[1]).all() and \
                       (a[0] == a[2]).all() and \
                       (a[0] == a[3]).all() or (a[3] == 0).all():  # CHECK
                        a=a[0]
            a=a.copy() # just copy() to get contiguous   
        else:
           a.shape = ( ny, nx )
    else:
        if cols == -1:
            raise NotImplementedError, "TODO a: bit array: image size: %s" % (im.size,)
        if cols > 1:
            a = N.empty(shape=(nn, cols, ny, nx), dtype=t)
            for i in range(nn):
                im.seek(i0+iDelta*i)
                x = N.fromstring(im.tostring(), t)
                x.shape = (ny, nx, cols)
                a[i] = x.transpose((2,0,1))
        else:
            a = N.empty(shape=(nn, ny, nx), dtype=t)
            for i in range(nn):
                im.seek(i0+iDelta*i)
                x = N.fromstring(im.tostring(), t)
                x.shape = (ny, nx)
                a[i] = x
        

    if isSwapped:
        a.byteswap(True)
        
    return a


def array2image(a):
    """Convert numpy array to image
       a must be of ndim 2 and dtype UInt8,Float32 or UInt16
       if a is of ndim 3: !!!
          a.shape[0] must be 3
            (3 sections: one for red, one for green and one for blue)
            dtype must be Uint8
    """
    
    import Image

    if a.ndim == 3:
        if a.shape[0] == 3:
            assert a.dtype==N.uint8
            a22 = N.transpose(a,(1,2,0)) # .copy()
            ii = Image.fromstring("RGB", (a.shape[-1],a.shape[-2]), a22.tostring())
            return ii
        elif a.shape[0] == 2:
            assert a.dtype==N.uint8
            a22 = N.transpose(a,(1,2,0)) # .copy()
            import fftfuncs as F
            a22 = N.append(a22,F.zeroArr(a22.dtype,a22.shape[:2]+(1,)), -1)
            ii = Image.fromstring("RGB", (a.shape[-1],a.shape[-2]), a22.tostring())
            return ii
        elif a.shape[0] == 4:
            assert a.dtype==N.uint8
            a22 = N.transpose(a,(1,2,0)) # .copy()
            ii = Image.fromstring("RGBA", (a.shape[-1],a.shape[-2]), a22.tostring())
            return ii
        else:
            raise ValueError, "only 2d greyscale or 3d (RGB[A]) supported"
    # else:  (see return above)
    if a.ndim != 2: 
        raise ValueError, "only 2d greyscale or 3d (RGB[A]) supported"

    if a.dtype.type == N.uint8:
        mode = "L"
    elif a.dtype.type == N.float32:
        mode = "F"
    elif a.dtype.type in ( N.int16, N.uint16 ):
        mode = "I;16"
    else:
        raise ValueError, "unsupported array datatype"
    return Image.fromstring(mode, (a.shape[1], a.shape[0]), a.tostring())
    #20040929 todo: try this:   return Image.frombuffer(mode, (a.shape[1], a.shape[0]), a._data)

def loadImg(fn, i0=0, iDelta=1, squeezeGreyRGB=True):
    """Loads image file (tiff,jpg,...) and return it as array

    if squeezeGreyRGB:
       test if an RGB (RGBA) image really just grey - 
         then return only one channel (others are identical)

    !!be careful about up-down orientation !!
    """

    #global im
    import Image
    im = Image.open(fn)
    return image2array(im, i0, iDelta, squeezeGreyRGB)

def loadImg_seq(fns, channels=None, verbose=0): #### #, i0=0, iDelta=1, squeezeGreyRGB=True):
    """
    Open multiple TIFF-files into a 3-(or 4-)D numpy stack.

    fns is a list of filenames or a glob-expression
    channels:
      specify 0 for R
              1 for B
              2 for G
              list of above for mnore than one
              None for all
    """
    import glob, Image
    if type(fns) is not type([]):
        fns = glob.glob( fns )
        fns.sort()

    n = len(fns)
    #print n
    #print fns

    fn = fns[0]
    im = Image.open(fn)
    dtype,cols, ny,nx = _getImgMode(im)
    del im

    if cols > 1:
        if channels is None:
            channels = range(cols)
        elif not hasattr(channels, "__len__"):
            channels = [channels]
        else:
            channels = list(channels)

        shape = (n,len(channels),ny,nx)
    else:
        shape = (n,ny,nx)
        
    a = N.zeros(dtype=dtype, shape=shape)
        

    for i,fn in enumerate(fns):
        if verbose:
            print i,
            Y.refresh()

        im = Image.open(fn)
        ##be more robust: 
        aa = loadImg(fn, squeezeGreyRGB=False)
        #         dtype2,cols2, ny2,nx2 = U._getImgMode(im)
        #         aa = image2array(im)
        if cols > 1:
            #             if cols2 == 1:
            #                 # what now: we just put data into channels[0] - set others to 0
            #                 aa = aa[channels]
            #             else:
            aa = aa[channels]
        a[i] = aa

    if verbose:
        print 
        Y.refresh()
    return a


def saveImg(arr, fn, forceMultipage=False):
    """
    Saves data array as image file (format from    extension !! .tif,.jpg,...)
    tries to use number format of 'arr'
    also supports multipage TIFF:
        3D arrays: grey (if more than 4 z-secs or forceMultipage==True)
        4D arrays: color (second dims must be of len 2..4 (RG[B[A]])"
       
    !!be careful about up-down orientation !!
    """

    arr = N.asarray(arr)
    if (arr.ndim == 3 and (len(arr)>4 or forceMultipage)) or \
            arr.ndim == 4:
        return saveTiffMultipage(arr, fn)

    im = array2image(arr)
    im.save(fn)

def _saveSeq_getFixedFN(fn, n):
    """
    check that fn contains a '%02d'-like part'
    autofix if necessary (add enough digits to fit n filenames)
    """
    try:
        __s = fn % 1 # test if fn contains '%d'
    except TypeError:
        import os
        fnf = os.path.splitext(fn)
        fns = '_%0' + '%d'%(int(N.log10(n-1))+1) +'d'
        fn = fnf[0] + fns + fnf[1]
    return fn

def saveImg_seq(arr, fn):
    """Saves 3D data array as 8-bit gray image file sequence (format from  extension !! .tif,.jpg,...)
    filename should contain a "template" like %02d - use '%%' otherwise inplace of single '%'
    template gets replaced with 00,01,02,03,...
    !!be careful about up-down orientation !!
    """
    arr = N.asarray(arr)
    #if arr.ndim != 3:
    #    raise "can only save 3d arrays"
    if not (arr.ndim == 3 or (arr.ndim == 4 and arr.shape[1] in (2,3,4))):
        raise ValueError, "can only save 3d arrays or 4d with second dim of len 2..4 (RG[B[A]])"

    fn = _saveSeq_getFixedFN(fn, len(arr))

    for i in range(arr.shape[0]):
        saveImg(arr[i], fn % i)

def saveImg8(arr, fn, forceMultipage=False):
    """Saves data array as 8-bit gray image file (format from  extension !! .tif,.jpg,...)
    be careful about up-down orientation !!
    if arr.dtype is not N.uint8  arr gets rescaled to 0..255
    also supports multipage TIFF:
        arr gets rescaled to 0..255 to match min..max of entire stack
        3D arrays: grey (if more than 4 z-secs or forceMultipage==True)
        4D arrays: color (second dims must be of len 2..4 (RG[B[A]])"
    """

    arr = N.asarray(arr)
    if (arr.ndim == 3 and (len(arr)>4 or forceMultipage)) or \
            arr.ndim == 4:
        return saveTiffMultipage(arr, fn, rescaleTo8bit=True)

    if not (arr.ndim == 2 or (arr.ndim == 3 and arr.shape[0] in (2,3,4))):
        raise ValueError, "can only save 2d greyscale or 3d (RGB[A]) arrays"
    
    if arr.dtype.type != N.uint8:
        mi,ma = float(arr.min()), float(arr.max())
        ra = ma-mi
        arr = ((arr-mi)*255./ra).astype(N.uint8)

    import Image
    im8 = array2image(arr)
    #20050711 im8= im.convert("L")
    im8.save(fn)

def saveImg8_seq(arr, fn):
    """Saves 3D data array as 8-bit gray image file sequence (format from  extension !! .tif,.jpg,...)
    filename must contain a "template" like %02d - use '%%' otherwise inplace of single '%'
    template gets replaced with 00,01,02,03,...
    !!be careful about up-down orientation !!
    arr gets rescaled to 0..255 to match min..max of entire stack
    """
    arr = N.asarray(arr)
    if arr.ndim != 3:
        raise "can only save 3d arrays"

    fn = _saveSeq_getFixedFN(fn, len(arr))

    mi,ma = float(arr.min()), float(arr.max())
    ra = ma-mi
    for i in range(arr.shape[0]):
        a=(arr[i]-mi)*255./ra
        saveImg(a.astype(N.uint8), fn % i)

def loadFits(fn, slot=0):
    """Loads FITC file and return it as array
    """
    import pyfits
    ff = pyfits.open(fn)
    return ff[ slot ].data

def saveFits(arr, fn, overwrite=1):
    import pyfits

    if overwrite:
        import os
        if os.path.exists(fn):
            os.remove(fn)

    fits_file = pyfits.HDUList()
    datahdu = pyfits.PrimaryHDU()
    shapehdu = pyfits.ImageHDU()
    datahdu.data = arr
    shapehdu.data = N.array(arr.shape)
    fits_file.append(datahdu)
    fits_file.append(shapehdu)
    fits_file.writeto(fn)

def saveTiffMultipage(arr, fn, rescaleTo8bit=False, **params):
    if arr.ndim == 4:
        if arr.shape[1] not in (2,3,4):
            raise ValueError, "can save 4d arrays (color) only with second dim of len 2..4 (RG[B[A]])"
    elif arr.ndim != 3:
        raise ValueError, "can only save 3d (grey) or 4d (color) arrays"

    fp = open(fn, 'w+b')

    ifd_offsets=[]

    if rescaleTo8bit:
        mi,ma = float(arr.min()), float(arr.max())
        ra = ma-mi        

    params["_debug_multipage"] = True
    for z in range(arr.shape[0]):
        if rescaleTo8bit:
            a=(arr[z]-mi)*255./ra
            ii = array2image(a.astype(N.uint8))
        else:
            ii = array2image(arr[z])

        fp.seek(0,2) # go to end of file
        if z==0:
            # ref. PIL  TiffImagePlugin
            # PIL always starts the first IFD at offset 8
            ifdOffset = 8
        else:
            ifdOffset = fp.tell()

        ii.save(fp, format="TIFF", **params)
        
        if z>0: # correct "next" entry of previous ifd -- connect !
            ifdo = ifd_offsets[-1]
            fp.seek(ifdo)
            ifdLength = ii._debug_multipage.i16(fp.read(2))
            fp.seek(ifdLength*12,1) # go to "next" field near end of ifd
            fp.write(ii._debug_multipage.o32( ifdOffset ))

        ifd_offsets.append(ifdOffset)
    fp.close()

def loadImageFromURL(url):
    """
    download url of an image file
    into local cache and 
    return numpy array 
    """
    import urllib
    fp = urllib.urlretrieve(url, filename=None, reporthook=None, data=None)
    #     >>> fp[0]
    #     'c:\docume~1\haase\locals~1\temp\tmpgpcmwo.jpg'
    #     >>> fp[1]
    #     Date: Sat, 29 Sep 2007 21:03:15 GMT
    #     Server: Apache/1.3.27 (Unix)  (Red-Hat/Linux)
    #     P3P: CP="NOI DSP COR NID ADM DEV TAI PSA PUBo STP PHY"
    #     Last-Modified: Mon, 18 Oct 1999 17:32:10 GMT
    #     ETag: "4b75a-7aca-380b599a"
    #     Accept-Ranges: bytes
    #     Content-Length: 31434
    #     Connection: close
    #     Content-Type: image/jpeg 
    #     >>> fp[2]
    #     IndexError: tuple index out of range
    arr = loadImg(fp[0])
    return arr


###############################################################
###############################################################

def calc_threshold_basic(a, histYX=None, dt=.5, nMax=100):
    """
    calculate a threshold value
    using the "Basic Global Thresholding" method
    described in Ch. 10.3.2 in "Digital Image Processing"

    returns threshold T

    stop iteration when T doesn't change more than dt
    or after nMax iterations

    histYX, is the histogram of a -- a tuple(binCount, binPixelValue)
    """

    if histYX is None:
        h,x = histogramYX(a)
    else:
        h,x = histYX

    m1,m2 = x[0],x[-1]
    T = .5*(m1+m2)
    for i in xrange(nMax):
        ix1=N.where(x<=T)[0]
        ix2=N.where(x> T)[0]
        m1 = (h[ix1]*x[ix1]).sum() / h[ix1].sum()
        m2 = (h[ix2]*x[ix2]).sum() / h[ix2].sum()

        Tnew = .5*(m1+m2)

        if abs(T-Tnew) < dt:
            return Tnew
        T=Tnew



def calc_threshold_otsu(a, histYX=None):
    """
    calculate a threshold value
    using "Otsu's Method"
    described in Ch. 10.3.3 in "Digital Image Processing"

    returns threshold T

    histYX, is the histogram of a -- a tuple(binCount, binPixelValue)
    """
    import fftfuncs as F

    if histYX is None:
        h,x = histogramYX(a)
    else:
        h,x = histYX

    p = F.zeroArrF(len(h))
    p[:] = h/h.sum()
    P = p.cumsum()
    m = (x*p).cumsum()
    m_G = m[-1]
    s2_B = (m_G*P - m)**2 / (P*(1-P))

    T = x[N.argmax(s2_B)] # findMax(

    #s2_G = ((x-m_G)**2*p).sum()
    #separability measure:
    #eta  =  s2_B/s2_G
    #eta[T]

    return T

def calc_threshold_otsu2(a, histYX=None):
    """
    calculate multiple (nT = 2 !!) threshold values
    using "Otsu's Method"
    described in Ch. 10.3.6 in "Digital Image Processing"

    returns array of nT(=2) thresholds (T1,T2,...)

    histYX, is the histogram of a -- a tuple(binCount, binPixelValue)
    """
    import fftfuncs as F

    if histYX is None:
        h,x = histogramYX(a)
    else:
        h,x = histYX

    m_G = (h*x).sum()/h.sum()  # global mean

    K = nT + 1 # number of classes
    T=N.arange(0,K+1)
    T[0]  = x[0] -1 # lower bound is fixed to min-1
    T[K]  = x[-1]+1 # upper bound is fixed to max+1

    p = F.zeroArrD(len(h))
    p[:] = h
    p/=h.sum()

    P  = F.zeroArrD(K)
    m  = F.zeroArrD(K)

    otsu2Img = F.zeroArrF(len(h), len(h))
    for T1 in x[1:]:
        for T2 in x[N.where((x>T1) & (x<x[-1]))]:

            T[1] = T1
            T[2] = T2
    
            ix =  [ N.where((x>T[i]) & (x<=T[i+1]))             for i in range(K) ]


            for i in range(K):
                P [i] =  p[ix[i]].sum()
                m [i] =  (p[ix[i]]*x[ix[i]]).sum() / P[i]

            s2_B = (P[i]*(m[i]-m_G)**2).sum()

            otsu2Img[T1,T2] = s2_B

    #s2_G = ((x-m_G)**2*p).sum()
    #separability measure:
    #eta  =  s2_B/s2_G
    #eta[T]

    return otsu2Img



def uu_encodestring(text, compress=True):
    """
    from http://effbot.org/librarybook/uu.htm
    seb added bz2 compression
    """
    import StringIO, uu, bz2
    fin = StringIO.StringIO(bz2.compress(text))
    fout = StringIO.StringIO()
    uu.encode(fin, fout)
    return fout.getvalue()

def uu_decodestring(text, decompress=True):
    """
    from http://effbot.org/librarybook/uu.htm
    seb added bz2 compression
    """
    import StringIO, uu, bz2
    fin = StringIO.StringIO(text)
    fout = StringIO.StringIO()
    uu.decode(fin, fout)
    return bz2.decompress(fout.getvalue())


def grep(pattern, *files):# , retList=False):
    """
    emulate grep-functionality

    #if retList:
        return tuple list of (file, lineNo, lineText)-tuple
    #else:
    #    print familiar output to stdout

    posted by Fredrik Lundh, October 25th, 2005
    http://bytes.com/forum/thread169012.html
    """
    #if retList:
    ret=[]
    search = re.compile(pattern).search
    for file in files:
        for index, line in enumerate(open(file)):
            if search(line):
                #if retList:
                ret.append( (file, str(index+1), line[:-1]) )
                #else:
                #    print ":".join((file, str(index+1), line[:-1]))
    #if retList:
            fns = '_%0' + '%d'%(int(N.log10(n))+1) +'d'
    return ret

def sgn(a):
    return N.sign(a)

def binaryRepr(x, count=8):
    """
    Integer to "binary string" ("101011")
    returns string of length count containing '0's and '1'
    building up the "binary representation" of x
    Count is number of bits
    
    Note: the inverse operation is done by int(xxx, 2)
    """
    return "".join(map(lambda i:str((x>>i)&1), range(count-1, -1, -1)))
    
def fib(max=100, startWith0=True):
    """uses generator to iterate over sequence of Fibonacci numbers
    """
    a, b = 0, 1
    if startWith0:
        yield a
    while 1:
        if b > max:
            return
        yield b
        a, b = b, a+b
def fib2(n):
    """
    direct calc (non-recursive) return n_th Fibonacci number (as float!)
    n=0 --> 0
    n=1 --> 1
    n=2 --> 1
    ...
    n should be <= 604 ;-( (as float)
    n should be <= 46  ;-( (if you want to convert to int)
    #http://en.wikipedia.org/wiki/Fibonacci_sequence
    #
    http://www.research.att.com/cgi-bin/access.cgi/as/njas/sequences/eisA.cgi?Anum=A000045
    """
    
    return ((1+N.sqrt(5))**n-(1-N.sqrt(5))**n)/(2**n*N.sqrt(5))

def primes(max=100):
    ps=[2]
    i = 3
    yield 2
    while i<=max:
        isPrime = 1
        for p in ps:
            if i % p == 0:
                isPrime=0
                break
        if isPrime:
            ps.append(i)
            yield i
        i+=1

def primeFactors(a, max=None, includeRemainder=False):
    """return list of a's prime factors
    if max is not None:
       largest prime in list will be max
        (as often as it would be in the complete list)
       in this case: if includeRemainder is True:
                     append remainder so that N.product(<list>) == a
    """
    f = []
    for p in primes(a):
        if max is not None and p>max:
            if includeRemainder and a>1:
                f.append(a)
            return f
        while a%p==0:
            f.append(p)
            a/=p
            if a == 1:
                return f
    return f

def factorial(n, _memo={0:1,1:1}):
    try: return _memo[n]
    except KeyError:
        result = _memo[n] = n * factorial(n-1)
        return result
fac = factorial

def gamma(x, _memo={.5:N.pi**.5,  1.:1.}):
    """
    return gamma function
    defined for integer and half-integer values

    you can use scipy.special.gamma() for the general case
    """
    try: return _memo[x]
    except KeyError:
        if x>0 and (x == int(x) or 2.*x % 2 == 1.):
            xx=x-1
            return (xx)*gamma(xx)
        else:
            raise ValueError, "we have gamma(x) only defined for x =.5, 1, 1.5,..."
    
def iterIndices(shape):
    if type(shape) == int:
        shape = (shape,)    
    if len(shape) == 1:
        for i in range(shape[0]):
            yield (i,)
    else:
        for i in range(shape[0]):
            for ii in iterIndices(shape[1:]):
                yield (i,) + ii
