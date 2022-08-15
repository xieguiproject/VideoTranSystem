#该脚本用于扫描树莓派，这样自动扫描树莓派得到树莓派的ip地址

from Utils.PiDevceScan.ToolBox import *
from socket import *
import _thread
import time
import json
import os
import sys
from threading import Semaphore
from Utils.PiDevceScan.StartUpItem import  Ui_StartUpItem
from Utils.PiDevceScan.StartUpItemCfgCtl import StartUpItemCfg
from PyQt5.QtWidgets import  *
from PyQt5.QtCore import pyqtSlot,pyqtSignal,Qt,QDateTime,QTimer
from PyQt5.QtWidgets import QMainWindow
from PyQt5 import QtGui
from PyQt5.QtGui import QPainter, QPalette,QPen,QColor
import dlib
from threading import Semaphore
import cv2
import _thread
import numpy as np
import time
import os
from PIL import Image, ImageTk,ImageDraw, ImageFont

class StartUpItem(QMainWindow, Ui_StartUpItem):
    def __init__(self, parent=None):
        super(StartUpItem, self).__init__(parent)
        self.setupUi(self)
        self.parent = parent
        self.InitTableWidget()
    def InitTableWidget(self):
        self.tableWidget_StartupItem.setColumnWidth(0,100)
        self.tableWidget_StartupItem.setColumnWidth(1, 400)
        self.tableWidget_StartupItem.setContextMenuPolicy(Qt.CustomContextMenu)  # 允许生成右击菜单
        self.tableWidget_StartupItem.customContextMenuRequested.connect(self.tableMenu)
    def tableMenu(self,pos):
        menu = QMenu()  # 实例化菜单
        StartupItem = menu.addAction(u"增加启动项")
        DeleteItem = menu.addAction(u"删除启动项")

        action = menu.exec_(self.tableWidget_StartupItem.mapToGlobal(pos))
        if(action == StartupItem):
            self.StartUpItemCfgs = StartUpItemCfg(self)
            self.StartUpItemCfgs.show()
    def addStartupItemRecd(self,data_list,flg):
        if(flg):
            #该配置为新增，先将配置信息发送到下位机
            sendmsg = "{\"cmd\":\"addstartitem\"}"
            self.parent.sendCmd(sendmsg)
        current_row_count = self.tableWidget_StartupItem.rowCount()
        for row_list in data_list:
            self.tableWidget_StartupItem.insertRow(current_row_count)
            for i ,data_cell in enumerate(row_list):
                cell = QTableWidgetItem(str(data_cell))
                self.tableWidget_StartupItem.setItem(current_row_count, i, cell)
            current_row_count += 1
    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        self.deleteLater()