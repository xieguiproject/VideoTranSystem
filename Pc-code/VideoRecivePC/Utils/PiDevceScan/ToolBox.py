import socket
import time
import re
def getLocalIp():
    """
    查询本机ip地址ew import QChartView pyqt
    :return:
    """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip
#获取当前的时间
def getNowTimeString():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
#获取时间
def getTimeCodeString():
    return time.strftime("%Y%m%d%H%M%S", time.localtime())


def GetLocalIPByPrefix(prefix):
    localIP = ''
    for ip in socket.gethostbyname_ex(socket.gethostname())[2]:
        if ip.startswith(prefix):
            localIP = ip

    return localIP
def getLocalIpList():
    return socket.gethostbyname_ex(socket.gethostname())[2]
def IpToBoardCastAddr(Ip):
    localip = Ip.split('.')
    localip = localip[0] + '.' + localip[1] + '.' + localip[2] + '.255'
    return localip

if __name__ == "__main__":
    print(getNowTimeString())
    print(getLocalIpList())
    pass
