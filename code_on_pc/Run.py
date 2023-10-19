# -*- coding: utf-8 -*-
import Connect2Pi
import threading
import keyboard
import time
import sys
import cv2
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QTimer, QThread, Qt, QEvent

IP = ''
re_port = '5555'
se_port = '5556'

global Vx
global Vy
global Angz
global AngArm
Vx = 0
Vy = 0
Angz = 0
AngArm=0

global arm_num # 用于选择控制哪个舵机 
arm_num = True
global img

re_img = Connect2Pi._RecvImg(IP,re_port)
se_cmd = Connect2Pi._SendCmd(IP,se_port)

exit_event = threading.Event()

def sendNumLimit():
    global Vx, Vy, Angz, AngArm
    if Vx > 5:
        Vx = 0
    elif Vy > 5:
        Vy = 0
    elif Angz > 90:
        Angz = 0
    elif AngArm > 90:
        AngArm = 0



class VideoViewer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.label = QLabel(self)
        self.label.setGeometry(10, 10, 640, 480)
        self.label_vx = QLabel(self)
        self.label_vx.setGeometry(660, 10, 200, 30)
        self.label_vy = QLabel(self)
        self.label_vy.setGeometry(660, 50, 200, 30)
        self.label_angz = QLabel(self)
        self.label_angz.setGeometry(660, 90, 200, 30)
        self.label_angarm = QLabel(self)
        self.label_angarm.setGeometry(660, 130, 200, 30)
        self.label_armNum = QLabel(self)
        self.label_armNum.setGeometry(660, 170, 200, 30)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(1)
    

    def update_frame(self):
        global Vx, Vy, Angz, AngArm
        # temp = re_img.check_connection()
        # if temp:
        #     print('re is ok')
        # temp2 = se_cmd.check_connection()
        # if temp2:
        #     print('se is ok')


        ret, frame = re_img.imgProcessing()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            height, width, channel = frame.shape
            bytes_per_line = 3 * width
            q_image = QImage(frame.data, width, height, bytes_per_line, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(q_image)
            self.label.setPixmap(pixmap)
            self.label.setScaledContents(True)
            self.label_vx.setText(f'前后速度: {Vx}')
            self.label_vy.setText(f'左右速度: {Vy}')
            self.label_angz.setText(f'底盘旋转速度: {Angz}')
            self.label_angarm.setText(f'舵机旋转速度:{AngArm}')
            self.label_armNum.setText(f'舵机控制：{arm_num}')



class VideoViewerThread(QThread):
    def run(self):
        app = QApplication([])
        viewer = VideoViewer()
        viewer.show()
        sys.exit(app.exec_())


def key_listener():
    global Vx, Vy, Angz, arm_num, AngArm
    while not exit_event.is_set():
        sendNumLimit()        
        if keyboard.is_pressed('q'):
            exit_event.set()
            break
        elif keyboard.is_pressed('w'):
            se_cmd.velocitySet(Vx, 0, 0)
            time.sleep(0.3)
        elif keyboard.is_pressed('a'):
            se_cmd.velocitySet(0, Vy, 0)
            time.sleep(0.3)
        elif keyboard.is_pressed('s'):
            se_cmd.velocitySet(Vx*(-1), 0, 0)
            time.sleep(0.3)
        elif keyboard.is_pressed('d'):
            se_cmd.velocitySet(0, Vy*(-1), 0)
            time.sleep(0.3)
        elif keyboard.is_pressed('left'):
            se_cmd.velocitySet(0, 0, Angz)
            time.sleep(0.3)
        elif keyboard.is_pressed('right'):
            se_cmd.velocitySet(0, 0, Angz*(-1))
            time.sleep(0.3)
        elif keyboard.is_pressed('up'):
            if not arm_num:
                se_cmd.armCamContral(AngArm, 0)
            else:
                se_cmd.armCamContral(0, AngArm)
            time.sleep(0.3)
        elif keyboard.is_pressed('down'):
            if not arm_num:
                se_cmd.armCamContral(-1*AngArm, 0)
            else:
                se_cmd.armCamContral(0, -1*AngArm)
            time.sleep(0.3)
        elif keyboard.is_pressed('right shift'):
            arm_num = not arm_num
            time.sleep(0.5)
        elif keyboard.is_pressed('c'):
            Vx = Vx + 1
            Vy = Vy + 1
            Angz = Angz + 18
            AngArm = AngArm + 18
            time.sleep(0.3)




if __name__ == '__main__':
    viewer_thread = VideoViewerThread()
    keylistener_thread = threading.Thread(target=key_listener)


    keylistener_thread.start()
    viewer_thread.start()

    keylistener_thread.join()
