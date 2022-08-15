#该脚本用于扫描树莓派，这样自动扫描树莓派得到树莓派的ip地址
from Utils.PiDevceScan.ToolBox import *
from socket import *
import _thread
import time
import json
import os
import sys
from threading import Semaphore
from Utils.PiDevceScan.StartupItemCfg import  Ui_StartupItemCfg
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
from PyQt5.QtChart import QChart,QSplineSeries,QChartView, QPieSeries, QPieSlice,QDateTimeAxis,QValueAxis

class StartUpItemCfg(QMainWindow, Ui_StartupItemCfg):
    def __init__(self, parent=None):
        super(StartUpItemCfg, self).__init__(parent)
        self.setupUi(self)
        self.parent = parent
    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        self.deleteLater()
    @pyqtSlot()
    def on_pushButton_2_clicked(self):
        self.close()
        self.deleteLater()
    @pyqtSlot()
    def on_pushButton_clicked(self):
        #self.parent
        self.parent.addStartupItemRecd([["sudo python3 main.py","2","4"]],1)
        self.close()
        self.deleteLater()