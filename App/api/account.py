import datetime
import uuid

from flask import request, session
from flask_restful import Resource, reqparse, fields, marshal

import App.ext
import tasks
from App import dao, helper
from App.helper import md5_crypt
from App.models import User, db


class AccountApi(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('opt',required = True,help='操作不能为空')
 #    parser.add_argument('token')

    def get(self):
        # 从请求参数中获取opt和token参数值
        # 如果opt 为active ，则从redis缓存中查询token对应的user.id
        # 再通过 user.id查询数据库中用户， 最后更新用户的is_active状态为True
        args = self.parser.parse_args()
        opt = args.get('opt')
        if opt == 'active':
            activeParse = self.parser.copy()
            activeParse.add_argument('token',required=True,help='没有提供TOKEN')

            args = activeParse.parse_args()
            token = args.get('token')
            id = App.ext.cache.get(token)
            print('------',id,token)
            if id:
                user=dao.getById(User,id)
                user.is_active = True
                dao.save(user)
                #清除缓存
                App.ext.cache.clear()
                print('用户id',id)
                return {'msg':' 恭喜您的{}用户激活成功!'.format(user.name)}
            else:
                #cache过时了，申请用户激活
                reactive_url = request.host_url+'account/?opt=reactive'
                return {'msg':'验证超时，请重新激活'+reactive_url}
        elif opt ==  'login':
             return self.login()
        elif opt == 'reactive':
             return self.reactive()
        elif opt =='loginout':
             return self.loginout()
        return {'msg': '404'}


    def  login(self):   #GET请求时，opt为login时只行该方法
        loginParser = self.parser.copy()
        loginParser.add_argument('name', required=True, help='必须提供用户名')
        loginParser.add_argument('password', required=True, help='必须提供密码')
        args = loginParser.parse_args()   #验证数据
        name = args.get('name')
        password = md5_crypt(args.get('password'))
        user = dao.query(User).filter(db.and_(User.name==name,User.password==password,
                                              User.is_active==True,User.is_life==True)).first()
        print(user)
        if user:
            user.last_login_time=datetime.datetime.now()
            dao.save(user)
            user_fields={
                'id':fields.Integer,
                'name':fields.String,
                'phone':fields.String,
                'nickName':fields.String,
                'email':fields.String
            }
            out_fields={
                'msg': fields.String,
                'token':fields.String,
                'data':fields.Nested(user_fields)
            }
            #如果用户登录成功，session存入{token:userid}
            token = helper.md5_crypt(str(uuid.uuid4()))
            session[token]=user.id
            data = {'msg':'您已登陆成功',
                    'token':token,
                    'data':user}
            return marshal(data,out_fields)
        else:
            return {'msg':'用户名或密码错误'}

    #重新激活
    def reactive(self):
        reactiveParser =self.parser.copy()
        reactiveParser.add_argument('email',required=True,help='邮箱不能空')
        args = reactiveParser.parse_args()
        email = args.get('email')
        qs=dao.query(User).filter(User.email.__eq__(email))
        if not qs.count():

            return {'status': 666, 'msg': email + '邮箱未被注册'}
        print('request.host_url',request.host_url)
        print('request.path',request.path)
        print('request.url',request.url)
        print('request.base_url',request)
        url =request.host_url
        # 重新发送邮件
        tasks.sendMail.delay(qs.first().id,url)
        print(qs.first().id)
        return {'mag':'重新申请用户激活，请查收邮箱'}

    #登出
    def loginout(self):
        loginoutParser = self.parser.copy()
        loginoutParser.add_argument('token', required=True,help='退出用户必须提供token')
        args = loginoutParser.parse_args() #验证数据
        token = args.get('token')
        userid = session.get(token)
        if not userid:
            return {'msg':'用户未登录，请先登录'}
        user= dao.getById(User,userid)
        if not user:
            return {'status':400,'msg':'token无效，退出失败'}
        session.pop(token) #从session字典中删除token
        return {'status':200,'msg':'退出成功'}