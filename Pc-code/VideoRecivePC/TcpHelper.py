import socket
class TcpHelper:
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        #创建socket
    def CreateTcpServer(self,host,port):
        #创建TCP服务器
        self.socket.bind((host, port))
        self.socket.listen(5)
        return self.socket.accept()
    def connectToServer(self,host,port,timeOut):
        #客户端链接到服务器
        if(self.socket != None):
            self.socket.close()
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        #print(host)
        if(timeOut != -1):
            self.socket.settimeout(timeOut)
        self.socket.connect((host,port))

        #这里会进行阻塞，可以通过超时时间来进行
    def recv(self,len,timeout):
        if(timeout != -1):
            self.socket.settimeout(timeout)
        return self.socket.recv(len)
    def send(self,Data):
        return self.socket.send(Data)