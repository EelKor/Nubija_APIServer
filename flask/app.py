from flask import Flask, jsonify, render_template
from dbaccess import DBAccess
import logging
from logging import Formatter, FileHandler
from logging import handlers
from time import time

#로그 파일 설정
fileMaxByte = 1024 * 1024 * 100
log_file_count = 20

logging.basicConfig(level="DEBUG")

logger = logging.getLogger(__name__)

fileHandler = FileHandler('log/flask.log')
fileHandler.setFormatter(
    Formatter('[%(asctime)s][%(levelname)s|%(filename)s:%(lineno)s] >> %(message)s'))
fileHandler = logging.handlers.RotatingFileHandler(filename='./log/flask.log', maxBytes= fileMaxByte, backupCount= log_file_count)
logger.addHandler(fileHandler)



app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
db = DBAccess()

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/terminalinfo/<id>')
def terminalinfo(id):
    id = int(id)
    data = db.read(id)
    return jsonify(data[::])

@app.errorhandler(404)
def page_not_found(error):
    logger.exception(error)
    return render_template("error_404.html"), 404



@app.errorhandler(500)
def internal_server_error(error):
    logger.exception(error)
    return render_template("error_500.html"), 500


if __name__ == "__main__":
    app.run()

