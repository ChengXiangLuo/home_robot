import serial
import re

def velocity_f2b(num):
    '''
        转换速度格式用于发送给stm32
    '''
    binary = [0]*8
    decimal_value =0

    if num<0:
        binary[7]=1
        num = -num
        
    inter_part = int(num)
    fracitional_part = int((num-inter_part)*10)

    for i in range(4,7):
         binary[i] = inter_part % 2
         inter_part //= 2
    for i in range(4):
         binary[i] = fracitional_part % 2
         fracitional_part //= 2

    for i in range(7,-1,-1):
         decimal_value = decimal_value*2+binary[i]
        
    return decimal_value




class _connect2Stm32:
     def __init__(self):
        self.ser = serial.Serial('/dev/ttyAMA0', 9600)
        self.ser.bytesize = serial.EIGHTBITS  # 设置数据位为8位
        self.ser.parity = serial.PARITY_NONE  # 设置奇偶校验

    
     def send(self,data):
        self.ser.write(data.to_bytes(1,'big'))
    
     def receive(self):
         re_data = self.ser.readline()
         return re_data
    
     def close(self):
         self.ser.close()

    #速度范围：-8～+8,精度：0.1
     def sendMoveCmdDecimal(self,line_x,line_y,ang_z):
         '''
          接受十进制速度并发送stm32
         '''
         binary_x = velocity_f2b(line_x)
         binary_y = velocity_f2b(line_y)
         binary_z = velocity_f2b(ang_z)
         self.ser.write(0x7b.to_bytes(1,'big'))
         self.ser.write(0x01.to_bytes(1,'big'))
         self.ser.write(binary_x.to_bytes(1,'big'))
         self.ser.write(binary_y.to_bytes(1,'big'))
         self.ser.write(binary_z.to_bytes(1,'big'))
         self.ser.write(0x7d.to_bytes(1,'big'))

     def sendArmCmdDecimal(self, ID1, ID2):
         '''
          接受舵机角速度并发送给stm32
         '''
         binary_id1 = velocity_f2b(ID1)
         binary_id2 = velocity_f2b(ID2)
         self.ser.write(0x7b.to_bytes(1,'big'))
         self.ser.write(0x02.to_bytes(1,'big'))
         self.ser.write(binary_id1.to_bytes(1,'big'))
         self.ser.write(binary_id2.to_bytes(1,'big'))
         self.ser.write(0x7d.to_bytes(1,'big'))

     def sendMoveCmdBinary(self,line_x,line_y):
         self.ser.write(0x7b.to_bytes(1,'big'))
         self.ser.write(0x01.to_bytes(1,'big'))
         self.ser.write(line_x)
         self.ser.write(line_y)
         self.ser.write(0x7d.to_bytes(1,'big')) 

     def stm32Data_processing(self):
         '''
          处理32发送的数据
         '''
         data = self.receive()
        #  print(data)
         if data.startswith(b'page'):
               data = data.decode()
               dec = re.findall(r'-?\d+', data)
               page_num = [int(num) for num in dec]  # 得到stm32发来的页面数
            #    print(f'page={page_num[0]}')
               return page_num[0]




         
            

# toCar =_command2Car()
# toCar.sendMoveCmdBinary(0x01.to_bytes(1,'big'),0x91.to_bytes(1,'big'))
# print(toCar.receive())
# toCar.close()


# ser = serial.Serial('/dev/ttyAMA0', 9600)
# ser.bytesize = serial.EIGHTBITS  # 设置数据位为8位
# ser.parity = serial.PARITY_NONE  # 设置奇偶校验

# ser.write(b'Hello Arduino!')

# while True:
#     if(input()=='k'):
#         ser.write(0x7b.to_bytes(1,'big'))
#         ser.write(0x01.to_bytes(1,'big'))
#         ser.write(velocity_f2b(0).to_bytes(1,'big'))
#         ser.write(0x00.to_bytes(1,'big'))
#         ser.write(0x00.to_bytes(1,'big'))
#         ser.write(0x7d.to_bytes(1,'big'))



#     data = ser.readline()
#     print(data)


