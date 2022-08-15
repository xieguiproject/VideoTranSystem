import socket
import time

from UdpHelper import UdpHelper #导入UDP库
from TcpHelper import TcpHelper
from ObjectDetect import ObjectDetect#引入检测模块
from FaceCheck import face_detect_demo
import _thread
import cv2 #导入opencv库
import json
import numpy
import struct
import queue

from threading import Semaphore
UdpSocket = UdpHelper('0.0.0.0',5567)
cap = cv2.VideoCapture(0) #打开摄像头

ys = 100
#print(cap.set(cv2.CAP_PROP_FRAME_WIDTH,1920))
#print(cap.set(cv2.CAP_PROP_FRAME_HEIGHT,1080))

CamreaNewImage  = None
CamreaSem = Semaphore(1) #创建信号量
resolution = (1920, 1080)
UdpMaxPkg = 1000
ImageQueue = queue.Queue(5)

def CamreaProcess():
    global CamreaNewImage
    global cap
    global resolution
    global CamreaSem
    global ImageQueue
    while(True):
        CamreaSem.acquire()

        ret, img = cap.read()  # 读取一张图片
        #对改图片调用图像识别物体
        img = ObjectDetect(img)
        #检测人脸
        img = face_detect_demo(img)
        CamreaNewImage = img
        if(not ImageQueue.full()):
            ImageQueue.put(img)
        CamreaSem.release()
        if(ret):
            cv2.imshow("camrea", img)
        # Press 'q' to quit
        if cv2.waitKey(1) == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()
def UdpSendPkg(byte_data,addr):
    global  UdpSocket
    global UdpMaxPkg
    global ImageQueue
    needSendLen = len(byte_data)

    loop = 0
    while(needSendLen > 0):
        if(needSendLen >= UdpMaxPkg):
            content = byte_data[loop * UdpMaxPkg:(loop + 1) * UdpMaxPkg]
            UdpSocket.send(content,addr)
            needSendLen -= UdpMaxPkg
            loop += 1
        else:
            content = byte_data[loop * UdpMaxPkg:]
            UdpSocket.send(content,addr)
            needSendLen = 0
def doUserSendProcess(client,addr):
    global CamreaSem
    global ImageQueue
    global ys
    while(True):
        if (not ImageQueue.empty()):
            CamreaImage = ImageQueue.get()
        else:
            time.sleep(0.001)
        try:
            # print(ys)
            CamreaSem.acquire()
            img_param = [int(cv2.IMWRITE_JPEG_QUALITY), ys]  # 设置传送图像格式、帧数
            CamreaSem.release()
            _, img_encode = cv2.imencode('.jpg', CamreaImage, img_param)  # 按格式生成图片

            img_code = numpy.array(img_encode)  # 转换成矩阵
            img_data = img_code.tobytes()  # 生成相应的字符串
        except:
            img_data = ''
        if (len(img_data) > 0):
            senddata = struct.pack("lhh", len(img_data), resolution[0], resolution[1]) + img_data
        else:
            senddata = struct.pack("lhh", len(img_data), resolution[0], resolution[1])
        try:
            client.send(senddata)
        except:
            break;
def doUserProcess(client,addr):
    global cap
    global resolution
    global ys
    global CamreaSem
    JsonData = ""

    print("用户线程创建成功")
    while (True):
        try:
            data = client.recv(1024)
        except TimeoutError as e:
            # 超时退出，继续接受
            continue
        except ConnectionResetError:
            # 客户端主动断开，直接重新链接
            print("客户端主动断开")
            break
        if (len(data) == 0):
            # 上面你是不超时退出的，如果长度为0则代表链接断开
            break
        data = data.decode('utf-8')
        print(data)
        if(data[-1] != '}'):
            JsonData = data
            continue
        else:
            JsonData = JsonData + data
        JsonData = JsonData.split('}{')
        if (len(JsonData) > 1):
            JsonData = '{' + JsonData[-1]
        else:
            JsonData = JsonData[0]
        print(JsonData)
        jsonobj = json.loads(JsonData)
        JsonData = ''

        if (jsonobj["cmd"] == 'getdata'):
            # 接受到正确的命令，开始发送tcp数据
            GetImageSize = jsonobj["size"]
            GetX,GetY = GetImageSize.split('*')
            GetX = int(GetX)
            GetY = int(GetY)
            ys = int(jsonobj["ys"])

            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            hight = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

            if(width != GetX and hight != GetY):
                print('new size', GetX, GetY, width, hight)
                CamreaSem.acquire()
                resolution = (GetY, GetY)
                cap.set(cv2.CAP_PROP_FRAME_WIDTH,GetX)
                cap.set(cv2.CAP_PROP_FRAME_HEIGHT, GetY)
                CamreaSem.release()

    print("用户线程退出成功")
if __name__ == "__main__":
    _thread.start_new_thread(CamreaProcess,())
    #1、创建tcp服务器

    while(True):
        time.sleep(5)
        print("TCP服务器正在监听")
        server = TcpHelper()
        client,addr = server.CreateTcpServer('0.0.0.0', 5568)
        print("检测到新链接 ip",addr)
        _thread.start_new_thread(doUserProcess,(client,addr))
        _thread.start_new_thread(doUserSendProcess,(client,addr))
    pass