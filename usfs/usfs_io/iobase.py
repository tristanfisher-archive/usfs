#!/usr/bin/env python

from __future__ import with_statement

import abc
import os
import errno

from usfs.usfs_lib import file_utils
from usfs.usfs_lib.info import Console
from usfs.usfs_net import tx
from easyos import easyos


from fuse import FUSE, FuseOSError, Operations


class USFSException(Exception):
    def __init__(self, message):
        self.message = message


class USFSIOBase(Operations):

    __metaclass__ = abc.ABCMeta
    __default_mount_dir = easyos['mount_dir'] + '/usfs'

    #todo: gets called twice on init, not totally sure why.
    def make_mount_dir(self, dir=None):
        if dir is not None:
            file_utils._mkdir(dir)
        else:
            raise USFSException("Mount dir cannot be type: None")

    def __init__(self, root, mount_dir=__default_mount_dir):
        self.root = root
        self.mount_dir = mount_dir
        self.make_mount_dir(dir=mount_dir)

    # Helpers
    # =======
    def _full_path(self, partial):
        if partial.startswith("/"):
            partial = partial[1:]
        path = os.path.join(self.root, partial)
        return path

    def is_remote(self, cwd):
        return os.path.relpath(cwd, self.root).split(os.sep)[0] == 'users'

    # Filesystem methods

    def access(self, path, mode):

        full_path = self._full_path(path)

        if self.is_remote(full_path):
            tx.access()
        else:
            Console.console("Calling os.access on %s %s %s" % (path, mode, full_path))

        if not os.access(full_path, mode):
            raise FuseOSError(errno.EACCES)

    def getattr(self, path, fh=None):

        fh = fh if fh is not None else ''

        #Console.console("Calling os.lstat on %s %s" % (path, fh))

        full_path = self._full_path(path)
        st = os.lstat(full_path)
        return dict((key, getattr(st, key)) for key in ('st_atime', 'st_ctime',
                                                        'st_gid', 'st_mode', 'st_mtime', 'st_nlink', 'st_size', 'st_uid'))

    def readdir(self, path, fh):
        Console.console("Called readdir on %s" % path)
        full_path = self._full_path(path)

        dirents = ['.', '..']
        if os.path.isdir(full_path):
            dirents.extend(os.listdir(full_path))
        for r in dirents:
            yield r

    def readlink(self, path):
        Console.console("Called readlink on %s" % path)
        pathname = os.readlink(self._full_path(path))
        if pathname.startswith("/"):
            # Path name is absolute, sanitize it.
            return os.path.relpath(pathname, self.root)
        else:
            return pathname

    def rmdir(self, path):
        full_path = self._full_path(path)
        return os.rmdir(full_path)

    def mkdir(self, path, mode):
        return os.mkdir(self._full_path(path), mode)

    def statfs(self, path):
        #Console.console("Called statfs on %s" % path)
        full_path = self._full_path(path)
        stv = os.statvfs(full_path)
        return dict((key, getattr(stv, key)) for key in ('f_bavail', 'f_bfree',
                                                         'f_blocks', 'f_bsize', 'f_favail', 'f_ffree', 'f_files', 'f_flag',
                                                         'f_frsize', 'f_namemax'))

    def rename(self, old, new):
        return os.rename(self._full_path(old), self._full_path(new))

    def utimens(self, path, times=None):
        return os.utime(self._full_path(path), times)



    # File methods
    # ============

    def open(self, path, flags):
        print 'called open' + ' ' + path + ' ' + flags
        full_path = self._full_path(path)
        return os.open(full_path, flags)

    def create(self, path, mode, fi=None):
        print 'called create' + ' ' + path + ' ' + mode
        full_path = self._full_path(path)
        return os.open(full_path, os.O_WRONLY | os.O_CREAT, mode)

    def read(self, path, length, offset, fh):
        print 'called read' + ' ' + path
        os.lseek(fh, offset, os.SEEK_SET)
        return os.read(fh, length)


    def write(self, path, buf, offset, fh):
        print 'called write'
        os.lseek(fh, offset, os.SEEK_SET)
        return os.write(fh, buf)

    def truncate(self, path, length, fh=None):
        full_path = self._full_path(path)
        with open(full_path, 'r+') as f:
            f.truncate(length)

    def flush(self, path, fh):
        return os.fsync(fh)

    def release(self, path, fh):
        return os.close(fh)

    def fsync(self, path, fdatasync, fh):
        return self.flush(path, fh)


def main(mountpoint, root):
    FUSE(USFSIOBase(root), mountpoint, foreground=True)

if __name__ == '__main__':

    from easyos import easyos

    mount_dir = easyos['mount_dir']+'/usfs'
    target_dir = easyos['current_user_desktop'] + '/usfs_target'

    test_dir = USFSIOBase(root="/Users/tfisher/Desktop/usfs_target")

    main(mount_dir, target_dir)

    #TODO: this is _so_ ugly
    def cleanup_task():
        try:
            os.removedirs(mount_dir)
        except OSError, e:
            print e

    import atexit
    atexit.register(cleanup_task)
