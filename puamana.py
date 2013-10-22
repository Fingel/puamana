from flask import Flask
from flask import render_template, redirect, url_for
from flask import request
from flask.ext.pymongo import PyMongo
import datetime

app = Flask(__name__)
mongo = PyMongo(app)

@app.route('/')
def index():
    links = mongo.db.data.find().sort('date', -1);
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
      return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
