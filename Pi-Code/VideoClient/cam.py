import cv2
import time
import _thread
import threading
maxCamrea = 1

width = 640
height = 480


camreaSem = threading.Semaphore(1)


def takeCamreaProcess(loop):
    global  width
    global  height
    canDevice =  cv2.VideoCapture(loop)
    canDevice.set(cv2.CAP_PROP_FRAME_WIDTH, width)  # 设置图像宽度
    canDevice.set(cv2.CAP_PROP_FRAME_HEIGHT, height)  # 设置图像高
    canDevice.set(cv2.CAP_PROP_FPS,30)
    starttick = 0
    while(True):
        ret, frame = canDevice.read()  # 读取图像(frame就是读取的视频帧，对frame处理就是对整个视频的处理)
        if(ret):
            fps = 1 / (time.time() - starttick)
            starttick = time.time()
            img = cv2.putText(frame, 'fps:' + str(int(fps)), (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2.0, (255, 0, 0), 5,
                              cv2.LINE_AA,
                              False)
            cv2.imshow("frame" + str(loop), frame)
            cv2.imwrite('cam_' + str(loop) + '.png', frame, [cv2.IMWRITE_PNG_COMPRESSION, 0])
        cv2.waitKey(10)
    canDevice.release()  # 释放摄像头
if __name__ == '__main__':
    for loop in range(maxCamrea):
        _thread.start_new_thread(takeCamreaProcess,(loop,))
    while(1):
        time.sleep(1)
    cv2.destroyAllWindows()  # 销毁窗口
    pass