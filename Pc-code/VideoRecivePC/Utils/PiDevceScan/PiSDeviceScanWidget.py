# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'PiSDeviceScanWidget.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_PiDeviceScanWidget(object):
    def setupUi(self, PiDeviceScanWidget):
        PiDeviceScanWidget.setObjectName("PiDeviceScanWidget")
        PiDeviceScanWidget.resize(625, 259)
        self.centralwidget = QtWidgets.QWidget(PiDeviceScanWidget)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tableWidget_DeviceInfo = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget_DeviceInfo.setObjectName("tableWidget_DeviceInfo")
        self.tableWidget_DeviceInfo.setColumnCount(6)
        self.tableWidget_DeviceInfo.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tableWidget_DeviceInfo.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tableWidget_DeviceInfo.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tableWidget_DeviceInfo.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tableWidget_DeviceInfo.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tableWidget_DeviceInfo.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tableWidget_DeviceInfo.setHorizontalHeaderItem(5, item)
        self.verticalLayout.addWidget(self.tableWidget_DeviceInfo)
        PiDeviceScanWidget.setCentralWidget(self.centralwidget)

        self.retranslateUi(PiDeviceScanWidget)
        QtCore.QMetaObject.connectSlotsByName(PiDeviceScanWidget)

    def retranslateUi(self, PiDeviceScanWidget):
        _translate = QtCore.QCoreApplication.translate
        PiDeviceScanWidget.setWindowTitle(_translate("PiDeviceScanWidget", "树莓派自动发现器"))
        item = self.tableWidget_DeviceInfo.horizontalHeaderItem(0)
        item.setText(_translate("PiDeviceScanWidget", "设备ID"))
        item = self.tableWidget_DeviceInfo.horizontalHeaderItem(1)
        item.setText(_translate("PiDeviceScanWidget", "有线网IP"))
        item = self.tableWidget_DeviceInfo.horizontalHeaderItem(2)
        item.setText(_translate("PiDeviceScanWidget", "有线MAC"))
        item = self.tableWidget_DeviceInfo.horizontalHeaderItem(3)
        item.setText(_translate("PiDeviceScanWidget", "无线网IP"))
        item = self.tableWidget_DeviceInfo.horizontalHeaderItem(4)
        item.setText(_translate("PiDeviceScanWidget", "无线MAC"))
        item = self.tableWidget_DeviceInfo.horizontalHeaderItem(5)
        item.setText(_translate("PiDeviceScanWidget", "设备摄像头"))