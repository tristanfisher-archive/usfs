import socket
import os

from functools import partial

#from . import tx
from usfs.usfs_lib.exceptions import USFSNetException

#from usfs.usfs_lib.exceptions import USFSNetException
from usfs.usfs_lib.info import Console

#import tx

RX_PORT = os.environ.get('usfs_bind_ip') or '1234'

class USFSNetRX(object):

    def __init__(self, listen_protocol="udp", listen_ip=None, listen_port=RX_PORT):
        self._listen_protocol = None
        self.listen_protocol = listen_protocol
        self._listen_ip = None
        self.listen_ip = listen_ip
        self.buffer_size = 1024
        self.listen_port = int(listen_port)

        #sock is 'internet type' with the return of the property for listen_protocol
        self._sock = None
        #socket.socket(socket.AF_INET, self._listen_protocol)
        self.sock = None

    @property
    def listen_protocol(self):
        return self._listen_protocol

    @listen_protocol.setter
    def listen_protocol(self, proto):
        proto = proto.lower()

        if proto == "tcp" or proto == "sock_stream":
            self._listen_protocol = socket.SOCK_STREAM
        elif proto == "udp" or proto == "sock_dgram":
            self._listen_protocol = socket.SOCK_DGRAM
        else:
            raise USFSNetException("Protocol must be of type UDP or TCP")

    @property
    def listen_ip(self):
        return self._listen_ip

    @listen_ip.setter
    def listen_ip(self, ip):

        if isinstance(ip, str):
            ip = ip.lower()

        if ip == "all":
            self._listen_ip = "0.0.0.0"
        elif ip == "localhost" or ip is None:
            self._listen_ip = "localhost"
        else:
            self._listen_ip = ip

    @property
    def sock(self):
        return self._sock

    @sock.setter
    def sock(self, _lp):
        _lp = self._listen_protocol
        #socket.socket(socket.AF_INET, self._listen_protocol)
        _sockfunc = partial(socket.socket, socket.AF_INET)
        self._sock = _sockfunc(_lp)

    def stub_info(self, data, *args):
        # Informative messages do not require an acknowledgement.
        Console.stdout(str(data))

    def stub_io(self, data, addr, *args):
        # IO messages should respond to the sender with data or an error message.
        print "io func|" + str(data)

        #tx.USFSNetTX(self.target_hosts )

    def noop(self, *args): pass

    def parse_stream(self, sock_recv, *args, **kwargs):
    # todo: how to get msg class? first N bytes?, fixed N-char?

        #Class, message. If we get an io, call the right class.
        #if we get a noop, do nothing, it's just extra info.

        message_action_lookup = {
            'io': self.stub_io,
            'info': self.stub_info,
            'noop': self.noop
        }

        data, addr = sock_recv

        try:
            return message_action_lookup[data](data, addr)
        except KeyError, e:
            #or return noop to prevent crashing.
            return "No handler found for %s" % data


    def bind(self):
        Console.console("Binding a type %s socket to %s:%s" % (self._listen_protocol, self._listen_ip, self.listen_port))
        self.sock.bind((self._listen_ip, self.listen_port))


        while True:
            sock_recv = self.sock.recvfrom(self.buffer_size)
            self.parse_stream(sock_recv)

# TODO:
'''
- define datastructure
- send callback
    - if just informative packet, send back general ack
    - if a request for data, the data is the ack (e.g. yielding access())

'''

if __name__ == '__main__':
    test_socket = USFSNetRX()
    test_socket.bind()


