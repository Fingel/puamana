from flask import Flask
from flask import render_template, redirect, url_for
from flask import request
from flask.ext.pymongo import PyMongo
import datetime
from datetime import date, timedelta

app = Flask(__name__)
mongo = PyMongo(app)

@app.route('/')
def index():
    today =  datetime.datetime.now();
    if today.weekday() == 1:
      offset = 7
    else:
      offset = (today.weekday() - 1) % 7
    last_tuesday = today - timedelta(days=offset)
    links = mongo.db.data.find({"date" : {"$gte": last_tuesday}}).sort('date', -1);
    return render_template('index.html', links=links, last=last_tuesday)

@app.route('/all')
def all():
  return render_template('index.html', links=mongo.db.data.find().sort('date', -1));

@app.route('/add', methods=['POST', 'GET'])
def add():
    if request.method == 'GET':
      return render_template('add.html')
    else:
      data = {"url": request.form['url'],
              "description": request.form['description'],
              "date": datetime.datetime.now()}
      mongo.db.data.insert(data);
      return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
