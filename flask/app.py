from flask import Flask, jsonify, render_template
from dbaccess import DBAccess
import logging
from logging import Formatter, FileHandler

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
fileHandler = FileHandler('log/flask.log')
fileHandler.setFormatter(
    Formatter('[%(asctime)s][%(levelname)s|%(filename)s:%(lineno)s] >> %(message)s'))
logger.addHandler(fileHandler)

app = Flask(__name__)
db = DBAccess()

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/terminalinfo/<id>')
def terminalinfo(id):
    id = int(id)
    data = db.read(id)
    return jsonify(data[0])

@app.errorhandler(404)
def page_not_found(error):
    logger.exception(error)



@app.errorhandler(500)
def internal_server_error(error):
    logger.exception(error)


if __name__ == "__main__":
    app.run()

