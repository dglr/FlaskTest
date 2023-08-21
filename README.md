# 概述

这是一个使用python的Flask框架完成的简易的具备用户功能的API Server，特性如下：

支持用户登录、登出 

支持通过某个安全的特定请求，直接添加用户 

支持通过邮箱注册新用户: 

​	当用户提交注册请求后，API Server 会通过某个邮件服务器给用户的邮箱发送一封包含验证码的邮件 

​	当用户提交验证注册请求后，API Server 会验证请求用户名、验证码，若验证通过，则用户注册成功 

账户体系格式要求：用户名必须为符合国内格式的手机号码 (如 1300000000)，或者是邮箱： 密码必须是包含且仅包含大写、小写、数字的 6位数以上的字符。

支持查询用户登录状态

仓库里有三个python文件：

main.py：Server文件

unit_test.py：测试用户登录成功和失败

add_user_test.py：测试：1管理员添加用户 2 非管理员添加用户 3 未添加管理员的token添加用户

# Pre-requisites

安装依赖：

```python
pip install Flask flask-httpauth passlib Flask-Mail
```

# Getting Started

运行`main.py`：

```python
python main.py
```

可以看到

![image](https://github.com/dglr/FlaskTest/blob/master/image-20230821190551191.png)

接下来运行两个单元测试

```python
python add_user_test.py
python unit_test.py
```

![image](https://github.com/dglr/FlaskTest/blob/master/image-20230821190647393.png)

![image](https://github.com/dglr/FlaskTest/blob/master/image-20230821190700380.png)
