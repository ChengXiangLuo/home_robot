import MySerial.Connect2Stm as c
import time
mc = c._connect2Stm32()


while True:
    time.sleep(0.5)
    mc.sendArmCmdDecimal(0,5)
