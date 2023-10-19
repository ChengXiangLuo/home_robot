import Vision.Connect2Pc as C2PC
import MySerial.Connect2Stm as C2STM
import Chat.Audio2Text as a2text
import Chat.ChatGPT as chatgpt
import Chat.Text2Audio as text2a
import cv2
import threading
import time

time.sleep(2)

page_num_event = threading.Event()
page_num = 0 # 用于表示串口屏此时页面
pcCtl_flag = False

IP = '192.168.137.1'
image_PORT = '5555' # 上传图像端口
order_PORT = '5556' # 接受指令端口

# 初始化摄像头
cap = cv2.VideoCapture(0)  # 使用默认摄像头，如果有多个摄像头，请适当更改索引
cap.set(3, 640)  # 设置帧宽度
cap.set(4, 480)  # 设置帧高度

# 连接电脑对象
connect2pc = C2PC._connect2PC(IP,image_PORT,order_PORT)
# 连接stm32对象
connect2Stm = C2STM._connect2Stm32()
# 语音转换对象
audio2text = a2text._Audio2Text()
# 文本转语音
text2audio = text2a._Text2Audio()
# chat对象
chat = chatgpt._ChatGPT()


# 树梅派主线程
def main_thread():
    global page_num
    while True:
        new_page_num = connect2Stm.stm32Data_processing()
        # print(page_num)
        if new_page_num != page_num:
            page_num = new_page_num
            page_num_event.set()

          

def PcCtl_1_thread():
    global page_num
    while True:
        page_num_event.wait()  # 等待事件被设置
        if page_num == 1:
            # print(1)
            ret, frame = cap.read()  # 读取一帧图像
            if ret:
                connect2pc.imageUpload(frame)   #上传图像
        # connect2pc.PcCommandProcess() 
def PcCtl_2_thread():
    global page_num
    while True:
        page_num_event.wait()  # 等待事件被设置
        if page_num == 1:
            connect2pc.PcCommandProcess() 

def Talk_thread():
    global page_num
    while True:
        page_num_event.wait()  # 等待事件被设置
        if page_num == 2:
            flag = audio2text.GetAudio()
            if flag == 1:
                question = audio2text.get_text()
                print(question)
                answer = chat.continue_ask(question)
                print(answer)
                text2audio.getAudio(answer)
                time.sleep(1)

def Watch_thread():
    global page_num
    while page_num == 3:
        pass

def Doctor_thread():
    global page_num
    while page_num == 4:
        pass


main_thread = threading.Thread(target=main_thread)
PcCtl_1_thread = threading.Thread(target=PcCtl_1_thread)
PcCtl_2_thread = threading.Thread(target=PcCtl_2_thread)
Talk_thread = threading.Thread(target=Talk_thread)
Watch_thread = threading.Thread(target=Watch_thread)
Doctor_thread = threading.Thread(target=Doctor_thread)

main_thread.start()
PcCtl_1_thread.start()
PcCtl_2_thread.start()
Talk_thread.start()
Watch_thread.start()
Doctor_thread.start()

main_thread.join()
PcCtl_1_thread.join()
PcCtl_2_thread.join()
Talk_thread.join()
Watch_thread.join()
Doctor_thread.join()
