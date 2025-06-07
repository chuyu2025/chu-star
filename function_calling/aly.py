import json
from openai import OpenAI
from datetime import datetime
import json
import os
import random

client = OpenAI(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx",
    api_key="sk-ab0e1f8f4b6143aba24ce1d57e166467",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",  # 填写DashScope SDK的base_url
)

# 定义工具列表，模型在选择使用哪个工具时会参考工具的name和description
tools = [
    # 工具1 获取当前时刻的时间
    {
        "type": "function",
        "function": {
            "name": "get_current_time",
            "description": "当你想知道现在的时间时非常有用。",
            # 因为获取当前时间无需输入参数，因此parameters为空字典
            "parameters": {},
        },
    },
    # 工具2 获取指定城市的天气
    {
        "type": "function",
        "function": {
            "name": "get_current_weather",
            "description": "当你想查询指定城市的天气时非常有用。",
            "parameters": {
                "type": "object",
                "properties": {
                    # 查询天气时需要提供位置，因此参数设置为location
                    "location": {
                        "type": "string",
                        "description": "城市或县区，比如北京市、杭州市、余杭区等。",
                    }
                },
                "required": ["location"],
            },
        },
    },
]


# 模拟天气查询工具。返回结果示例："北京今天是雨天。"
def get_current_weather(arguments):
    # 定义备选的天气条件列表
    weather_conditions = ["晴天", "多云", "雨天"]
    # 随机选择一个天气条件
    random_weather = random.choice(weather_conditions)
    # 从 JSON 中提取位置信息
    location = arguments["location"]
    # 返回格式化的天气信息
    return f"{location}今天是{random_weather}。"


# 查询当前时间的工具。返回结果示例："当前时间：2024-04-15 17:15:18。"
def get_current_time():
    # 获取当前日期和时间
    current_datetime = datetime.now()
    # 格式化当前日期和时间
    formatted_time = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
    # 返回格式化后的当前时间
    return f"当前时间：{formatted_time}。"


# 封装模型响应函数
def get_response(messages):
    completion = client.chat.completions.create(
        model="qwen-plus",  # 模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
        messages=messages,
        tools=tools,
    )
    return completion


def call_with_messages():
    # 读取num_data.json文件
    with open('num_data.json', 'r', encoding='utf-8') as f:
        num_data = json.load(f)
        
    print("\n欢迎使用小雨~AI Agent助手！输入'再见'或'exit'可以结束对话。")
    messages = [
        {
            "role": "system",
            "content": """你叫小雨是一个AI Agent助手。你需要与用户进行持续的多轮对话，直到用户明确表示想要结束对话。

对话规则：
1. 如果用户提问关于天气的问题，请调用 'get_current_weather' 函数;
2. 如果用户提问关于时间的问题，请调用 'get_current_time' 函数;
3. 请以友好的语气回答问题;
4. 在每轮对话中，保持对话的连贯性，记住之前的对话内容;
5. 如果用户表达以下意图，请结束对话：
   - 明确说"再见"、"拜拜"、"结束对话"等告别语
   - 表达"我要走了"、"对话到此为止"等结束意图
   - 使用"exit"、"quit"等退出命令

请确保在对话过程中保持礼貌和专业，同时能够自然地进行多轮交互。"""
        }
    ]
    
    while True:
        user_input = input("\n请输入：")
        
        # 检查用户是否想要结束对话
        if user_input.lower() in ['再见', '拜拜', '结束对话', 'exit', 'quit', '我要走了', '对话到此为止']:
            print("\n感谢使用希音千寻-C1助手，再见！")
            break
            
        messages.append({
            "role": "user",
            "content": user_input
        })
        
        print("-" * 60)
        # 模型调用
        i = 1
        first_response = get_response(messages)
        assistant_output = first_response.choices[0].message
        print(f"\n第{i}轮大模型输出信息：{first_response}\n")
        
        if assistant_output.content is None:
            assistant_output.content = ""
            print("呜呜呜呜呜assistant_output无信息")
            
        messages.append(assistant_output)
        
        # 如果不需要调用工具，则直接返回最终答案
        if assistant_output.tool_calls == None:
            print(f"无需调用工具，我可以直接回复：{assistant_output.content}")
            continue
            
        # 如果需要调用工具，则进行模型的多轮调用，直到模型判断无需调用工具
        while assistant_output.tool_calls != None:
            tool_info = {
                "content": "",
                "role": "tool",
                "tool_call_id": assistant_output.tool_calls[0].id,
            }
            
            if assistant_output.tool_calls[0].function.name == "get_current_weather":
                argumens = json.loads(assistant_output.tool_calls[0].function.arguments)
                tool_info["content"] = get_current_weather(argumens)
            elif assistant_output.tool_calls[0].function.name == "get_current_time":
                tool_info["content"] = get_current_time()
                
            tool_output = tool_info["content"]
            print(f"工具输出信息：{tool_output}\n")
            print("-" * 60)
            
            messages.append(tool_info)
            assistant_output = get_response(messages).choices[0].message
            
            if assistant_output.content is None:
                assistant_output.content = ""
                
            messages.append(assistant_output)
            i += 1
            print(f"第{i}轮大模型输出信息：{assistant_output}\n")
            
        print(f"最终答案：{assistant_output.content}\n如果想要结束对话请和我说“再见”")


if __name__ == "__main__":
    call_with_messages()