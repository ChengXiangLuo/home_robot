import cv2
import zmq
import base64
import re
import MySerial.Connect2Stm as myse

C2Car = myse._connect2Stm32()

class _connect2PC:
    def __init__(self,IP,TX2PC_PORT,RX2PC_PORT):
        self.context = zmq.Context()
        # zmq 对象使用TCP通讯协议
        self.send_socket = self.context.socket(zmq.PUSH)
        self.rece_socket = self.context.socket(zmq.PULL)
        # zmq 对象和视频接收端建立TCP通讯协议
        self.send_socket.connect(f'tcp://{IP}:{TX2PC_PORT}')
        self.rece_socket.connect(f'tcp://{IP}:{RX2PC_PORT}')

    def imageUpload(self,frame):
        _, buffer = cv2.imencode('.jpg', frame)  # 把图像数据转换为JPEG格式并编码
        jpg_as_text = base64.b64encode(buffer)  # 把编码后的图像数据转换为base64编码
        # 发送图像数据给视频接收端
        self.send_socket.send(jpg_as_text)
    

    def PcCommandProcess(self):
        '''
            处理PC发送的指令
        '''
        data = self.rece_socket.recv_string()
        print(data)
        # 针对car的指令 car:Vx,Vy
        if data.startswith('car'):
            dec = re.findall(r'-?\d+', data)
            nums = [float(num) for num in dec]  # 得到Pc发来的速度
            C2Car.sendMoveCmdDecimal(nums[0],nums[1],nums[2])   # 串口发送指令
            #for i in nums:
            #    print(i)
            # C2Car.receive()
        elif data.startswith('arm'):
            dec = re.findall(r'-?\d+', data)
            nums = [float(num) for num in dec]  # 得到Pc发来的速度
            C2Car.sendArmCmdDecimal(nums[0],nums[1])   # 串口发送指令
            #for i in nums:
             #   print(i)
        
            
    
    
     






# IP = '192.168.137.1'  # 视频接收端的IP地址

# # 初始化摄像头
# cap = cv2.VideoCapture(0)  # 使用默认摄像头，如果有多个摄像头，请适当更改索引
# cap.set(3, 640)  # 设置帧宽度
# cap.set(4, 480)  # 设置帧高度

# # 实例化用来发送帧的 zmq 对象
# context = zmq.Context()
# # zmq 对象使用TCP通讯协议
# footage_socket = context.socket(zmq.PAIR)
# # zmq 对象和视频接收端建立TCP通讯协议
# footage_socket.connect('tcp://%s:5555' % IP)
# print(IP)

# while True:
#     ret, frame = cap.read()  # 读取一帧图像
#     encoded, buffer = cv2.imencode('.jpg', frame)  # 把图像数据转换为JPEG格式并编码
#     jpg_as_text = base64.b64encode(buffer)  # 把编码后的图像数据转换为base64编码

#     # 发送图像数据给视频接收端
#     footage_socket.send(jpg_as_text)

#     cv2.imshow("Video Stream", frame)  # 显示图像

#     # 按 'q' 键退出循环
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# cap.release()  # 释放摄像头
# cv2.destroyAllWindows()  # 关闭窗口
