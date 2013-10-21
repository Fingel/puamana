from flask import Flask
from flask import render_template
from flask import request
from flask.ext.pymongo import PyMongo
import datetime

app = Flask(__name__)
mongo = PyMongo(app)

@app.route('/')
def index():
    links = mongo.db.data.find();
    return render_template('index.html', links=links)

@app.route('/add', methods=['POST', 'GET'])
def add():
    if request.method == 'GET':
      return render_template('add.html')
    else:
      data = {"url": request.form['url'],
              "description": request.form['description'],
              "date": datetime.datetime.utcnow()}
      mongo.db.data.insert(data);
      return render_template('index.html', links = mongo.db.data.find())

if __name__ == '__main__':
    app.run(debug=True)
