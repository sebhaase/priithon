"""
Priithon: "we need some nice images" ...

# author of original version:  Dan Goodman
# FAST FRACTALS WITH PYTHON AND NUMPY 
# March 22, 2009, 4:06 pm 
# http://thesamovar.wordpress.com/2009/03/22/fast-fractals-with-python-and-numpy/
# modified for Priithon
"""
from __future__ import absolute_import
from numpy import *

def mandel(ny=512, nx=512, itermax=30, ymin=-1.25, ymax=1.25, xmin=-2, xmax=.6):
    """
    Fast mandelbrot computation using numpy.

    (nx, ny) are the output image dimensions
    x: real axis
    y: imaginary axis

    itermax is the maximum number of iterations to do
    ymin, ymax, xmin, xmax specify the region of the
    set to compute.
    """
    # The point of iy and ix is that they are 2D arrays
    # giving the y-coord and x-coord at each point in
    # the array. The reason for doing this will become
    # clear below...
    iy, ix = mgrid[0:ny, 0:nx]

    # Now y and x are the y-values and x-values at each
    # point in the array, linspace(start, end, n)
    # is an array of n linearly spaced points between
    # start and end, and we then index this array using
    # numpy fancy indexing. If A is an array and I is
    # an array of indices, then A[I] has the same shape
    # as I and at each place i in I has the value A[i].
    y = linspace(ymin, ymax, ny)[iy]
    x = linspace(xmin, xmax, nx)[ix]

    # c is the complex number with the given y, x coords
    c = x+complex(0,1)*y

    del y, x # save a bit of memory, we only need z

    # the output image coloured according to the number
    # of iterations it takes to get to the boundary
    # abs(z)>2
    img = zeros(c.shape, dtype=int)
    # Here is where the improvement over the standard
    # algorithm for drawing fractals in numpy comes in.
    # We flatten all the arrays iy, ix and c. This
    # flattening doesn't use any more memory because
    # we are just changing the shape of the array, the
    # data in memory stays the same. It also affects
    # each array in the same way, so that index i in
    # array c has y, x coords iy[i], ix[i]. The way the
    # algorithm works is that whenever abs(z)>2 we
    # remove the corresponding index from each of the
    # arrays iy, ix and c. Since we do the same thing
    # to each array, the correspondence between c and
    # the y, x coords stored in iy and ix is kept.
    iy.shape = \
        ix.shape = \
        c.shape = ny*nx

    # we iterate z->z^2+c with z starting at 0, but the
    # first iteration makes z=c so we just start there.
    # We need to copy c because otherwise the operation
    # z->z^2 will send c->c^2.
    z = copy(c)

    for i in xrange(itermax):
        if not len(z): break # all points have escaped

        # equivalent to z = z*z+c but quicker and uses
        # less memory
        multiply(z, z, z)
        add(z, c, z)

        # these are the points that have escaped
        rem = abs(z)>2.0

        # colour them with the iteration number, we
        # add one so that points which haven't
        # escaped have 0 as their iteration number,
        # this is why we keep the arrays iy and ix
        # because we need to know which point in img
        # to colour
        img[iy[rem], ix[rem]] = i+1

        # -rem is the array of points which haven't
        # escaped, in numpy -A for a boolean array A
        # is the NOT operation.
        rem = -rem

        # So we select out the points in
        # z, iy, ix and c which are still to be
        # iterated on in the next step
        z = z[rem]
        iy, ix = iy[rem], ix[rem]
        c = c[rem]

    return img

if __name__=='__main__':
    from pylab import *
    import time
    start = time.time()
    I = mandel(400, 400, 100, -1.25, 1.25, -2, .5)
    print 'Time taken:', time.time()-start
    I[I==0] = 101
    img = imshow(I, origin='lower left')
    img.write_png('mandel.png', noscale=True)
    print "saved image to 'mandel.png'"
    show()
