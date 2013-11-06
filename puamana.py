from flask import Flask
from flask import render_template, redirect, url_for
from flask import request
from flask.ext.pymongo import PyMongo
import datetime
import urllib2
import re

app = Flask(__name__)
mongo = PyMongo(app)

@app.route('/')
def index():
    today =  datetime.datetime.now();
    if today.weekday() == 1:
      offset = 7
    else:
      offset = (today.weekday() - 1) % 7
    last_tuesday = today - datetime.timedelta(days=offset)
    print last_tuesday.day
    links = mongo.db.data.find({"date" : {"$gte": last_tuesday}}).sort('date', -1);
    return render_template('index.html', links=links, last=str(last_tuesday.day) + suffix(last_tuesday.day))

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

@app.route('/scrape/')
def scrape():
  p = re.compile('<p>([a-zA-z].*?)<\/p>', re.DOTALL)
  try:
    text = urllib2.urlopen(request.args['url']).read()
  except:
    return ""
  if (p.search(text)):
    return p.search(text).group()
  else:
    return ""

def suffix(d):
    return 'th' if 11<=d<=13 else {1:'st',2:'nd',3:'rd'}.get(d%10, 'th')

if __name__ == '__main__':
    app.run(debug=True)
