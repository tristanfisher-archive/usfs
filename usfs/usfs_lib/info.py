from __future__ import print_function
from easyos import easyos
from usfs.usfs_lib import file_utils


import logging
import os
import sys


log_dir = os.path.join(easyos['tmp_dir'] + '/usfs/')
file_utils._mkdir(log_dir)

verbose_format = logging.Formatter('%(levelname)s :: %(asctime)s :: Thread %(thread)d :: %(name)s  - %(message)s')
standard_format = logging.Formatter('%(levelname)s :: %(asctime)s :: %(name)s  - %(message)s')
console_format = logging.Formatter('%(asctime)s :: %(name)s  - %(message)s', "%H:%M:%S")

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

log_file = logging.FileHandler(log_dir + 'usfs.log')
log_file.setLevel(logging.DEBUG)
log_file.setFormatter(standard_format)
logger.addHandler(log_file)

#Console, non-file "log." Not associated as a handler for logger.
log_console = logging.getLogger(__name__)
_lc = logging.StreamHandler(sys.stdout)
_lc.setFormatter(console_format)
_lc.setLevel(logging.INFO)
log_console.addHandler(_lc)
log_console.setLevel(logging.INFO)

class Console(object):

    log_file = sys.stdout

    @classmethod
    def log(cls, msg, log_file=log_file, log_level=logging.DEBUG):
        pass

    @classmethod
    def console(cls, msg):
        log_console.info(msg)

    output = console

    @classmethod
    def stderr(cls, msg, prefix_msg='', **kwargs):
        print(prefix_msg + msg, file=sys.stderr, **kwargs)

    @classmethod
    def stdout(cls, msg, prefix_msg='', **kwargs):
        print(prefix_msg + msg, file=sys.stdout, **kwargs)
