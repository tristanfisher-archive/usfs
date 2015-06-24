
import sys
from easyos import easyos

def install_fuse_msg(_os):

    _os = str(_os).lower()

    messages = {
        "darwin": "install FUSE using https://github.com/osxfuse/osxfuse",
        "debian": "aptitude install fuse"
    }

    return messages[_os]

try:
    import fuse
    raise EnvironmentError
except EnvironmentError:
    sys.exit(install_fuse_msg(easyos['os']))