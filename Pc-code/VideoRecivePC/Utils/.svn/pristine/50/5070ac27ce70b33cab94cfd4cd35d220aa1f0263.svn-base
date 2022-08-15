#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# exit interrupt lib
import socket
import time
import re
import platform
import subprocess
from subprocess import Popen, PIPE
import re
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
    if platform.system().lower() == 'windows':
        return socket.gethostbyname_ex(socket.gethostname())[2]
    elif platform.system().lower() == 'linux':
        AllNetDeviceList = []


        #树莓派linux下使用ifconfig命令获取所有的ip地址
        p = subprocess.Popen('ifconfig', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        Lines = p.stdout.readlines()
        Count = 0
        #print(Lines)
        for line in Lines:
            try:
                Ip = re.search(r"(([01]?\d?\d|2[0-4]\d|25[0-5]\d)\.){3}([01]?\d?\d|2[0-4]\d|25[0-5]\d)", str(line))[0]
                if(Ip != '127.0.0.1' and Ip.split('.')[-1] != '1'):
                    # 取出上一行的网络名
                    DeviceIpList = {}
                    NetName = str(str(Lines[Count - 1]).split(':')[0][2:])
                    #测试中发现有可能无法获取MAC地址
                    try:
                        MacAddr = str(str(Lines[Count + 3]))
                        MacAddr = re.findall(re.compile(r'(?:[0-9a-fA-F]:?){12}'),MacAddr)[0]
                    except:
                        MacAddr = ''
                    DeviceIpList['NetName'] = NetName

                    DeviceIpList['ip'] = Ip
                    DeviceIpList['Mac']  = MacAddr
                    AllNetDeviceList.append(DeviceIpList)
            except:
                pass
            Count += 1
        return AllNetDeviceList
def checkCamreaStatus():
    #检查摄像头的状态
    p = subprocess.Popen('ls /dev/video0', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    try:
        Lines = p.stdout.readlines()
        if(str(Lines[0]).index('/dev/video0') > 0):
            return '/dev/video0'
        else:
            return '未检测到摄像头'
    except:
        return '未检测到摄像头'
def getUUID():
    #获取设备的UUID，一般树莓派下我们就使用SerialCode,ubuntu下使用uuid
    p = subprocess.Popen('sudo blkid', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    Lines = p.stdout.readlines()
    for line in Lines:
        line = str(line)
        if(line.find("/dev/sda1") > 0):
            startcut = line.find('UUID="') + 6
            endcut = startcut + 36
            uuid = str(line[startcut:endcut])
    return uuid
def getPiDeviceInfo():
    #获取树莓派的设备信息
    p = subprocess.Popen('cat  /proc/cpuinfo', shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    Lines = p.stdout.readlines()
    try:
        SerialCode = str(str(Lines[-2]).split(':')[1][1:-3])
        Model = str(str(Lines[-1]).split(':')[1][1:-3])
    except:
        SerialCode = getUUID()
        Model = 'Ubuntu'
    return SerialCode,Model
def IpToBoardCastAddr(Ip):
    localip = Ip.split('.')
    localip = localip[0] + '.' + localip[1] + '.' + localip[2] + '.255'
    return localip
if __name__ == "__main__":
    print(getNowTimeString())
    print(getLocalIpList())
    getPiDeviceInfo()
    print(checkCamreaStatus())
    pass
