# -*- coding: utf8 -*-

from database import db
from datetime import datetime

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(40), nullable=False)
 	facebook_id = db.Column(db.String(20), unique=True, nullable=False)
 	facebook_token = db.Column(db.String(160), unique=True, nullable=False)
	
	def __init__(self, name, facebook_id, facebook_token):
		self.name = name
 		self.facebook_id = facebook_id
 		self.facebook_token = facebook_token
		
	def __repr__(self):
		return '<User %r>' % (self.name)

class Photo(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(120))
	description = db.Column(db.Text)
	filename = db.Column(db.String(200))
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	user = db.relationship('User', backref=db.backref('user', lazy='dynamic'))
	date = db.Column(db.DateTime)

	def __init__(self, title, description, user, date=None):
		self.title = title
		self.description = description
		self.user = user
		if date is None:
			date = datetime.utcnow()
		self.date = date
	
	def __repr__(self):
		return '<Photo %r>' % (self.title)
		
	def url(self):
		return 'http://xoul.kr/smarteen-photo-contest/photo/%d' % (self.id)