#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# exit interrupt lib
#该脚本用于扫描树莓派，这样自动扫描树莓派得到树莓派的ip地址
from ToolBox import *
from socket import *
import _thread
import time
import json
import os
import sys
from threading import Semaphore
from config import CONFIG


class PiDeviceScan:
    def __init__(self,callback = None):
        self.udpSocket = socket(AF_INET, SOCK_DGRAM)
        HostAddr = ("0.0.0.0", 6666) #本机地址
        self.udpSocket.bind(HostAddr)
        self.udpSocket.setsockopt(SOL_SOCKET, SO_BROADCAST, 1) #创建广播
        self.Sem = Semaphore(1)

        self.DeviceIpInfo = getLocalIpList()  # 获取所有的ip地址信息
        self.callback = callback
        self.SerialCode,self.Model = getPiDeviceInfo()
        self.config = CONFIG('config.ini')

        _thread.start_new_thread(self.RunAPP,())
        _thread.start_new_thread(self.check, ())
    def getAutoStart(self):
        #获取开机启动项
        AutoStartList = list()
        self.config.Sem.acquire()
        sections = self.config.config.sections()
        for section in sections:
            #print(section)
            Item = list()
            Item.clear()
            Item.append(section)
            Item.append(self.config.getKeyValue(section,'cmdString'))
            AutoStartList.append(Item)
        self.config.Sem.release()
        return AutoStartList
        pass
    def RunAPP(self):
        #1、获取所有启动项
        self.AutoStartList = self.getAutoStart()
        for StartItem in self.AutoStartList:
            #os.system()
            pass
            #print(subprocess.Popen(StartItem[1], shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).pid)
    def check(self):
        while (True):
            '''
            1、树莓派关机命令
            2、树莓派重启命令
            3、树莓派ip地址
            '''
            self.CamreaStatus = checkCamreaStatus()
            data, addr = self.udpSocket.recvfrom(1024)
            data = data.decode('utf-8')
            jsonobj = json.loads(data)
            #print(data)
            if (jsonobj['cmd'] == 'scan'):
                respcmd = "{\"cmd\":\"deviceinfo\",\"IpList\":["
                for item in self.DeviceIpInfo:
                    if(item == self.DeviceIpInfo[-1]):
                        respcmd = respcmd + "{\"NetName\":\"" + item['NetName'] + "\",\"Ip\":\"" + item['ip'] + "\",\"Mac\":\"" + item['Mac'] + "\"}"
                    else:
                        respcmd = respcmd + "{\"NetName\":\"" + item['NetName'] + "\",\"Ip\":\"" + item['ip'] + "\",\"Mac\":\"" + item['Mac'] + "\"},"
                respcmd = respcmd + "],\"AutoStartList\":["
                AutoStartList = self.getAutoStart()
                for item in AutoStartList:
                    if (item == AutoStartList[-1]):
                        respcmd = respcmd + "{\"appName\":\"" + item[0] + "\",\"cmdString\":\"" + item[1] + "\"}"
                    else:
                        respcmd = respcmd + "{\"appName\":\"" + item[0] + "\",\"cmdString\":\"" + item[1] + "\"},"
                respcmd = respcmd + "],"
                respcmd = respcmd + "\"SerialCode\":" + "\"" + self.SerialCode + \
                          "\",\"Model\":" + "\"" + self.Model + "\",\"CamreaStu\":" + "\"" + self.CamreaStatus + "\"}"

                respcmd = str(respcmd).encode('utf-8')
                print(respcmd)
                self.udpSocket.sendto(respcmd, addr)
            elif(jsonobj['cmd'] == 'reboot'):
                os.system("sudo reboot")
            elif(jsonobj['cmd'] == 'poweroff'):
                os.system('sudo shutdown -h now')
            elif(jsonobj['cmd'] == 'addstartitem'):
                pass
                print("set")
                #z曾加启动项

if __name__ == "__main__":
    pi = PiDeviceScan()
    while(True):
        time.sleep(1)

