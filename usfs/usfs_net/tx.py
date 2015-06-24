import socket

#
#  TODO: I want this to work without the awful python -m path.to.module.py
#
#
from ..usfs_lib.info import Console

class USFSNetTX(object):

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def __init__(self, target_host, target_port, payload):
        self.target_host = target_host
        self.target_port = target_port
        self.payload = payload

        '''
        source ip
        source rx port (for callbacks)
        #how to get public ip
        source prococol (can be inferred by socket type)
        dest protocol (obviously inferred by socket type)
        '''

    def pack_struct(self): pass


    def ack(self):
        pass

    # http://en.wikipedia.org/wiki/UDP_hole_punching

#    @staticmethod
#    def access(self):
#        pass


    def send(self):

        #hash of command?

        #self.recipient = (self.target_host, self.target_port)
        Console.stdout("Sending a packet to %s:%s" % (self.target_host, self.target_port))

        self.sock.sendto(
            self.payload,
            (self.target_host, self.target_port)
        )

    def send_binary(self):
        #chunk data and do checksums?
        pass


if __name__ == '__main__':
    test = USFSNetTX(target_host="127.0.0.1",
                     target_port=1234,
                     payload="io"

    )
    test.send()


