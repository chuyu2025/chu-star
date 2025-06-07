import os
from dotenv import load_dotenv
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial.distance import cdist
from flask import Flask, render_template, request, jsonify
import base64
from io import BytesIO
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import json
from openai import OpenAI

app = Flask(__name__)

GPT_MODEL = "qwen-plus"

load_dotenv('.env')
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

# 全局变量存储对话历史
conversation_history = [
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


def find_point(target_point, num_data):
    """
    查找距离目标点最近的数据点并可视化

    Args:
        target_point (tuple): 目标点坐标 (x, y)
        num_data (list): 数据点列表，每个元素为 [x, y] 格式

    Returns:
        tuple: 最近点的坐标和图片的base64编码
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
    plt.scatter(data_points[:, 0], data_points[:, 1],
                c='blue', label='Database Point')

    # 绘制目标点（红色）
    plt.scatter(target_point[0], target_point[1],
                c='red', label='Target Point')

    # 绘制最近点（黄色星号）
    plt.scatter(nearest_point[0], nearest_point[1],
                c='yellow', marker='*', s=200, label='Nearest point')

    plt.title('Data Point Distribution Chart')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.legend()
    plt.grid(True)

    # 将图片转换为base64
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    plt.close()

    return tuple(nearest_point), image_base64


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
                        "description": "The email address, eg., rememeber0101@126.com",
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
                        "description": "The recipients' email addresses",
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


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/chat', methods=['POST'])
def chat():
    global conversation_history

    data = request.json
    user_message = data.get('message', '')

    # 检查用户是否想要结束对话
    if user_message.lower() in ['再见', '拜拜', '结束对话', 'exit', 'quit', '我要走了', '对话到此为止']:
        return jsonify({
            'response': '哼~我也不是很想和你聊天，再见！',
            'end_conversation': True
        })

    conversation_history.append({"role": "user", "content": user_message})

    response = chat_completion_request(
        messages=conversation_history,
        tools=tools
    )

    if content := response.choices[0].message.content:
        conversation_history.append({"role": "assistant", "content": content})
        return jsonify({
            'response': content,
            'end_conversation': False
        })
    else:
        fn_name = response.choices[0].message.tool_calls[0].function.name
        fn_args = response.choices[0].message.tool_calls[0].function.arguments

        if fn_name == "send_email":
            try:
                args = json.loads(fn_args)
                response = {
                    'response': f"邮件内容如下：\n发件人: {args['FromEmail']}\n收件人: {args['Recipients']}\n主题: {args['Subject']}\n内容: {args['Body']}\n\n请确认是否发送？",
                    'end_conversation': False,
                    'action': 'confirm_email',
                    'email_data': args
                }
                return jsonify(response)
            except Exception as e:
                return jsonify({
                    'response': f"发送邮件时出错：{str(e)}",
                    'end_conversation': False
                })
        elif fn_name == "find_point":
            try:
                args = json.loads(fn_args)
                target_point = tuple(args['target_point'])
                nearest_point, image_base64 = find_point(
                    target_point, num_data)
                response = f"距离点{target_point}最近的点是{nearest_point}。"
                conversation_history.append(
                    {"role": "assistant", "content": response})
                return jsonify({
                    'response': response,
                    'end_conversation': False,
                    'image': image_base64
                })
            except Exception as e:
                return jsonify({
                    'response': f"查找最近点时出错：{str(e)}",
                    'end_conversation': False
                })
        elif fn_name == "get_current_time":
            try:
                now_time = get_current_time()
                response = f"函数输出信息：{now_time}"
                print(f"【AI】: {response}")
                conversation_history.append(
                    {"role": "assistant", "content": response})
                # 返回当前时间
                return jsonify({
                    'response': response,
                    'end_conversation': False,
                })

            except Exception as e:
                print(f"查找时间出错：{e}")
                conversation_history.append(
                    {"role": "assistant", "content": "抱歉，无法查找当前时间！"})
                return jsonify(response)


@app.route('/send_email', methods=['POST'])
def send_email_route():
    data = request.json
    try:
        send_email(
            sender_email=data["FromEmail"],
            sender_authorization_code=AUTHORIZATION_CODE,
            recipient_email=data["Recipients"],
            subject=data["Subject"],
            body=data["Body"]
        )
        return jsonify({
            'response': "邮件已发送，还需要什么帮助吗？",
            'end_conversation': False
        })
    except Exception as e:
        return jsonify({
            'response': f"发送邮件时出错：{str(e)}",
            'end_conversation': False
        })


if __name__ == "__main__":
    # 读取num_data.json文件
    with open('num_data.json', 'r', encoding='utf-8') as f:
        num_data = json.load(f)
    app.run(debug=True)
