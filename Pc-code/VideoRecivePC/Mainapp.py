# -*- coding:utf-8 -*-
from PyQt5.QtCore import *
from PyQt5.QtWidgets import  *
from PyQt5 import *
from PyQt5.QtGui import *
from PyQt5.QtCore import pyqtSlot,pyqtSignal
from PyQt5.QtWidgets import QMainWindow
from PyQt5 import QtCore,QtGui,QtWidgets
from PyQt5.QtChart import *
from threading import Semaphore
import cv2
import _thread
from MainWindow import Ui_MainWindow
import sys
import numpy as np
import time
import os
from MainWindowControl import MainWindow
from Utils.PiDevceScan.PiDeviceScanCtl import PiDeviceScan
import socket
class WidgetController:
    def __init__(self):
        self.MainWidget = MainWindow()  #登录页面
        self.MainWidget.ScanPiDeviceCallback("xieguimsn.vicp.cc","")
        #self.MainWidget.ScanPiDeviceCallback("192.168.1.10", "")
        #self.MainWidget.ScanPiDeviceCallback("47.97.183.88", "")
    def showMainWindow(self):
        self.MainWidget.show()
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    Widgetcontroller =  WidgetController()
    Widgetcontroller.showMainWindow() #先显示登录页面
    sys.exit(app.exec_())
