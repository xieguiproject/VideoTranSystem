import cv2

def face_detect_demo(capterimg):
    pass
    global faceSimple
    # 1、检测人脸信息
    gray = cv2.cvtColor(capterimg, cv2.COLOR_BGR2GRAY)
    # 转换为灰度读片,降低颜色通道
    # 加载特征数据
    face_detector = cv2.CascadeClassifier('Cascades/haarcascade_frontalface_default.xml')  # 返回对象
    # 由于检测的原因，检测出来的人脸数和人脸的位置可能存在偏差，需要调整检测器的参数来过滤这些检测错误的人脸信息，或则在后期进行手动过滤
    # 检测人脸
    faces = face_detector.detectMultiScale(gray, 1.1, 5, cv2.CASCADE_SCALE_IMAGE, (100, 100),
                                           (500, 500))  # 开始检测,返回人脸数据的x，y高度和宽度
    if (len(faces) > 0):
        for x, y, w, h in faces:
            cv2.rectangle(capterimg, (x, y), (x + w, y + h), color=(0, 255, 0), thickness=2)  # 在原始图片上讲人脸信息框选出来
    return capterimg