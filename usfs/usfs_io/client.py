from iobase import USFSIOBase
from iobase import USFSException

class USFSIOClient(USFSIOBase):
    """
    A subset of commands that are "safe" to run from a remote machine
    as part of the USFS Shared FileSystem.

    e.g. runs ls and custom commands
    """
    pass
