from flask import Flask
import os
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)

#Configuring app settings for db and initializing db instance
basedir = os.path.abspath(os.path.dirname(__file__))
#Set database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir,'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
db = SQLAlchemy(app)