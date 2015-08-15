# all the imports
import os,binascii
from flask import Flask, request, session, g, redirect, url_for, abort, \
		render_template, flash, Blueprint, stream_with_context, Response
from flaskext.mysql import MySQL
from config import config
from werkzeug.utils import secure_filename
from flask import send_from_directory
import datetime
import logging
from logging.handlers import SMTPHandler
from collections import Counter
import requests
import json

credentials = None

mysql = MySQL()
# create our little application :)

app = Flask(__name__)

for key in config:
	app.config[key] = config[key]

mysql.init_app(app)

def tup2float(tup):
	return float('.'.join(str(x) for x in tup))

def get_cursor():
	return mysql.connect().cursor()

@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html'), 404

# Add new username to leaderboard DB
@app.route('/add/<username>/', methods=['GET', 'POST'])
def addUser(username):
	uname = username
	db = get_cursor()
	score = '0'
	countQuery = 'SELECT COUNT(*) FROM Leaderboard'
	db.execute(countQuery)
	data = db.fetchone()[0]
	count = data + 1
	sql = 'INSERT INTO `Leaderboard` (`idLeaderboard`, `username`, `score`) VALUES ("%s","%s","%s")'
	db.execute(sql%(count, uname, score))
	db.execute("COMMIT")
	json_data = {}
	json_data['idLeaderboard'] = str(count)
	json_data['username'] = uname
	json_data['score'] = score 
	return json.dumps(json_data)

# Update the score of a particular username
@app.route('/update/<username>/<score>', methods = ['GET', 'POST'])
def scoreUpdate(username, score):
	uname = username
	score = score
	db = get_cursor()
	updateQuery = 'UPDATE `Leaderboard` SET `score`="%s" where `username`="%s"'
	db.execute(updateQuery%(score, uname))
	db.execute("COMMIT")
	json_data = {}
	json_data['success'] = "True"
	return json.dumps(json_data)

# Show leaderboard
@app.route('/')
def screen():
	db = get_cursor()
	showQuery = 'select * from Leaderboard order by username, Score desc'
	db.execute(showQuery)
	data = db.fetchall()
	users = []
	for userObject in data:
		temp = {}
		temp['idLeaderboard'] = userObject[0]
		temp['username'] = userObject[1]
		temp['score'] = userObject[2]
		users.append(temp)
	print json.dumps(users)
	return json.dumps(users)

@app.teardown_appcontext
def close_db():
	"""Closes the database again at the end of the request."""
	get_cursor().close()

if __name__ == '__main__':
	app.debug = True
	app.secret_key=os.urandom(24)
	# app.permanent_session_lifetime = datetime.timedelta(seconds=200)
	app.run()