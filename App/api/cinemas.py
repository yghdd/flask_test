from flask_restful import Resource, reqparse, fields, marshal_with

##
# 获取部分影院信息(排序)
# GET  http://127.0.0.1:8000/cinemas?city=&sort=&orderby=&limit=
# 获取所有影院信息(排序)
# GET  http://127.0.0.1:8000/cinemas?city=&sort=&orderby=
#
#
#
# 4、增加影院
# POST  http://127.0.0.1:8000/cinemas
# 5、减少影院
# DELETE  http://127.0.0.1:8000/cinemas
# 6、修改影院信息
# PUT  http://127.0.0.1:8000/cinemas
#
#
# 获取所在城市的区县信息
# GET  http://127.0.0.1:8000/areas?city=
# 获取所有影院信息
# GET  http://127.0.0.1:8000/cinemas
# 分页获取影院信息
# POST  http://127.0.0.1:8000/cinemas?city=&area=&page=&count=
# #
from flask_sqlalchemy import BaseQuery

from App import dao
from App.models import Cinemas


class CinemasApi(Resource):
    #定制输出字段
    #输出字段的子字段，必须写在上方
    cinemas_fields = {
        'name':fields.String,
        'city':fields.String,
        'district':fields.String,
        'address':fields.String,
        'phone':fields.String,
        'score':fields.Float,
        'servicecharge':fields.Float,
        'flag':fields.Boolean

    }
    out_fields={
        'data':fields.String,
        'status':fields.Integer,
        'data':fields.Nested(cinemas_fields)
    }

    #定制输入字段
    parse = reqparse.RequestParser()
    parse.add_argument('city', required=True, help='必须提供城市信息')
    parse.add_argument('sort',default='1') #评分 1降序,2升序
    parse.add_argument('order_by',default='score')
    parse.add_argument('limit',type=int,default=10,help='显示内容必须是数字型') # 限制，每页显示的数量
    parse.add_argument('page',type=int,help='页码必须是数字型',default=1)

    #获取部分影院信息(排序)
    # GET  http://127.0.0.1:8000/cinemas?city=&sort=&orderby=&limit（限制）=
    # 获取所有影院信息(排序)
    # GET  http://127.0.0.1:8000/cinemas?city=&sort=&orderby=
    @marshal_with(out_fields)
    def get(self):
        args =self.parse.parse_args()
        city =args.get('city')
        sort = args.get('sort')
        qs:BaseQuery = dao.query(Cinemas).filter(Cinemas.city==city)
        cinemas2:BaseQuery = qs.order_by(('-' if sort else '')+args.get('order_by'))
        page =cinemas2.paginate(args.get('page'),args.get('limit'))
        print('当前城市的总影院数',cinemas2.count())
        return {'status':200,'msg':"ok",'data':page.items}



    #新增资源
    def post(self):
        pass
    #修改某一资源
    def put(self):
        pass
    #修改多个资源
    def patsh(self):
        pass
    #删除资源
    def delete(self):
        pass