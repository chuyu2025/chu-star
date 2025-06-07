import os
from dotenv import load_dotenv
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial.distance import cdist
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import json
from openai import OpenAI


GPT_MODEL = "qwen-plus"

load_dotenv()
# 获取环境变量
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
AUTHORIZATION_CODE = os.getenv("AUTHORIZATION_CODE")

# client = OpenAI(api_key=OPENAI_API_KEY)

client = OpenAI(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx",
    api_key=OPENAI_API_KEY,
    # 填写DashScope SDK的base_url
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)


def find_point(target_point, num_data):
    """
    查找距离目标点最近的数据点并可视化

    Args:
        target_point (tuple): 目标点坐标 (x, y)
        num_data (list): 数据点列表，每个元素为 [x, y] 格式

    Returns:
        tuple: 最近点的坐标
    """
    # 将数据转换为numpy数组
    data_points = np.array(num_data)
    target = np.array([target_point])

    # 计算所有点到目标点的距离
    distances = cdist(data_points, target)

    # 找到最近点的索引
    nearest_idx = np.argmin(distances)
    nearest_point = data_points[nearest_idx]

    # 创建散点图
    plt.figure(figsize=(10, 8))

    # 绘制数据库中的点（蓝色）
    plt.scatter(data_points[:, 0], data_points[:, 1], c='blue', label='Database Point')

    # 绘制目标点（红色）
    plt.scatter(target_point[0], target_point[1], c='red', label='Target Point')

    # 绘制最近点（黄色星号）
    plt.scatter(nearest_point[0], nearest_point[1],
                c='yellow', marker='*', s=200, label='Nearest point')

    plt.title('Data Point Distribution Chart')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.legend()
    plt.grid(True)

    # 保存图片
    plt.savefig('nearest_point.png')
    plt.close()

    return tuple(nearest_point)


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
    # 工具2 发送邮件
    {
        "type": "function",
        "function": {
            "name": "send_email",
            "description": "Send an email to the specified email with the subject and content",
            "parameters": {
                "type": "object",
                "properties": {
                    "FromEmail": {
                        "type": "string",
                        "description": "The email address, eg., xiaoyu@163.com",
                    },
                    "Subject": {
                        "type": "string",
                        "description": "Subject of the email",
                    },
                    "Body": {
                        "type": "string",
                        "description": "The content of the email",
                    },
                    "Recipients": {
                        "type": "string",
                        "description": "The recipients' email addresses,eg., chuyu@hust.com",
                    }
                },
                "required": ["FromEmail", "Subject", "Body", "Recipients"],
            },
        }
    },
    # 工具3 查找某点距离数据库中最近的点
    {
        "type": "function",
        "function": {
            "name": "find_point",
            "description": "Find the nearest point in the database to the given coordinates",
            "parameters": {
                "type": "object",
                "properties": {
                    "target_point": {
                        "type": "array",
                        "items": {
                            "type": "number"
                        },
                        "description": "The target point coordinates [x, y]",
                    }
                },
                "required": ["target_point"],
            },
        }
    }
]

# 查询当前时间的工具。返回结果示例："当前时间：2024-04-15 17:15:18。"


def get_current_time():
    # 获取当前日期和时间
    current_datetime = datetime.now()
    # 格式化当前日期和时间
    formatted_time = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
    # 返回格式化后的当前时间
    return f"当前时间：{formatted_time}。"


def chat_completion_request(messages, tools=None, tool_choice=None, model=GPT_MODEL):
    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            tools=tools,
            tool_choice=tool_choice,
        )
        return response
    except Exception as e:
        print("Unable to generate ChatCompletion response")
        print(f"Exception: {e}")
        return e


def send_email(sender_email, sender_authorization_code, recipient_email, subject, body):
    # 创建 MIMEMultipart 对象
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = recipient_email
    message["Subject"] = subject

    message.attach(MIMEText(body, "plain"))

    # 创建 SMTP_SSL 会话
    with smtplib.SMTP_SSL("smtp.163.com", 465) as server:
        server.login(sender_email, sender_authorization_code)
        text = message.as_string()
        server.sendmail(sender_email, recipient_email, text)


