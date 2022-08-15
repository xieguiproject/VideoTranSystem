from PyQt5.QtWidgets import  *
from PyQt5.QtCore import pyqtSlot,pyqtSignal,Qt,QDateTime,QTimer,QSize
from PyQt5.QtWidgets import QMainWindow
from PyQt5 import QtGui
from PyQt5.QtGui import QPainter, QPalette,QPen,QColor
import dlib
from threading import Semaphore
import cv2
import _thread
from  MainWindow import Ui_MainWindow
import numpy as np
import time
import os
import sys
from PIL import Image, ImageTk,ImageDraw, ImageFont
from PyQt5.QtChart import QChart,QSplineSeries,QChartView, QPieSeries, QPieSlice,QDateTimeAxis,QValueAxis
from UdpHelper import UdpHelper
from TcpHelper import TcpHelper
import queue
import random
import socket
import json
debugflg = 1
import struct
import numpy
class MainWindow(QMainWindow, Ui_MainWindow):
    """
    槽函数
    """
    def __init__(self, parent=None):
        """
        Constructor

        @param parent reference to the parent widget
        @type QWidget
        """
        #self.parent().show()
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.PiDeviceIp = ''
        self.CurrentSize = '640*480'
        self.ys = 50
        self.CamreaSem = Semaphore(1)  # 创建信号量
        self.udpSocket = UdpHelper('0.0.0.0',5566) #创建一个udp，
        self.tcpSocket = TcpHelper()#创建一个TCPsocket
        self.sem = Semaphore(1)
        self.NewImage = None
        self.setWindowTitle('实时图传')
        _thread.start_new_thread(self.ImageReciveProcess,()) #创建一个图片接受处理线程
        self.horizontalSlider_5.valueChanged.connect(self.updateYS)
        self.horizontalSlider_5.setValue(50)
        self.window().resize(QSize(int(self.CurrentSize.split("*")[0] ) * 1.5, int(self.CurrentSize.split("*")[1]) * 1.2))
    def updateYS(self,value):
        self.ys = value + 1
        self.CamreaSem.acquire()
        self.sendGetImagCmd(self.CurrentSize)
        self.CamreaSem.release()
    def ImageReciveProcess(self):
        DataBuf = bytes()
        datalen = 0
        while(True):
            #1、检查树莓派的地址是否设置成功,地址为空则不进行数据收发工作
            if(self.PiDeviceIp == ''):
                time.sleep(0.1)
                continue
            try:
                print("即将链接视频服务器")
                self.tcpSocket.connectToServer(self.PiDeviceIp, 43102
                                              , -1)

                #self.tcpSocket.connectToServer(self.PiDeviceIp, 35193, -1)
                #print("视频服务器", (self.PiDeviceIp, 35193), '链接成功')
            except:
                #链接失败，等待重试
                time.sleep(1)
                continue
                self.CamreaSem.acquire()
                self.sendGetImagCmd(self.CurrentSize)
                self.CamreaSem.release()
            while(True):

                try:
                    data = self.tcpSocket.recv(8,-1)#接受8个字节的头部信息，包含图像的长度和宽度，以及数据包的大小
                except ConnectionResetError:
                    #链接被重置，直接重新链接
                    break
                if(len(data) == 0):
                    break
                #print(len(data))
                datalen += len(data)
                #print(len(data),type(data))
                DataBuf = DataBuf + data
                if(datalen != 8):
                    continue
                info = struct.unpack("lhh", DataBuf[0:8]) #解析控制命令
                DataBuf = bytes()
                datalen = 0
                needRecvLen = info[0] #数据包的长度
                buf = b""  # 代表bytes类型
                if (needRecvLen):
                    while(needRecvLen > 0):
                            try:
                                temp_buf = self.tcpSocket.recv(needRecvLen,-1)
                            except ConnectionResetError:
                                break
                            if(len(temp_buf) == 0):
                                break
                            needRecvLen -= len(temp_buf)
                            buf += temp_buf
                    if(needRecvLen == 0):
                        data = numpy.fromstring(buf, dtype='uint8')  # 按uint8转换为图像矩阵
                        image = cv2.imdecode(data, 1)  # 图像解码
                        self.sem.acquire()
                        self.NewImage = image
                        self.sem.release()
                        self.showImage(image)
                    else:
                        #未长成接受完成，可能是服务器断开了，需要重新链接
                        print("服务器断开，即将重连")
                        break
                pass
    def DownLineDeviceCallback(self,EthIp,WifiIp):
        pass
    def ScanPiDeviceCallback(self,EthIp,WifiIp):
        print("树莓派地址查询成功",EthIp,WifiIp)
        if(EthIp != ''):
            self.PiDeviceIp = EthIp
        elif(WifiIp != ''):
            self.PiDeviceIp = WifiIp
        self.lineEdit.setText(self.PiDeviceIp)
    def paint_chinese_opencv(self,im, chinese, position, fontsize, color):  # opencv输出中文
        img_PIL = Image.fromarray(cv2.cvtColor(im, cv2.COLOR_BGR2RGB))  # 图像从OpenCV格式转换成PIL格式
        font = ImageFont.truetype('simhei.ttf', fontsize, encoding="utf-8")
        # color = (255,0,0) # 字体颜色
        # position = (100,100)# 文字输出位置
        draw = ImageDraw.Draw(img_PIL)
        draw.text(position, chinese, font=font, fill=color)  # PIL图片上打印汉字 # 参数1：打印坐标，参数2：文本，参数3：字体颜色，参数4：字体
        img = cv2.cvtColor(np.asarray(img_PIL), cv2.COLOR_RGB2BGR)  # PIL图片转cv2 图片
        return img

    #在lab中显示一个图片
    def showImage(self,image):
        #print(image.shape[1])
        #image = cv2.resize(image, (640, 480))  # 把读到的帧的大小重新设置为 640x480

        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # 视频色彩转换回RGB，这样才是现实的颜色
        showImage = QtGui.QImage(image.data, image.shape[1], image.shape[0],
                                 QtGui.QImage.Format_RGB888)  # 把读取到的视频数据变成QImage形式
        self.label_CamreaShow.setPixmap(QtGui.QPixmap.fromImage(showImage))  # 往显示视频的Label里 显示QImage

    def sendGetImagCmd(self,size):
        # 发送命令让树莓派给界面传输一张图片

        sendmsg = "{\"cmd\":\"getdata\",\"size\":\"" + size + '\",\"ys\":\"' + str(self.ys) + '\"}'
        #print(sendmsg)
        sendmsg = str(sendmsg).encode('utf-8')


        if (self.PiDeviceIp != ''):
            try:
                self.tcpSocket.send(sendmsg)
            except:
                # 发送失败，服务器可能退出了
                print('数据发送失败，服务器可能退出')