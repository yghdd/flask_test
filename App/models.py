# 声明数据库中表对应的模型类
from datetime import datetime
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String, Integer, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import relationship, backref

db = SQLAlchemy()


def init_db(app):
    db.init_app(app)
    Migrate(app, db)


class IdBase():
    id = Column(Integer, primary_key=True, autoincrement=True)

class Letter(db.Model, IdBase):
    __tablename__ = 't_letter'

    name = Column(String(10))


class Role(db.Model, IdBase):
    # 用户角色
    name = Column(String(20))
    rights = Column(Integer, default=1)

class City(db.Model, IdBase):
    __tablename__ = 't_city'

    # id = Column(Integer, primary_key=True, autoincrement=True)
    parentId = Column(Integer, default=0)
    regionName = Column(String(20))
    cityCode = Column(Integer)
    pinYin = Column(String(50))

    letter_id = Column(Integer, ForeignKey(Letter.id))
    letter = relationship("Letter", backref=backref("citys", lazy=True))


class User(db.Model, IdBase):
    __tablename__ = 't_user'

    name = Column(String(50), unique=True)
    password = Column(String(50))
    nickName = Column(String(20))
    email = Column(String(50), unique=True)
    phone = Column(String(12), unique=True)
    is_active = Column(Boolean, default=False)
    is_life = Column(Boolean, default=True)
    regist_time = Column(DateTime, default=datetime.now())
    last_login_time = Column(DateTime)
    #新增头像的属性
    photo_1  = Column(String(100),nullable=True) #原图
    photo_2 = Column(String(100),nullable=True) #小图
    #权限，（被管理员授权的）
    reghts = Column(Integer,default=1)

    #用户角色
    role_id = Column(Integer,ForeignKey(Role.id))
    role = relationship('Role',backref=backref('users',lazy=True))
class Movies(db.Model,IdBase):
    __tablename__ = 't_movies'
    #中文电影名
    showname = Column(String(50))
    #英文电影名
    shownameen = Column(String(50))
    #导演
    director = Column(String(50))
    #演员
    leadingRole = Column(String(200))
    #类型
    type = Column(String(200))
    #国家
    country = Column(String(20))
    #语种
    language = Column(String(20))
    #电影时长
    duration = Column(Integer)
    #2d,3d
    screeningmodel = Column(String(10))
    #上映时间
    openday = Column(DateTime)
    #背景图片
    backgroundpicture = Column(String(100))
    #状态( 0:所有    1:热映   2:即将上映)
    flag = Column(Integer)
    #是否删除影院
    isdelete = Column(Boolean,default=False)


class Cinemas(db.Model,IdBase):
    name = Column(String(100))
    city = Column(db.String(20))
    #区域
    district = Column(String(200))
    #地址
    address = Column(String(200))
    phone = Column(String(50))
    #评分
    score = Column(db.Float)
    # 影厅数量
    hallnum = Column(Integer)
    #手续费
    servicecharge =Column(db.Float)
    #限购数量
    astrict = Column(Integer)
    #状态(营业、休息)
    flag = Column(Boolean,default=True)
    #是否删除 影厅
    isdelete =Column(Boolean,default=False)




class Qx(db.Model,IdBase):
    name = Column(String(30))
    right = Column(Integer)





