from flask import Flask, request, json, jsonify, make_response
import jwt
from datetime import datetime, timedelta, timezone

from DbHandler import DbHandler
from App import app

#Проверять наличие почты

@app.route('/api/login/', methods = ['GET', 'POST'])
def login():
    
    email = json.loads(request.data)['email']
    password = json.loads(request.data)['password']

    user = DbHandler.UserHandler.get_user_by_email(email)

    if not user:
        return make_response(
        'Could not verify',
        403,
        )
    
    if user.is_password_correct(password):
        token = jwt.encode({
            'public_id': user.id,
            'exp' : datetime.now(timezone.utc) + timedelta(minutes = 30)
        }, app.config['SECRET_KEY'], algorithm = 'HS256')
        decoded = jwt.decode(token, key = app.config['SECRET_KEY'], algorithms = 'HS256')

        return json.jsonify(token)
       
    
    else:
        return make_response(
        'Неверный логин или пароль',
        403)

@app.route('/api/register/', methods = ['POST'])
def register():
    first_name = request.json['first_name']
    last_name = request.json['last_name']
    email = request.json['email']
    password = request.json['password']

    user = DbHandler.UserHandler.get_user_by_email(email)
    if user:
        make_response(
            'Указанная почта уже используется',
            400
        )

    DbHandler.UserHandler.create_user(first_name, last_name, email, password)
    user = DbHandler.UserHandler.get_user_by_email(email)
    token = jwt.encode({
            'public_id': user.id,
            'exp' : datetime.now(timezone.utc) + timedelta(minutes = 30)
        }, app.config['SECRET_KEY'], algorithm = 'HS256')
    
    decoded = jwt.decode(token, key = app.config['SECRET_KEY'], algorithms = 'HS256')

    return json.jsonify(token)

@app.route('/api/logout/', methods = ['GET', 'POST'])
def logout():
    pass

if __name__ == "__main__":
    app.run(debug=True, port=2000)
