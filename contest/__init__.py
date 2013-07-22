from flask import Flask, g
from contest.views.web import web
from database import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://MYSQL_ID:MYSQL_PW@localhost/smarteen'
# app.config['UPLOAD_FOLDER'] = '/home/xoul/smarteen-photo-contest/media/'
app.secret_key = 'It is fucking secret!'
app.register_module(web)
app.debug = True

db.init_app(app)
db.create_all(app=app)

print 'Static Folder : ' + app.static_folder

# 
# def create_all():
# 	context = app.test_request_context()
# 	context.push()
# 	db.create_all()
# 	context.pop()