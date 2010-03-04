# read_spe.py

"""
Priithon: reader for Hamamatzu(?) SPE files

# http://www.scipy.org/Cookbook/Reading_SPE_files
# http://forums.wolfram.com/student-support/topics/8778
"""
from __future__ import absolute_import

__author__  = "Sebastian Haase <haase@msg.ucsf.edu>"
__license__ = "BSD license - see LICENSE file"

import numpy as N

_type_dtype_map = { 
    0: N.float32,
    1: N.int32,
    2: N.int16,
    3: N.uint16,
}
class File(object):
    
    def __init__(self, fname):
        self._fid = open(fname, 'rb')
        self._load_size()

    def _load_size(self):
        self._xdim = N.int64(self.read_at(42, 1, N.uint16)[0])
        self._ydim = N.int64(self.read_at(656, 1, N.uint16)[0])
        self._zdim = N.int64(self.read_at(1446, 1, N.int32)[0])
        self._type = self.read_at(108, 1, N.int16)[0]
        self._dtype = _type_dtype_map[ self._type ]


    def get_shape(self):
        return (self._zdim, self._ydim, self._xdim)

    def read_at(self, pos, size, ntype):
        #use memmap instead  self._fid.seek(pos)
        #use memmap instead  return N.fromfile(self._fid, ntype, size)
        return N.memmap(self._fid, dtype=ntype, mode='r', offset=pos, shape=size)

    def load_img(self):
        img = self.read_at(4100, self._zdim * self._xdim * self._ydim, self._dtype)
        img.shape = self.get_shape()
        return img

    def close(self):
        self._fid.close()

def load(fname):
    fid = File(fname)
    img = fid.load_img()
    fid.close()
    return img

if __name__ == "__main__":
    import sys
    img = load(sys.argv[-1])
