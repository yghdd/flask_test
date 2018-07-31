from flask import request, session
from flask_restful import Resource, reqparse, fields, marshal
from flask_sqlalchemy import BaseQuery

from App import dao
from App.models import Movies, User, Qx
from App.settings import QX

#修饰函数，判断用户是否具有权限
#QX参数，表示执行的操作权限
def qx(caozuo):
    def checkQx(fn):
        def action(*args,**kwargs):
            #获取用户的token,{token:id},从request中传来的
            token = request.args.get('token')
            u_id=session.get(token)
            if not  u_id:
                return {'msg':'请先登录'}
            user:User = dao.getById(User,u_id)
            # 用户要执行什么操作
            opt=dao.query(Qx).filter(Qx.right == caozuo).first()
            # 拿用户的权限和settings中的权限值做&操作
            if not user.reghts & caozuo == caozuo:

                return {'msg':'对不起您不具备{}权限'.format(opt.name)}
            return fn(*args,**kwargs)
        return action
    return checkQx

class MoviesApi(Resource):
    #定制输出字段
    movies_fields={
        'showname':fields.String,
        'director':fields.String,
        'leadingRole':fields.String,
        'type':fields.String,
        'country':fields.String,
        'language':fields.String,
        'backgroundpicture':fields.String
    }

    out_fields={
        'status':fields.Integer,
        'msg':fields.String,
        'data':fields.Nested(movies_fields)
    }
    #定制输入字段
    parser = reqparse.RequestParser()
    parser.add_argument('flag',type=int, required=True,help='必须指定类型')
    parser.add_argument('city',default='')
    parser.add_argument('region',default='')
    parser.add_argument('orderby',default='openday')#1 降序，0，升序
    parser.add_argument('sort',type = int,default=1,help='页码必须为数值')
    parser.add_argument('page', type=int, default=1, help='页码必须是数值')
    parser.add_argument('limit', type=int, default=10, help='每页显示的大小必须是数值')
    def get(self):
        args= self.parser.parse_args()
        qs:BaseQuery=dao.query(Movies).filter(Movies.flag==args.get('flag'))
        sort = args.get('sort')
       #排序
        qs:BaseQuery = qs.order_by(('-' if sort==1 else '')+args.get('orderby'))
        #分页
        pager=qs.paginate(args.get('page'),args.get('limit'))
        print('获取的总影片数',len(qs.all()))
        data={'status':200,
              'msg':'所有电影',
      #pager.items 表示当前页的数据
              'data':pager.items}
        return marshal(data,self.out_fields)

    @qx(QX.DELETE_QX)
    def delete(self):
        mid=request.args.get('mid')
        # #从session中获取登录用户的token
        # user_id = session.get(request.args.get('token'))
        # if not user_id:
        #     return {'msg':'请先登录'}
        # loginUser:User = dao.getById(User,user_id)
        #
        # #删除影片功能
        # if loginUser.reghts & QX.DELETE_QX ==QX.DELETE_QX:
        #     #当前用户有删除权限
        movie = dao.getById(Movies,mid)
        if not movie:
            return {'msg':'电影不存在'}
        dao.delete(movie)
        return {'msg':'删除成功'}


