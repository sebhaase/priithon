"""
This is supposed to be a "sparse" version of matplotlib.pylab.py
this should not include all the things already found in numpy
"""
import matplotlib, numpy

try:
    _use_called_
except NameError:
    _use_called_ = True
    matplotlib.use('WXAgg')

    from  matplotlib import pylab
    pylab.ion()
else:
    from  matplotlib import pylab


# P = new.module("pylab_sparse","""pylab module minus stuff alreay in numpy""")
for k,v in pylab.__dict__.iteritems():
    try:
       if k[:2] == '__' or v is numpy.__dict__[k]:
           continue
    except KeyError:
       pass
    #P.__dict__[k] = v
    exec("%s = pylab.%s" % (k,k))
# 20070802
# >>> len(dir(pylab))
# 441
# >>> len(dir(P))
# 346
# >>> P.nx.numpy.__version__
# '1.0.1'
# >>> N.__version__
# '1.0.1'
# >>> N.alltrue
# <function alltrue at 0x01471B70>
# >>> P.alltrue
# <function alltrue at 0x019142F0>
# >>> N.alltrue.__doc__
# 'Perform a logical_and over the given axis.'
# >>> P.alltrue.__doc__
# >>> #N.alltrue(x, axis=None, out=None)
# >>> #P.alltrue(x, axis=0)

del pylab, numpy
