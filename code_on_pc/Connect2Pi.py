import cv2
import zmq
import base64
import numpy as np

class _RecvImg:
    def __init__(self,IP,port):
        """设置接收图像的IP和端口

        Args:
            IP (字符串):IP地址 
            port (字符串): IP端口
        """
        self.IP = IP
        self.port = port
        if IP == '':
            bind_str = 'tcp://*:' + str(port)
        elif IP != '':
            bind_str = 'tcp://' + str(IP) +':'+ str(port) 
        self.context = zmq.Context()        
        self.recv_socket = self.context.socket(zmq.PULL)
        self.recv_socket.bind(bind_str)  # 绑定到所有本地接口
        
    def imgProcessing(self):
        """收到树莓派发来的视频流后，解码恢复

        Returns:
            bool: 接收到为TRUE,否则为Flase
            frame: 接收的图像,可用cv2.imshow显示
        """
        frame = self.recv_socket.recv_string() #接收TCP传输过来的一帧视频图像数据
        if frame is not None:
            img = base64.b64decode(frame) #把数据进行base64解码后储存到内存img变量中
            npimg = np.frombuffer(img, dtype=np.uint8) #把这段缓存解码成一维数组
            source = cv2.imdecode(npimg, 1) #将一维数组解码为图像source
            return True, source
        else:
            return False

class _SendCmd():
    def __init__(self,IP,port):
        """设置发送指令的IP和端口

        Args:
            IP (字符串):IP地址 
            port (字符串): IP端口
        """
        self.IP = IP
        self.port = port
        if IP == '':
            bind_str = 'tcp://*:' + str(port)
        elif IP != '':
            bind_str = 'tcp://' + str(IP) +':'+ str(port) 
        self.context = zmq.Context()
        self.send_socket = self.context.socket(zmq.PUSH)
        self.send_socket.bind(bind_str)

       
    def velocitySet(self,velocity_x,velocity_y,angle_z):
        """速度设置
        """
        if velocity_x>5 or velocity_x<-5:
            velocity_x = 0
        if velocity_y>5 or velocity_y<-5:
            velocity_y = 0
        if angle_z>90 or angle_z<-90:
            angle_z = 0
        send_str = 'car:'+str(velocity_x)+','+str(velocity_y)+','+str(angle_z)
        self.send_socket.send_string(send_str)
        

    def armCamContral(self, ID1, ID2):
        """舵机旋转速度控制

        Args:
            ID1 (数值): 第一个舵机旋转速度，范围-90至90
            ID2 (数值): 第二个舵机旋转速度，范围-90至90
        """
        if ID1 > 90 or ID1 < -90:
            ID1 = 10
        elif ID2 > 90 or ID2< -90:
            ID2 = 10
        send_str = 'arm:'+str(ID1)+','+str(ID2)
        self.send_socket.send_string(send_str)

    def lightValueSet(self,value):
        if(value>100 or value<0):
            value = 50
            print('value is out of range')
        send_str = 'cam_light:' + str(value) 
        self.send_socket.send_string(send_str)
    
