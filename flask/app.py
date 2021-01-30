from flask import Flask, jsonify, render_template
from flask_restx import Api, Resource
from dbaccess import DBAccess
import logging
from logging import Formatter, FileHandler
from logging import handlers
from time import time

# 로그 옵션 설정
logging.basicConfig(level="DEBUG")

# 로그 객체 생성
logger = logging.getLogger(__name__)

# 로그 파일 제작 및 기록 형식 지정
fileHandler = FileHandler('log/flask.log')
fileHandler.setFormatter(
    Formatter('[%(asctime)s][%(levelname)s|%(filename)s:%(lineno)s] >> %(message)s'))
fileHandler = logging.handlers.RotatingFileHandler(filename='./log/flask.log')
logger.addHandler(fileHandler)

# 초기 DB 업데이트
db = DBAccess()
db.update()
db.close()

# Flask 객체 및 DB 접속 객체 생성
app = Flask(__name__)
api = Api(app,
          version="1.0",
          title="SeungShin's API Server",
          description="Info Broadcast",
          terms_url="/",
          contact="cesf99@gnu.ac.kr"
          )

@api.route("/nubija")
class Nubija(Resource):
    def get(self):
        db = DBAccess()
        data = db.read(0)
        db.close()
        return data


if __name__ == "__main__":
    app.run(debug=True)