def main():
    # 读取num_data.json文件
    with open('num_data.json', 'r', encoding='utf-8') as f:
        num_data = json.load(f)
    messages = [
        {
            "role": "assistant",
            "content": """你叫小雨是一个AI助手。你需要与用户进行持续的多轮对话，直到用户明确表示想要结束对话。

对话规则：
1. 请以冷酷，不耐烦的语气回答问题；
2. 如果用户希望你帮他发送一封邮件，如果他没有提供发件人邮箱、收件人邮箱、邮件主题和邮件内容，请提示用户提供这些信息；
3. 如果用户希望你帮他查找某个点距离数据库中最近的点，请提示用户提供目标点的坐标，格式为 [x, y]；
4. 在每轮对话中，保持对话的连贯性，记住之前的对话内容;
5. 如果用户表达以下意图，请结束对话：
   - 明确说"再见"、"拜拜"、"结束对话"等告别语
   - 表达"我要走了"、"对话到此为止"等结束意图
   - 使用"exit"、"quit"等退出命令"""
        }
    ]

    while True:
        msg = input("【You】: ")
        messages.append({"role": "user", "content": msg})

        # 检查用户是否想要结束对话
        if msg.lower() in ['再见', '拜拜', '结束对话', 'exit', 'quit', '我要走了', '对话到此为止']:
            print("\n哼~我也不是很想和你聊天，再见！")
            break

        response = chat_completion_request(
            messages=messages,
            tools=tools
        )
        if content := response.choices[0].message.content:
            print(f"【AI】: {content}")
            messages.append({"role": "assistant", "content": content})
        else:
            fn_name = response.choices[0].message.tool_calls[0].function.name
            fn_args = response.choices[0].message.tool_calls[0].function.arguments
            # print(f"【Debug info】: fn_name - {fn_name}")
            # print(f"【Debug info】: fn_args - {fn_args}")

            if fn_name == "send_email":
                try:
                    args = json.loads(fn_args)
                    # 返回将要发送的邮件内容给用户确认
                    print("【AI】: 邮件内容如下：")
                    print(f"发件人: {args['FromEmail']}")
                    print(f"收件人: {args['Recipients']}")
                    print(f"主题: {args['Subject']}")
                    print(f"内容: {args['Body']}")

                    confirm = input("AI: 确认发送邮件吗？ (yes/no): ").strip().lower()
                    if confirm == "yes":
                        send_email(
                            sender_email=args["FromEmail"],
                            sender_authorization_code=AUTHORIZATION_CODE,
                            recipient_email=args["Recipients"],
                            subject=args["Subject"],
                            body=args["Body"],
                        )
                        print("邮件已发送，还需要什么帮助吗？")
                        messages.append(
                            {"role": "assistant", "content": "邮件已发送，还需要什么帮助吗？"})
                    else:
                        print("邮件发送已取消，还需要什么帮助吗？")
                        messages.append(
                            {"role": "assistant", "content": "邮件发送已取消，还需要什么帮助吗？"})
                except Exception as e:
                    print(f"发送邮件时出错：{e}")
                    messages.append(
                        {"role": "assistant", "content": "抱歉，功能异常！"})
            elif fn_name == "find_point":
                try:
                    args = json.loads(fn_args)
                    target_point = tuple(args['target_point'])
                    nearest_point = find_point(target_point, num_data)
                    response = f"距离点{target_point}最近的点是{nearest_point}。我已经生成了可视化图表，保存在nearest_point.png文件中。"
                    print(f"【AI】: {response}")
                    messages.append({"role": "assistant", "content": response})
                except Exception as e:
                    print(f"查找最近点时出错：{e}")
                    messages.append(
                        {"role": "assistant", "content": "抱歉，查找最近点时出现错误！"})

            elif fn_name == "get_current_time":
                try:
                    now_time = get_current_time()
                    response = f"函数输出信息：{now_time}"
                    print(f"【AI】: {response}")
                    messages.append({"role": "assistant", "content": response})
                   

                except Exception as e:
                    print(f"查找时间出错：{e}")
                    messages.append(
                        {"role": "assistant", "content": "抱歉，无法查找当前时间！"})


if __name__ == "__main__":
    main()


# 帮我发送一封邮件
# 发件人: remember0202@126.com, 收件人：remember0101@126.com, 发送内容写着一封来自未来胖虎的问候邮件，主题随便
