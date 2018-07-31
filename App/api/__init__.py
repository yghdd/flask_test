from flask_restful import Api

from App.api.account import AccountApi
from App.api.cinemas import CinemasApi
from App.api.city import CityApi
from App.api.movies import MoviesApi
from App.api.upload import UploadApi
from App.api.user import UserApi
from App.models import Cinemas

api = Api()  # 创建RESTful的Api对象


def init_api(app):
    api.init_app(app)


# 向api接口中添加资源(Resource)
api.add_resource(CityApi, '/city/')
api.add_resource(UserApi, '/user/')
api.add_resource(AccountApi, '/account/')
api.add_resource(MoviesApi,'/movies/')
api.add_resource(UploadApi,'/upload/')
api.add_resource(CinemasApi,'/cinemas/')