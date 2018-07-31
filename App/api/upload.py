import uuid

import os

from flask import session
from flask_restful import Resource, reqparse
from werkzeug.datastructures import FileStorage

from App import settings, dao
from App.models import User


class UploadApi(Resource):
    def post(self):
        parse=reqparse.RequestParser()
        parse.add_argument('img',dest='photo',type=FileStorage,required=True,help='必须提供图片',
                           location='files')
        parse.add_argument('token',type=str,required=True,help='必须提供token')
        args = parse.parse_args()
        token = args.get('token')
        uFile:FileStorage = args.get('photo')
        newFileName = str(uuid.uuid4()).replace('-','')
        newFileName += '.'+uFile.filename.split('.')[-1]
        uFile.save(os.path.join(settings.Config.MEDIA_DIR,newFileName))
        uFile.close()
        id = session.get(token)
        print('哈哈',id)
        user = dao.getById(User,id)
        user.photo_2 = newFileName
        dao.save(user)
        return {'static':'200',
                'msg':'上传成功',
                'path':'/static/uploads/'+newFileName}




