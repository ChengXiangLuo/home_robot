# -*- coding: utf-8 -*-
# 语音合成
from aip import AipSpeech
import pygame
import os
#接口文档：https://cloud.baidu.com/product/speech/tts_online

class _Text2Audio:
    def __init__(self,APP_ID='',API_KEY = '',SECRET_KEY = ''):
        self.APP_ID = APP_ID
        self.API_KEY = API_KEY
        self.SECRET_KEY = SECRET_KEY
        self.client = AipSpeech(self.APP_ID, self.API_KEY,self.SECRET_KEY)

    def getAudio(self,text):
        result  = self.client.synthesis(text, 'zh', 1, {
            'vol': 5,'spd':4,'pit':5,'per':1})
        if not isinstance(result, dict):
            with open('robot_speech.mp3', 'wb') as f:
                f.write(result)
        file_path = "robot_speech.mp3"  # 替换为要删除的文件的实际路径
        play_mp3(file_path)
        os.remove(file_path)

def play_mp3(mp3_file):
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load(mp3_file)
    pygame.mixer.music.play()

    # 让音乐播放完毕后脚本不立即退出
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

    pygame.mixer.quit()
    pygame.quit()


# 测试
def main():
    playAudio = _Text2Audio()
    playAudio.getAudio("你好")  
  

if __name__ == '__main__':
    main()


