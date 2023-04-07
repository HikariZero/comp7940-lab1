import openai
import json
import os
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters,CallbackContext, Filters
import configparser
import logging
import redis
import logging
global redis1


# 获取 api
def get_config():
    config_file = 'configs'
    with open(config_file, 'r', encoding='utf-8') as f:
        configs = json.loads(f.read())
    return configs
openai.api_key = get_config()['api']

def start(update, context):
    """发送欢迎消息"""
    message = "你好！我是机器人，有什么问题都可以问我哦~"
    update.message.reply_text(message)
    # 输出调试信息
    logging.debug(f"Sent a welcome message to {update.effective_chat.id}. Message content: {message}")

class ChatGPT:
    def __init__(self, user):
        self.user = user
        self.messages = [{"role": "system", "content": "hello there"}]
        self.filename = "./user_messages.json"

    def ask_gpt(self):
        # q = "用python实现：提示手动输入3个不同的3位数区间，输入结束后计算这3个区间的交集，并输出结果区间"
        rsp = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=self.messages
        )
        return rsp.get("choices")[0]["message"]["content"]
    '''
    def writeTojson(self):
        try:
            # 判断文件是否存在
            if not os.path.exists(self.filename):
                with open(self.filename, "w") as f:
                    # 创建文件
                    pass
            # 读取
            with open(self.filename, 'r', encoding='utf-8') as f:
                content = f.read()
                msgs = json.loads(content) if len(content) > 0 else {}
            # 追加
            msgs.update({self.user: self.messages})
            # 写入
            with open(self.filename, 'w', encoding='utf-8') as f:
                json.dump(msgs, f)
        except Exception as e:
            print(f"错误代码：{e}")
    '''

def main():
    config = configparser.ConfigParser()
    config.read('config.ini')
    updater = Updater(token=(config['TELEGRAM']['ACCESS_TOKEN']), use_context=True)
    dispatcher = updater.dispatcher

    global redis1
    redis1 = redis.Redis(host=(config['REDIS']['HOST']), password=(config['REDIS']['PASSWORD']), port=(config['REDIS']['REDISPORT']))

    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

    echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
    dispatcher.add_handler(echo_handler)

    dispatcher.add_handler(CommandHandler("chat", ChatGPT_command))


    updater.start_polling()
    updater.idle()

def echo(update, context):
    """回显用户的文本消息"""
    text = update.message.text
    update.message.reply_text(text)
    # 输出调试信息
    logging.debug(f"Echoed the message {text} to {update.effective_chat.id}")


def ChatGPT_command(update: Update, context: CallbackContext) -> None:
    """使用ChatGPT API回复消息"""
    user = update.message.chat_id
    chat = ChatGPT(user)

    # 获取命令参数
    message = " ".join(context.args)
    print ('msg:'+message)
    # 将用户输入添加到历史消息中
    chat.messages.append({"role": "user", "content": message})

    # 调用OpenAI的API进行对话生成
    response = chat.ask_gpt()
    print ('res:'+response)

    # 将对话生成的结果添加到历史消息中
    chat.messages.append({"role": "assistant", "content": response})

    # 发送回答
    update.message.reply_text(response)



if __name__ == '__main__':
    main()

