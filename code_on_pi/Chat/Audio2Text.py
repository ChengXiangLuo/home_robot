import pyaudio
import wave
import audioop
import os
from aip import AipSpeech



# 读取文件
def get_file_content(file_path):
    with open(file_path, 'rb') as fp:
        return fp.read()


class _Audio2Text:
    def __init__(self,silence_threshold_strat = 2500 ,silence_threshold_stop = 300,
                 APP_ID='37949396',API_KEY = '7wQ5ft9RSVSNYo28kjoTOIap',SECRET_KEY = 'lypMANN29ym4OowOWifw3g20fL7SF21g') :
        self.silence_threshold_strat = silence_threshold_strat
        self.silence_threshold_stop = silence_threshold_stop    
        self.p = pyaudio.PyAudio()
        self.client = AipSpeech(APP_ID,API_KEY,SECRET_KEY)
        self.stream = self.p.open(format=pyaudio.paInt16,
                channels=1,
                rate=8000,
                input=True,
                frames_per_buffer=256)
        
    def GetAudio(self):
        flag = 0
        frames = []
        count_num = 0 
        rms_list = [self.silence_threshold_stop]*5
        rms_agv = self.silence_threshold_stop+100 
        self.stream.start_stream()
        data = self.stream.read(256)
        # 计算音频数据的能量
        rms = audioop.rms(data, 2)  # 使用2字节采样格式（16位音频）
        # print(rms)
        if rms > self.silence_threshold_strat:
            print("Recording...")
            flag=1
            while rms_agv > self.silence_threshold_stop:
                data = self.stream.read(256)
                rms = audioop.rms(data, 2)

                rms_list[count_num] = rms
                count_num += 1
                if count_num==4:
                    count_num = 0

                rms_agv = sum(rms_list)/5
                frames.append(data)
                # print(rms_agv)
            
        
        if flag == 1:
            print("Finished recording")
            # 保存录制的音频为 WAV 文件
            with wave.open("user_speech.wav", "wb") as wf:
                wf.setnchannels(1)
                wf.setsampwidth(pyaudio.PyAudio().get_sample_size(pyaudio.paInt16))
                wf.setframerate(8000)
                wf.writeframes(b"".join(frames))
            return flag
    
    def get_text(self):
        result = self.client.asr(get_file_content('user_speech.wav'), 'wav', 8000, {
            'dev_pid': 1537, })
        os.remove('user_speech.wav')
        if result.get('result', 'None') == 'None':
            return '忽略这句话'
        else:
            return result['result'][0]
    
    def close_micp(self):
        # 停止音频输入流
        self.stream.stop_stream()
        # self.stream.close()

        # 关闭 PyAudio
        # self.p.terminate()



# 测试
if __name__=="__main__":

    audio2text = _Audio2Text()
    while True:
        flag = audio2text.GetAudio()
        if flag == 1:
            result = audio2text.get_text()
            print(result)
            # audio2text.close_micp()
            # break


    

    










# # 初始化 PyAudio
# p = pyaudio.PyAudio()

# # 打开音频输入流
# stream = p.open(format=pyaudio.paInt16,
#                 channels=1,
#                 rate=44100,
#                 input=True,
#                 frames_per_buffer=1024)

# print("Recording...")

# frames = []
# silence_threshold = 200  # 静音阈值
# rms_list = [100]*10
# count_num=0

# while True:
#     try:
#         data = stream.read(1024)
#         frames.append(data)

#         # 计算音频数据的能量
#         rms = audioop.rms(data, 2)  # 使用2字节采样格式（16位音频）
#         rms_list[count_num % 10] = rms
#         count_num += 1
#         if count_num==11:
#             count_num = 0
#         rms_avge = 0 
#         for i in range(9):
#             rms_avge = rms_list[i]+rms_avge
#         print(rms_avge)
#         if rms_avge < silence_threshold:
#             print("Silence detected. Stopping recording.")
#             break


#     except KeyboardInterrupt:
#         print("Recording interrupted by user.")
#         break

# print("Finished recording")

# # 停止音频输入流
# stream.stop_stream()
# stream.close()

# # 关闭 PyAudio
# p.terminate()

# # 保存录制的音频为 WAV 文件
# with wave.open("output.wav", "wb") as wf:
#     wf.setnchannels(1)
#     wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
#     wf.setframerate(44100)
#     wf.writeframes(b"".join(frames))
