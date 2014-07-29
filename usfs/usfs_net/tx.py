import socket
from usfs.usfs_lib.info import Console

class USFSNetTX(object):

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def __init__(self, target_host, target_port, payload):
        self.target_host = target_host
        self.target_port = target_port
        self.payload = payload

#    @staticmethod
#    def access(self):
#        pass

    def send(self):

        #self.recipient = (self.target_host, self.target_port)
        Console.console("Sending a packet to %s:%s" % (self.target_host, self.target_port))

        self.sock.sendto(
            self.payload,
            (self.target_host, self.target_port)
        )


if __name__ == '__main__':
    test = USFSNetTX(target_host="127.0.0.1",
                     target_port=1234,
                     payload="Hello!"

    )
    test.send()