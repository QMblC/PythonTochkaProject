from flask import Flask, request, json, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_jwt_extended import JWTManager


import os, jwt
from datetime import datetime, timedelta, timezone
from DbHandler import DbHandler
from App import app

#Проверять наличие почты

@app.route('/api/login/', methods = ['GET'])
def login():
    email = request.json['email']
    password = request.json['password']

    user = DbHandler.UserHandler.get_user_by_email(email)

    if not user:
        return make_response(
        'Could not verify',
        403,
        {'WWW-Authenticate' : 'Basic realm ="Неправильный логин или пароль"'})
    
    if user.is_password_correct(password):
        token = jwt.encode({
            'public_id': user.id,
            'exp' : datetime.now(timezone.utc) + timedelta(minutes = 30)
        }, app.config['SECRET_KEY'], algorithm = 'HS256')
        decoded = jwt.decode(token, key = app.config['SECRET_KEY'], algorithms = 'HS256')
        a = jsonify({"token" : token})
        return a
       
    
    else:
        return make_response(
        'Could not verify',
        403,
        {'WWW-Authenticate' : 'Basic realm ="Неправильный логин или пароль"'})

@app.route('/api/register/', methods = ['POST'])
def register():
    first_name = request.json['first_name']
    last_name = request.json['last_name']
    email = request.json['email']
    password = request.json['password']

    DbHandler.UserHandler.create_user(first_name, last_name, email, password)
    
    return 'a'

@app.route('/api/test/')
def test():
    if current_user.is_authenticated:
        return {"answer" : "yes"}
    return {"answer" : "no"}

@app.route('/api/logout/', methods = ['GET', 'POST'])
@login_required
def logout():
    logout_user()

if __name__ == "__main__":
    app.run(debug=True, port=2000)
