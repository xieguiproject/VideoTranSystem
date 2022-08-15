#该脚本用于扫描树莓派，这样自动扫描树莓派得到树莓派的ip地址
from Utils.PiDevceScan.ToolBox import *
from socket import *
import _thread
import time
import json
import os
import sys
from threading import Semaphore
from Utils.PiDevceScan.SSHClient import  Ui_SSHClientWidget
from PyQt5.QtWidgets import  *
from PyQt5.QtCore import pyqtSlot,pyqtSignal,Qt,QDateTime,QTimer,QEvent
from PyQt5.QtWidgets import QMainWindow
from PyQt5 import QtGui,QtCore,QtWidgets
from PyQt5.QtGui import QPainter, QPalette,QPen,QColor,QTextCursor
import dlib
from threading import Semaphore
import cv2
import _thread
import numpy as np
import time
import os
import paramiko
import queue
from PIL import Image, ImageTk,ImageDraw, ImageFont

class SSHClient(QMainWindow, Ui_SSHClientWidget):
    def __init__(self, parent=None):
        super(SSHClient, self).__init__(parent)
        self.setupUi(self)
        self.parent = parent
        self.ssh = None
        self.run_flg = True
        self.stdin = None
        self.CmdQueue = queue.Queue(100)
        self.stdout = None
        self.stderr = None

        #self.connect()
        _thread.start_new_thread(self.ssh_read_process,())
        self.plainTextEdit.installEventFilter(self)
        self.plainTextEdit.textChanged.connect(self.textChange)
    def textChange(self):
        self.plainTextEdit.moveCursor(QTextCursor.End)
    def eventFilter(self, obj, event):
        if obj == self.plainTextEdit:
            if event.type() == QEvent.KeyPress and (event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return):
                getEditStr = self.plainTextEdit.toPlainText()
                if len(getEditStr) != 0:
                    newcmd = getEditStr.split('\n')[-1]
                    self.runCmd(newcmd)
                return False
            else:
                return False
        else:
            return QWidget.eventFilter(obj, event)
    def runCmd(self,cmd):
        self.CmdQueue.put(cmd)
    def ssh_read_process(self):
        while(self.run_flg):
            #1、插叙队列中是否有命令，如果有则执行
            if(not self.CmdQueue.empty()):
                cmd = self.CmdQueue.get()
                #执行命令
                #print(cmd)
                self.stdin, self.stdout, self.stderr = self.ssh.exec_command(cmd)
            try:
                back = self.stdout.read().decode()
                if(len(back)):
                    self.plainTextEdit.appendPlainText(back)
            except:
                pass
            time.sleep(0.01)

    def connect(self,hostname,user,password):
        # 创建一个ssh的客户端，用来连接服务器
        self.ssh = paramiko.SSHClient()
        # 创建一个ssh的白名单
        know_host = paramiko.AutoAddPolicy()
        # 加载创建的白名单
        self.ssh.set_missing_host_key_policy(know_host)
        # 连接服务器
        self.ssh.connect(
            hostname=hostname,
            port=22,
            username=user,
            password=password)
    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        self.ssh.close()
        self.deleteLater()