from socket import *

class UdpHelper(object):
    def __init__(self,host,port):
        #创建一个UDP
        self.udpSocket = socket(AF_INET, SOCK_DGRAM)
        HostAddr = (host, port)
        self.udpSocket.bind(HostAddr)
    def CreateUdpBoardCast(self):
        self.udpSocket.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
    def sendto(self,data,Address):
        return self.udpSocket.sendto(data,Address)
        #发送UDP数据
    def recvfrom(self,recvsize):
        return self.udpSocket.recvfrom(recvsize)
        #接受UDP数据
    def __del__(self):
        self.udpSocket.close()
