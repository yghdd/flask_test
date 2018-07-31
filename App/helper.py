# 自定义工具类
import hashlib
import uuid

from flask import request
from flask_mail import Message

import App.ext


def md5_crypt(txt):
    m = hashlib.md5()
    m.update(txt.encode())

    return m.hexdigest()


def sendEmail(u,url):
    token = md5_crypt(str(uuid.uuid4()))

    # 将token设置到redis缓存中
    App.ext.cache.set(token, u.id, timeout=10 * 60)  # 允许10分钟内来激活用户
    print('toke',token)
    print('id',u.id)
    active_url = url + 'account/?opt=active&token=' + token

    print('路径',active_url)
    # 发送邮件
    msg = Message(subject='淘票票用户激活',
                  recipients=[u.email],
                  sender='zhaoairong0108@163.com')
    msg.html = "<h1>{} 注册成功！</h1><h3>请先<a href={}>激活</a>注册账号</h3> <h2>或者复制地址到浏览器: {}</h2>".format(u.name, active_url,
                                                                                                  active_url)

    try:
        print(msg.html)
        App.ext.mail.send(msg)
        print('邮件已发送')
    except Exception as e:
        print(e)
        print('邮件发送失败')