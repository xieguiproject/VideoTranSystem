from socket import *

class UdpHelper(object):
    def __init__(self,host,port):
        self.udpSocket = socket(AF_INET, SOCK_DGRAM)
        HostAddr = (host, port)
        self.udpSocket.bind(HostAddr)
    def CreateUdpBoardCast(self):
        self.udpSocket.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
    def send(self,data,Address):
        return self.udpSocket.sendto(data,Address)

    def recv(self,recvsize):
        return self.udpSocket.recvfrom(recvsize)
    def __del__(self):
        self.udpSocket.close()
