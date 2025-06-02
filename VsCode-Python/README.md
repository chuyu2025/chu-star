# Python安装及多版本管理、VsCode配置、构建虚拟环境

## 下载python解释器

### 官网地址：
>https://www.python.org/downloads/  

### 查看电脑目前有几个python的版本
>where python

### 查看电脑是64位还是32位  
**方法一：点击设置，点击系统，在系统信息里查看电脑的系统类型**  
**方法二：在cmd中输入指令：wmic os get osarchitecture**  

### 下载对应的python版本  

1.选择Add python.exe to PATH  

2.选择Customize installation   
   
**3.★★★在Advanced options这一步，勾选install Python for all users，并将解释器路径放到一个c盘没有中文路径下的一个你比较熟悉能随时想起来的路径下。**
<p align="center">
  <img src="Picture/one.png" width="500" alt="GitHub"/>
</p>  
<p align="center">
  <img src="Picture/two.png" width="500" alt="GitHub"/>
</p>   
<p align="center">
  <img src="Picture/three.png" width="500" alt="GitHub"/>
</p>   

### 查看环境变量是否添加

1.点击设置，点击高级系统设置，点击环境变量；  
2.在系统环境变量中点击path，查看刚刚下载的python路径是否被添加到环境变量中；  
3.在终端输入以下命令查看python是否安装成功：
> python --version
<p align="center">
  <img src="Picture/four.png" width="700
  " alt="GitHub"/>
</p>   

### 多个python的版本管理

**如果电脑存在多个版本的python，系统默认会调用环境变量中第一个版本的python，可以去调整它们在环境变量中的位置。**  
**或者可以将python解释器复制粘贴并重命名，然后调用的时候输入对应的python解释器名称**    
>python3.12 --version

<p align="center">
  <img src="Picture/five.png" width="700
  " alt="GitHub"/>
</p>  
<p align="center">
  <img src="Picture/six.png" width="700
  " alt="GitHub"/>
</p>    

## VsCode安装

### VsCode官网:
>https://code.visualstudio.com/ 

**安装python插件**  

<p align="center">
  <img src="Picture/seven.png" width="700
  " alt="GitHub"/>
</p>  

### 切换python解释器
<p align="center">
  <img src="Picture/eight.png" width="700
  " alt="GitHub"/>
</p>    

### 设置默认终端
<p align="center">
  <img src="Picture/nine.png" width="300
  " alt="GitHub"/>
</p> 
<p align="center">
  <img src="Picture/ten.png" width="700
  " alt="GitHub"/>
</p> 

## 一些便捷式编程设置
<p align="center">
  <img src="Picture/eleven.png" width="700
  " alt="GitHub"/>
</p>   
<p align="center">
  <img src="Picture/twelve.png" width="700
  " alt="GitHub"/>
</p>  

## 一些好用的VsCode的第三方包

### autopep8 
### 自动格式化代码
<p align="center">
  <img src="Picture/thirteen.png" width="400
  " alt="GitHub"/>
</p>   


## 创建虚拟环境
### 根据自己的python解释器版本输入在项目地址的终端下输入以下命令
>python -m venv .venv  

### 在虚拟环境中下载的包会存储在.env文件中的site-packes里

