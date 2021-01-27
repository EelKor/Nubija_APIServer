from flask import Flask, jsonify, render_template
from flask_restx import Api, Resource
from dbaccess import DBAccess
import logging
from logging import Formatter, FileHandler
from logging import handlers
from time import time

# 로그 파일 설정
fileMaxByte = 1024 * 1024 * 100
log_file_count = 20

# 로그 옵션 설정
logging.basicConfig(level="DEBUG")

# 로그 객체 생성
logger = logging.getLogger(__name__)

# 로그 파일 제작 및 기록 형식 지정
fileHandler = FileHandler('log/flask.log')
fileHandler.setFormatter(
    Formatter('[%(asctime)s][%(levelname)s|%(filename)s:%(lineno)s] >> %(message)s'))
fileHandler = logging.handlers.RotatingFileHandler(filename='./log/flask.log', maxBytes= fileMaxByte, backupCount= log_file_count)
logger.addHandler(fileHandler)

# Flask 객체 및 DB 접속 객체 생성
app = Flask(__name__)
api = Api(app,
          version="1.0",
          title="SeungShin's API Server",
          description="Info Broadcast",
          terms_url="/",
          contact="cesf99@gnu.ac.kr"
          )
db = DBAccess()

@api.route("/nubija")
class Nubija(Resource):
    def get(self):
        return db.read(0)

if __name__ == "__main__":
    app.run(debug=True)
