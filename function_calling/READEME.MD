# Function calling 

## 学习参考的文档  

### Open AI 的参考文档：
>https://platform.openai.com/docs/guides/function-calling?api-mode=responses&example=send-email

### 阿里千问系列Function calling的参考文档：
>https://help.aliyun.com/zh/model-studio/qwen-function-calling?spm=a2c4g.11186623.0.i8#b0910669927j7

## 下载代码及安装相关依赖  
### 首先将我的代码库clone到你的本地电脑上；
### 方式1：直接在代码库界面点击CODE;然后点击Download Zip；代码库链接：
>https://github.com/chuyu2025/chu-star

### 方式2：使用git clone 命令，打开终端运行以下命令：
>git clone https://github.com/chuyu2025/chu-star.git

### 1.在vscode中打开项目，选择function_calling文件；保证终端是在function_calling文件的路径下；

### 2.先创建一个虚拟环境(注意vevn和.venv中间有一个空格)；
>python -m venv .venv

#### 如果路径前没有出现(.venv)的话去激活一下虚拟环境：
>.venv\Scripts\activate.bat

### 3.安装所需依赖库，博主将程序所需的依赖库名单放到了requirements.txt文件中，可以执行以下命令一键安装。
>pip install -r requirements.txt  

## 代码介绍及运行模型所需要的API申请方法

### 一、main_code.py集成了3个function_calling函数；main_web.py是将main_code集成到了网页中；
1.查询当前时间；  

2.发送邮件；  

3.查找数据库num_data.json中距离某个输入点距离最近点的点；

### 二、在.env文件中要填写你的大模型API-KEY和邮箱的授权码；
#### 通义千问API申请网址：
>https://help.aliyun.com/zh/model-studio/get-api-key?spm=a2c4g.11186623.help-menu-2400256.d_2_0_0.7dc27297XIkwnW&scm=20140722.H_2712195._.OR_help-T_cn~zh-V_1

#### 网易邮箱客户端协议，获取授权码网址：
>https://help.mail.163.com/faqDetail.do?code=d7a5dc8471cd0c0e8b4b8f4f8e49998b374173cfe9171305fa1ce630d7f67ac2a5feb28b66796d3b

### 这些工作完成后就可以愉快的运行代码啦~  

