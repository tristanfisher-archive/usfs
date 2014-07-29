import socket
import os

from usfs.usfs_lib.exceptions import USFSNetException

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
        self.sock = socket.socket(socket.AF_INET, self._listen_protocol)

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

    def bind(self):

        self.sock.bind((self._listen_ip, self.listen_port))

        while True:
            data, addr = self.sock.recvfrom(self.buffer_size)
            print "from %s : %s" % (addr, data)


if __name__ == '__main__':
    test_socket = USFSNetRX()
    test_socket.bind()


