#该脚本用于扫描树莓派，这样自动扫描树莓派得到树莓派的ip地址
from Utils.PiDevceScan.ToolBox import *
from socket import *
import _thread
import time
import json
import os
import sys
from threading import Semaphore
from Utils.PiDevceScan.PiSDeviceScanWidget import  Ui_PiDeviceScanWidget
from Utils.PiDevceScan.SSHClientCtl import SSHClient
from Utils.PiDevceScan.StartUpItemCtl import StartUpItem
from PyQt5.QtWidgets import  *
from PyQt5.QtCore import pyqtSlot,pyqtSignal,Qt,QDateTime,QTimer
from PyQt5.QtWidgets import QMainWindow
from PyQt5 import QtGui,QtWidgets
from PyQt5.QtGui import QPainter, QPalette,QPen,QColor
import dlib
from threading import Semaphore
import cv2
import _thread
import numpy as np
import time
import os
from PIL import Image, ImageTk,ImageDraw, ImageFont
from PyQt5.QtChart import QChart,QSplineSeries,QChartView, QPieSeries, QPieSlice,QDateTimeAxis,QValueAxis
import subprocess
from subprocess import Popen, PIPE

class PiDeviceScan(QMainWindow, Ui_PiDeviceScanWidget):
    def __init__(self, parent=None):
        super(PiDeviceScan, self).__init__(parent)
        self.setupUi(self)
        self.udpSocket = socket(AF_INET, SOCK_DGRAM)
        HostAddr = ("0.0.0.0", 6667) #本机地址

        self.udpSocket.bind(HostAddr)
        self.udpSocket.setsockopt(SOL_SOCKET, SO_BROADCAST, 1) #创建广播
        self.LocalIpList = getLocalIpList() #获取所有的ip地址
        self.BoardCastAddr = []
        self.Sem = Semaphore(1)
        self.piDeviceList = [] #设备列表

        self.OnlineCallbackList = []
        self.DownLineCallbackList= []
        self.AutoStartList = []
        for LocalIp in self.LocalIpList:
            self.BoardCastAddr.append((IpToBoardCastAddr(LocalIp),6666))
        #print(self.BoardCastAddr)
        _thread.start_new_thread(self.scan,())
        _thread.start_new_thread(self.check,())
        #创建一个定时器，定时分析一下设备是否在线
        self.CheckOnlineTimer = QTimer()
        self.CheckOnlineTimer.timeout.connect(self.CheckDeviceOnline)
        self.CheckOnlineTimer.start(4000)
        self.tableWidgetInit()
    def tableWidgetInit(self):
        self.tableWidget_DeviceInfo.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)  # 设置表格未均分模式
        self.tableWidget_DeviceInfo.setContextMenuPolicy(Qt.CustomContextMenu)# 允许生成右击菜单
        self.tableWidget_DeviceInfo.customContextMenuRequested.connect(self.tableDeviceInfoMenu)
    def PowerOff(self,DeviceIpList):
        sendmsg = "{\"cmd\":\"poweroff\"}"
        sendmsg = str(sendmsg).encode('utf-8')
        for Address in DeviceIpList:
            if (Address != ''):
                self.udpSocket.sendto(sendmsg, (Address, 6666))
    def Reboot(self,DeviceIpList):
        sendmsg = "{\"cmd\":\"reboot\"}"
        sendmsg = str(sendmsg).encode('utf-8')
        for Address in DeviceIpList:
            if(Address != ''):
                self.udpSocket.sendto(sendmsg, (Address,6666))
    def tableDeviceInfoMenu(self,pos):
        row_num = -1
        for i in self.tableWidget_DeviceInfo.selectionModel().selection().indexes():
            row_num = i.row()
        if(row_num == -1):
            return
        menu = QMenu()  # 实例化菜单

        DeviceCtlMenu = QMenu(u"设备电源控制")
        DevicePowerOff = DeviceCtlMenu.addAction(u"设备关机")
        DeviceReboot = DeviceCtlMenu.addAction(u"设备重启")

        item1 = menu.addMenu(DeviceCtlMenu)

        StartupItem = menu.addAction(u"开机启动项")
        SSHMenu = menu.addAction(u"SSH登录")
        VncMenu = menu.addAction(u"VNC登录")
        FtpMenu = menu.addAction(u"FTP登录")

        action = menu.exec_(self.tableWidget_DeviceInfo.mapToGlobal(pos))
        DeviceIpList = [self.tableWidget_DeviceInfo.item(row_num, 1).text(),
                        self.tableWidget_DeviceInfo.item(row_num, 3).text()]
        if(action == DeviceReboot):
            self.Reboot(DeviceIpList)
        if(action == DevicePowerOff):
            self.PowerOff(DeviceIpList)
        if(action == StartupItem):
            #开机启动项
            self.StartUpItems = StartUpItem(self)
            self.StartUpItems.show()
            try:
                self.StartUpItems.addStartupItemRecd(self.AutoStartList,0) #将列表中的选项全部插入表格中
            except:
                pass
            pass
        if(action == FtpMenu):
            if (len(self.tableWidget_DeviceInfo.item(row_num, 0).text()) > 20):
                _thread.start_new_thread(self.ftp_process, (DeviceIpList[0],))
            else:
                _thread.start_new_thread(self.ftp_process, (DeviceIpList[0], 'pi', '1'))
        if(action == VncMenu):
            if (len(self.tableWidget_DeviceInfo.item(row_num, 0).text()) > 20):
                _thread.start_new_thread(self.vnc_process, (DeviceIpList[0],))
            else:
                _thread.start_new_thread(self.vnc_process, (DeviceIpList[0], 'pi', '1'))
        if(action == SSHMenu):
            #self.SSHClientItem = SSHClient(self)
            #self.SSHClientItem.connect(DeviceIpList[0],'smarthome','1314520')
            #self.SSHClientItem.show()
            #for ip in DeviceIpList:
            if(len(self.tableWidget_DeviceInfo.item(row_num,0).text()) > 20):
                _thread.start_new_thread(self.ssh_process,(DeviceIpList[0],))
            else:
                _thread.start_new_thread(self.ssh_process, (DeviceIpList[0],'pi','1'))
        #检测菜单按钮按下的情况
    def ftp_process(self,host,user = 'smarthome',passwd = '1314520'):
        cmd = 'WinSCP.exe %s@%s' % (user, host)
        p = subprocess.Popen(cmd, shell=True,stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        #os.system(cmd)
        pass
    def vnc_process(self,host,user = 'smarthome',passwd = '1314520'):
        cmd = 'VNC-Viewer.exe  -UserName %s %s' % (user, host)
        p = subprocess.Popen(cmd, shell=True,stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        #os.system(cmd)
        # print(p.stdout.readlines())
    def ssh_process(self,host,user = 'smarthome',passwd = '1314520'):
        cmd = 'putty.exe  -ssh -l %s -pw %s %s' % (user,passwd,host)
        p = subprocess.Popen(cmd, shell=True,stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        os.system(cmd)
        print(p.stdout.readlines())
    def CheckDeviceOnline(self):
        self.Sem.acquire()
        count = 0
        row_count = len(self.piDeviceList)
        for loop in range(0,row_count):
            Time = float(self.piDeviceList[loop]['Time'])
            #print(Time)
            if(time.time() - Time   > 4):
                #print("timeout")
                self.piDeviceList.pop(loop)
                self.tableWidget_DeviceInfo.removeRow(loop)
                try:
                    for item in self.DownLineCallbackList:
                        pass
                        item("","")
                except:
                    pass
            count += 1
        self.Sem.release()
    def setCallBack(self,OnlineCallback,DownLineCallback):
        self.OnlineCallbackList.append(OnlineCallback)
        self.DownLineCallbackList.append(DownLineCallback)
    def check(self):
        while (True):
            data, addr = self.udpSocket.recvfrom(1024)
            data = data.decode('utf-8')
            jsonobj = json.loads(data)
            print(jsonobj)
            IpList = jsonobj["IpList"]
            # AutoStartLists = jsonobj["AutoStartList"]
            # for item in AutoStartLists:
            #     oneStartItem = list(item.values())
            #     if(oneStartItem not in self.AutoStartList):
            #         self.AutoStartList.append(oneStartItem)
            exitflg = 0
            for item in self.piDeviceList:
                if(jsonobj['SerialCode'] == item['SerialCode']):
                    #该设备已经存在，则只更新时间信息
                    item['Time'] = time.time()
                    exitflg = 1
            if(exitflg == 0):
                #设备不存在，只插入该设备
                DeviceInfo = {}
                DeviceInfo['SerialCode'] = jsonobj['SerialCode']
                DeviceInfo['IpList'] = IpList
                EthIp = ''
                EthMac = ''
                WifiIp = ''
                WifiMac = ''
                try:
                    CamreaStatus = jsonobj['CamreaStu']
                except:
                    CamreaStatus = ''
                Model = jsonobj['Model']

                if(Model == 'Ubuntu'):
                    try:
                        for loop in range(0, 2):
                            if (IpList[loop]['NetName'] == 'ens38'):
                                EthIp = IpList[loop]['Ip']
                                EthMac = IpList[loop]['Mac']
                            if (IpList[loop]['NetName'] == 'wlan0'):
                                WifiIp = IpList[loop]['Ip']
                                WifiMac = IpList[loop]['Mac']
                    except:

                        pass
                else:
                    try:
                        for loop in range(0,2):
                            if(IpList[loop]['NetName'] == 'eth0'):
                                EthIp = IpList[loop]['Ip']
                                EthMac = IpList[loop]['Mac']
                            if (IpList[loop]['NetName'] == 'wlan0'):
                                WifiIp = IpList[loop]['Ip']
                                WifiMac = IpList[loop]['Mac']
                    except:
                        pass
                DeviceInfo['Time'] = time.time()
                self.Sem.acquire()
                self.piDeviceList.append(DeviceInfo)
                self.Sem.release()
                for item in self.OnlineCallbackList:
                    item(EthIp,WifiIp)
                self.InsertDeviceInfo([[jsonobj['SerialCode'],
                                      EthIp,EthMac,
                                      WifiIp,WifiMac,
                                      CamreaStatus]])

    def InsertDeviceInfo(self,data_list):
        current_row_count = self.tableWidget_DeviceInfo.rowCount()
        for row_list in data_list:
            self.tableWidget_DeviceInfo.insertRow(current_row_count)
            for i, data_cell in enumerate(row_list):
                cell = QTableWidgetItem(str(data_cell))
                self.tableWidget_DeviceInfo.setItem(current_row_count, i, cell)
            current_row_count += 1
    def getPiDeviceIp(self):
        if(len(self.piDeviceList) > 0):
            return self.piDeviceList[0]
        return None
    def sendCmd(self,sendmsg):
        sendmsg = str(sendmsg).encode('utf-8')
        for Address in self.BoardCastAddr:
            self.udpSocket.sendto(sendmsg, Address)
    def scan(self):
        sendmsg = "{\"cmd\":\"scan\"}"
        sendmsg = str(sendmsg).encode('utf-8')
        while(True):
            for Address in self.BoardCastAddr:
                self.udpSocket.sendto(sendmsg,Address)
            time.sleep(2)
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    PiDeviceScan = PiDeviceScan()
    PiDeviceScan.show()
    sys.exit(app.exec_())