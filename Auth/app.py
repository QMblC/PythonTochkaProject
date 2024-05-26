from flask import Flask, request, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user
import os


app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///auth.db'
app.config['SQLALCHEMY_TRACK_MODIFICTATIONS'] = False
app.secret_key = b's5DASsc@1sv$[a[c]]'

db = SQLAlchemy(app)
login_manager = LoginManager(app)

