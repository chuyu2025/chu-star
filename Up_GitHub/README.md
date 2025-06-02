# 将项目代码上传至 GitHub 库的几种方法

## 步骤 1：下载 git

### git 官网地址：https://git-scm.com/?hl=zh-cn

### 下载后使用以下命令查看是否安装成功：

> git --version

## 步骤 2：GitHub 创建仓库

### 加速器推荐：steam ++

### 下载网址：

> https://steampp.net/

### GitHub 网址：

> https://github.com/

◆◆◆**注意这里最好创建的仓库是一个空白仓库**◆◆◆

## 方法 1：直接在 GitHub 中上传项目和代码

### 1.点击：Add file

### 点击 create new file，并在文件名后打入/则会创建一个文件夹

### 点击 upload files 会从本地文件中选择上传

<p align="center">
  <img src="Picture/one.png" width="600" alt="GitHub"/>
</p>

### 2.创建文件夹

<p align="center">
  <img src="Picture/two.png" width="600" alt="GitHub"/>
</p>

### 3.创建文件夹

<p align="center">
  <img src="Picture/three.png" width="600" alt="GitHub"/>
</p>

## 方法 2：在 VsCode 中使用 git 上传项目和代码

### 1.在 cmd 或 VsCode 终端登陆 GitHub 用户名和邮箱

> 登陆 GitHub 用户名  
> git config --global user.name "John Doe"  
> 查看当前用户名  
> git config --global user.name  
> 登陆 GitHub 的邮箱  
> git config --global user.email johndoe@example.com  
> 查看当前邮箱  
> git config --global user.email

### 2.点击 initialize Repository 初始化仓库

<p align="center">
  <img src="Picture/four.png" width="600" alt="GitHub"/>
</p>

### 3.给本次的修改起一个标记,之后点击 Commit

<p align="center">
  <img src="Picture/five.png" width="600" alt="GitHub"/>
</p>

**当左下部出现如下标志说明本地初始化成功**

<p align="center">
  <img src="Picture/six.png" width="600" alt="GitHub"/>
</p>

### 3.接下来就是将项目上传到 GitHub，点击 add remote 添加远程仓库

<p align="center">
  <img src="Picture/seven.png" width="600" alt="GitHub"/>
</p>

**点击上部的 Add remote from GitHub**

<p align="center">
  <img src="Picture/eight.png" width="600" alt="GitHub"/>
</p>

**接下来就是按照提示登陆链接 GitHub 账号，链接好之后顶部会出现你的 GitHub 仓库，选择一个你要上传到的仓库,并输入本次上传的文件的命名**

### 具体操作过程参考我的教学视频：

> https://www.bilibili.com/video/BV1Hq7zzGEPt/?vd_source=12099d09fddf896d1fc41903a69054da

### 目前博主也没有涉及到很大的项目编辑，所以这两种上传项目的方式暂时已经足够我使用了，或者对于学生党来讲应该是足够的，等到以后博主不得不用到 git 更高阶的用法时再继续学习继续分享。

### 今天是六一儿童节祝各位小伙伴永葆童心，学业顺利~

![alt text](218E33EB.jpg)
