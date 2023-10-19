# 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
import openai
import os


class _ChatGPT:
    def __init__(self):
        self.user = "user"
        self.messages = [{"role": "system", "content": "一个叫做Mark的语音助手,语言简单易懂口语化,每次说话不超过5句"}]

    # 调用chatgpt的API
    def ask_gpt(self):
        openai.api_key = ""
        openai.api_base = "https://api.chatanywhere.com.cn/v1"
        rsp = openai.ChatCompletion.create(
          model="gpt-3.5-turbo",
          messages=self.messages
        )
        return rsp.get("choices")[0]["message"]["content"]
    
    # 连续提问，返回答案
    def continue_ask(self,question):
        self.messages.append({"role": "user", "content": question})
        answer = self.ask_gpt()
        self.messages.append({"role": "assistant", "content": answer})
        return answer



# 测试
def main():
    chat = _ChatGPT() 
    # 循环
    while 1:
        # 提问-回答-记录
        question=input()
        if question=='q':
            break
        answer = chat.continue_ask(question)
        print(answer)

if __name__ == '__main__':
    main()
