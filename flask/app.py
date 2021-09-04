from json.decoder import JSONDecoder
from flask import Flask, jsonify, render_template
from flask.json import JSONEncoder
from flask_restx import Api, Resource
from dbaccess import DBAccess


# 초기 DB 업데이트
db = DBAccess()
db.update()
db.close()

# Flask 객체 및 DB 접속 객체 생성
app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

api = Api(app,
          version="1.0",
          title="SeungShin's API Server",
          description="Info Broadcast",
          terms_url="/",
          contact="cesf99@gnu.ac.kr",
          )


@api.route("/nubija2")
class Nubija(Resource):
    def get(self):
        db = DBAccess()
        data = db.read(0)
        db.close()
        return data


if __name__ == "__main__":
    app.run(debug=True)
