import openai
import json
import os
#from processing_data import get_config

#os.environ["HTTP_PROXY"] = "http://127.0.0.1:7890"
#os.environ["HTTPS_PROXY"] = "http://172.27.112.1:7296" #本地服务器的代理地址
'''
config_file = 'configs'
with open(config_file, 'r', encoding='utf-8') as f:
        openai.api_key = json.loads(f.read())

#openai.api_key = get_config()['api']
'''
def get_config():
    config_file = 'configs'
    with open(config_file, 'r', encoding='utf-8') as f:
        configs = json.loads(f.read())
    return configs
# 获取 api
openai.api_key = get_config()['api']

# 将当前用户所有历史消息+最新提问发送给 gpt-3.5-turbo ，并返回响应结果
def ask_gpt(messages):
    # q = "用python实现：提示手动输入3个不同的3位数区间，输入结束后计算这3个区间的交集，并输出结果区间"
    rsp = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    return rsp.get("choices")[0]["message"]["content"]