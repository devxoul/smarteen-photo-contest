# -*- coding: utf8 -*-

from flask import Module, render_template, url_for, request, redirect, session, send_file
from contest.model import User, Photo
from contest.database import db
from facebook import GraphAPI
import json
import os

web = Module(__name__)

@web.route('/')
def index():
	if not session.get('user_id'):
		return redirect(url_for('login'))
	
	user = User.query.filter(User.id == session.get('user_id')).first()
	if not user:
		session.pop('user_id', None)
		return redirect(url_for('index'))
		
	photo = Photo.query.filter(Photo.user_id == user.id).order_by(Photo.date.desc()).first()
	return render_template('my_photo.html', user=user, photo=photo)

@web.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'GET':
		return render_template('login.html')
		
	elif request.method == 'POST':
		print json.dumps(request.form)
		
		if not request.form.has_key('facebook_id'):
			return 'no facebook id'
			
		if not request.form.has_key('facebook_token'):
			return 'no facebook token'
		
		# 가입된 회원 - 로그인
		user = User.query.filter(User.facebook_id == request.form['facebook_id']).first()
		if user:
			graph = GraphAPI(request.form['facebook_token'])
			me = graph.get_object('me', fields='id')
			print json.dumps(me)
			
			# 로그인 정보가 실제 페이스북 정보와 동일
			if request.form['facebook_id'] == me['id']:
				session['user_id'] = user.id
				return redirect(url_for('index'))
			else:
				return 'Facebook Auth Failure!'
			
		
		# 미가입된 회원 - 회원가입
		else:
			print 'name : ' + request.form['name']
			user = User(request.form['name'], request.form['facebook_id'], request.form['facebook_token'])
			db.session.add(user)
			db.session.commit()
			session['user_id'] = user.id
			return redirect(url_for('index'))
			
	return 'Method not allowed.'
	
@web.route('/logout', methods=['GET'])
def logout():
	session.pop('user_id', None)
	return redirect(url_for('index'))
	
@web.route('/photo', methods=['POST'])
def upload_photo():
	if request.method == 'POST':
		if not request.form.has_key('title'):
			return 'no title'
			
		if not request.form.has_key('description'):
			return 'no description'
		
		if not request.files.has_key('photo'):
			return 'no file'
		
		user = User.query.filter(User.id == session.get('user_id')).first()
		photo = Photo(request.form['title'], request.form['description'], user)
		db.session.add(photo)
		db.session.commit()
		photo.filename = '%d_%d.png' % (session.get('user_id'), photo.id)
		db.session.commit()
		
		path = os.path.join('/home/xoul/smarteen-photo-contest/media/', photo.filename)
		file = request.files['photo']
		file.save(path)
		
		return redirect(url_for('index'))
	
	return 'Method not allowed.'

@web.route('/photo/<int:photo_id>', methods=['GET'])
def get_photo(photo_id):
	#return '<img src="http://whitsblog.com/wp-content/uploads/2013/05/Troll_Face.png" width="600px"></img>'
	photo = Photo.query.filter(Photo.id == photo_id).first()
	path = os.path.join('/home/xoul/smarteen-photo-contest/media/', photo.filename)
	print 'Photo : ' + path
	return send_file(path)