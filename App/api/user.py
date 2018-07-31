from flask import request
from flask_restful import Resource, reqparse
import App.ext

import tasks
from App import helper, dao
from App.models import User


class UserApi(Resource):

    # 定制输入的字段
    parser = reqparse.RequestParser()
    parser.add_argument('username', dest='name', required=True, help='用户名不能为空')

    def post(self):
        # 从基本的请求解析器中复制请求参数说明
        registParser = self.parser.copy()

        # 再添加注册时使用
        registParser.add_argument('password', dest='pwd', required=True, help='口令不能为空')
        registParser.add_argument('email', required=True, help='邮箱不能为空！')
        registParser.add_argument('phone', required=True, help='手机号不能为空！')
        registParser.add_argument('nickname', required=True, help='昵称不能为空！')

        # 验证请求参数是满足要求
        args = registParser.parse_args()

        u = User()
        u.name = args.get('name')
        u.nickName = args.get('nickname')
        u.email = args.get('email')
        u.phone = args.get('phone')
        u.password = helper.md5_crypt(args.get('pwd'))

        if dao.save(u):
            # token = helper.md5_crypt(str(uuid.uuid4()))
            #
            # # 将token设置到redis缓存中
            # App.ext.cache.set(token, u.id, timeout=10 * 60)  # 允许10分钟内来激活用户
            #
            # active_url = request.host_url + 'account/?opt=active&token=' + token

            # # 发送邮件
            # msg = Message(subject='淘票票用户激活',
            #               recipients=[u.email],
            #               sender='disenqf@163.com')
            # msg.html = "<h1>{} 注册成功！</h1><h3>请先<a href={}>激活</a>注册账号</h3> <h2>或者复制地址到浏览器: {}</h2>".format(u.name, active_url, active_url)
            #
            # App.ext.mail.send(msg)e
            url = request.host_url
            tasks.sendMail.delay(u.id,url)

            return {'status': 200,
                    'msg': '用户注册成功'}

        return {'status': 201,
                'msg': '用户注册失败'}

    def get(self):
        # 验证用户名是否已注册
        args = self.parser.parse_args()

        name = args.get('name')

        qs = dao.query(User).filter(User.name == name)
        if qs.count():
            return {'status': 202, 'msg': name+' 用户名已被注册!'}

        return {'status': 200, 'msg': name + ' 用户名可以注册!'}
