from flask import Flask, jsonify, render_template
from dbaccess import DBAccess

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


if __name__ == "__main__":
    app.run()

