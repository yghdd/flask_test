import os


class Config():
    DEBUG = True
    ENV = 'development'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:ygh19940426@localhost:3306/taopiaopiao'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    #配置邮箱
    MAIL_SERVER ='smtp.163.com'  #邮箱服务器
    MAIL_USERNAME='zhaoairong0108@163.com'
    MAIL_PASSWORD='zcr13571934239'  #授权码

    #配置session
    SECRET_KEY='DASDSFA1231#$@$#'
    #获取当前的绝对路径
    ABS_PATH=os.path.abspath(__name__)
    #获取settings的所在目录名
    BASE_PATH=os.path.dirname(ABS_PATH)
    STATIC_DIR=os.path.join(BASE_PATH,'APP\static')
    MEDIA_DIR = os.path.join(STATIC_DIR,'uploads')


class QX():
    QUERT_QX = 1
    EDIT_QX = 2
    DELETE_QX = 4
    ADD_QX = 8
    MAIL_QX = 16
    PLAY_QX = 32
