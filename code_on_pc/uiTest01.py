# -*- coding: utf-8 -*-
import sys
import cv2
from PyQt5.QtWidgets import QApplication, QMainWindow, QGraphicsScene
from PyQt5.uic import loadUi
from PyQt5.QtGui import QImage, QPixmap, QPainter
from PyQt5.QtCore import Qt, QTimer
import numpy as np
import threading
import time,zmq
import Connect2Pi

IP = '192.168.137.1' # 默认本地IP,与树莓派发送IP相同
re_port = '5555'    # 接收端口
se_port = '5556'    # 发送端口

line_x = 2  # 前后移动速度，1m/s
line_y = 3  # 左右移动速度，1m/s
ang_z = 3   # 选择速度 ，1m/s
Ang_Arm= 2  # 舵机旋转速度


steering_num = 0 # 用于选择控制哪个舵机 0底部 1顶部
transmit_status = False
imgFrame = 0
imgRet = False

re_img = Connect2Pi._RecvImg(IP,re_port)
se_cmd = Connect2Pi._SendCmd(IP,se_port)
connected_status = False    # 用于判断树莓派连接情况

class CameraViewerWindow(QMainWindow):
    def __init__(self):
        super(CameraViewerWindow, self).__init__()
        loadUi("E:\\vscode _ws\\home_robot\\code_on_pc\\uiTest01.ui", self)   
        
        # 添加以下三行代码以添加新的场景        
        self.scene = QGraphicsScene(self)  # 创建场景对象
        self.graphicsView.setScene(self.scene)
        self.graphicsView.setRenderHint(QPainter.Antialiasing)
        
        # self.capture = cv2.VideoCapture(0)

        # 定时刷新
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)    # 更新频率为30hz

        # 初始化定义
        self.chosen_steering.setText('舵机选择:底部')
        self.w_pressed = False
        self.a_pressed = False
        self.s_pressed = False
        self.d_pressed = False
        self.i_pressed = False
        self.j_pressed = False
        self.k_pressed = False
        self.l_pressed = False

        # 多线程
        self.exit_flag = False  # 添加一个标志来控制线程的结束
        self.transmit_status_thread = threading.Thread(target=self.transmit_status)
        self.transmit_status_thread.start()

    def keyReleaseEvent(self, event):
        if event.key() == Qt.Key_W:
            self.w_pressed = False
        elif event.key() == Qt.Key_S:
            # S 后退
            self.s_pressed = False
        elif event.key() == Qt.Key_A:
            # A 左转
            self.a_pressed = False
        elif event.key() == Qt.Key_D:
            # D 右转
            self.d_pressed = False
        elif event.key() == Qt.Key_J:
            # J 左进
            self.j_pressed = False
        elif event.key() == Qt.Key_L:
            # L 右进
            self.l_pressed = False
        elif event.key() == Qt.Key_I:
            # I 舵机上升
            self.i_pressed = False
        elif event.key() == Qt.Key_K:
            # K 舵机下降
            self.k_pressed = False

    def keyPressEvent(self, event):
        """_summary_
            按键监听进程
        Args:
            event (_type_): _description_
        """ 
        global steering_num           
        if event.key() == Qt.Key_Q:
            # Q:清空所有窗口，关闭程序
            # self.capture.release()
            cv2.destroyAllWindows()
            self.exit_flag = True
            self.close()
        elif event.key() == Qt.Key_Shift:
            # shift:切换舵机
            if steering_num == 0:
                steering_num +=1
                self.chosen_steering.setText('舵机选择:顶部')
            else:
                steering_num -=1
                self.chosen_steering.setText('舵机选择:底部')
        elif event.key() == Qt.Key_W:
            # w 前进
            self.w_pressed = True
        elif event.key() == Qt.Key_S:
            # S 后退
            self.s_pressed = True
        elif event.key() == Qt.Key_A:
            # A 左转
            self.a_pressed = True
        elif event.key() == Qt.Key_D:
            # D 右转
            self.d_pressed = True
        elif event.key() == Qt.Key_J:
            # J 左进
            self.j_pressed = True
        elif event.key() == Qt.Key_L:
            # L 右进
            self.l_pressed = True
        elif event.key() == Qt.Key_I:
            # I 舵机上升
            self.i_pressed = True
        elif event.key() == Qt.Key_K:
            # K 舵机下降
            self.k_pressed = True
            

    def transmit_status(self):
        """_summary_
            监测与树莓派的连接
        """        
        global transmit_status, imgRet,imgFrame
        while not self.exit_flag:
            transmit_status = se_cmd.check_connection()
            imgRet, imgFrame = re_img.imgProcessing() # 接收图像

            if self.w_pressed:
                # print('w')
                se_cmd.velocitySet(line_x, 0, 0)
            elif self.s_pressed:
                se_cmd.velocitySet(-line_x, 0, 0)
            elif self.j_pressed:
                se_cmd.velocitySet(0, line_y, 0)
            elif self.l_pressed:
                se_cmd.velocitySet(0, -line_y, 0)
            elif self.a_pressed:
                se_cmd.velocitySet(0, 0, ang_z)
            elif self.d_pressed:
                se_cmd.velocitySet(0, 0, -ang_z)
            elif self.i_pressed:
                if steering_num == 0:
                    se_cmd.armCamContral(-Ang_Arm, 0)
                else:
                    se_cmd.armCamContral(0, -Ang_Arm)
            elif self.k_pressed:
                if steering_num == 0:
                    se_cmd.armCamContral(Ang_Arm, 0)
                else:
                    se_cmd.armCamContral(0, Ang_Arm)
            else:
                se_cmd.velocitySet(0, 0, 0)
                se_cmd.armCamContral(0, 0)

    def update_frame(self):
        """_summary_
            QT窗口更新函数
        """
        global steering_num, transmit_status, imgRet, imgFrame, line_x, line_y, ang_z
        if transmit_status:
            self.status.setText('已连接树莓派')
            if imgRet:
                rgb_image = cv2.cvtColor(imgFrame, cv2.COLOR_BGR2RGB)
                height, width, channel = rgb_image.shape
                bytesPerLine = 3 * width
                qImg = QImage(rgb_image.data, width, height, bytesPerLine, QImage.Format_RGB888)
                pixmap = QPixmap.fromImage(qImg)
                self.scene.clear()  # 清空场景中的内容
                self.scene.addPixmap(pixmap)  # 添加像素图到场景中
                self.graphicsView.fitInView(self.scene.sceneRect(), Qt.AspectRatioMode.KeepAspectRatio)     
        else:
            self.status.setText('未连接树莓派')

        
            

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CameraViewerWindow()
    window.show()
    sys.exit(app.exec_())
