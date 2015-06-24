import os
import sys
import errno

from easyos import easyos

# Operations is the subclass-able FUSE obj
from fuse import FUSE, Operations, FuseOSError



#TODO: remove


#class USFSIOBase(Operations):
class USFSIOBase(object):
    '''
    general purpose initialization and methods
    '''

    def __call__(self, op, *args):
        if not hasattr(self, op):
            raise FuseOSError('error!')
        return getattr(self, op)(*args)

    def __init__(self, root):
        self.root = root

    def create(self, path, mode, fi=None):
        pass

    def destroy(self, path):
        pass

    def read(self, path, size, offset, fh):
        pass

    def readdir(self, path, fh):
        pass

    def write(self, path, data, offset, fh):
        pass


#def instantiate(directory, mountpoint, foreground_bool=True):
#    FUSE(USFSIOBase(directory), mountpoint, foreground=foreground_bool)

if __name__ == '__main__':

    root = '/parking'
    mountpoint = '/Volumes/usfs'

    FUSE(USFSIOBase(root), mountpoint, foreground=True)

#def main(mountpoint, root):
#    FUSE(Passthrough(root), mountpoint, foreground=True)

