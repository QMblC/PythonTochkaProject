from flask import Flask, request, json, jsonify, make_response
import jwt, requests
from datetime import datetime, timedelta, timezone

from DbHandler import DbHandler
from DbModels import *
from App import app

#Проверять на админ или booked_by
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
            'id': user.id,
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

    if email == app.config['ADMIN_LOGIN']:
        DbHandler.UserHandler.create_user(first_name, last_name, email, password)
        user = DbHandler.UserHandler.get_user_by_email(email)
        token = jwt.encode({
            'id': user.id,
            'exp' : datetime.now(timezone.utc) + timedelta(minutes = 30)
        }, app.config['SECRET_KEY'], algorithm = 'HS256')
    
        decoded = jwt.decode(token, key = app.config['SECRET_KEY'], algorithms = 'HS256')
        DbHandler.AdminHandler.create_admin(user.id)
        return json.jsonify(token)

    DbHandler.UserHandler.create_user(first_name, last_name, email, password)
    user = DbHandler.UserHandler.get_user_by_email(email)
    token = jwt.encode({
            'id': user.id,
            'exp' : datetime.now(timezone.utc) + timedelta(minutes = 30)
        }, app.config['SECRET_KEY'], algorithm = 'HS256')
    
    decoded = jwt.decode(token, key = app.config['SECRET_KEY'], algorithms = 'HS256')

    return json.jsonify(token)

@app.route('/api/change-user-status/')

def change_user_status():

    new_status = request.json['status']
    user_id = request.json['user_id']

    user = DbHandler.UserHandler.get_user(user_id)

    if user == None:
        return make_response(
            'Пользователя не существует, или вы пытаетесь изменить статус администратора',
            400
        )
    

    if new_status == 'master':
        
        location_id = request.json['location_id']

        if DbHandler.MasterHandler.contains(user_id):
            return make_response(
                'Пользователь уже является парикмахером',
                500
            )
        DbHandler.MasterHandler.create_master(user.id, location_id)
        master = DbHandler.MasterHandler.get_master_by_global(user_id)

        masters = DbHandler.MasterHandler.get_master_by_location(location_id)

        response = requests.post('http://127.0.0.1:3000/api/create-clots/', json = {"master_id" : master.master_id, "location_id" : location_id})
        pass

    elif new_status == 'user':

        master_id = DbHandler.MasterHandler.delete_master(user_id)
        requests.delete('http://127.0.0.1:3000/api/delete-slots/', json = {"master_id" : master_id})

    elif new_status == 'admin':
        DbHandler.AdminHandler.create_admin(user_id)

@app.route('/api/get-masters/<int:location_id>')
def get_masters(location_id: int):
    users = []
    masters = DbHandler.MasterHandler.get_master_by_location(location_id)

    for i in range(len(masters)):
        user = DbHandler.UserHandler.get_user(masters[i].user_id)
        users.append({"master_id" : masters[i].master_id,
            "first_name" : user.first_name,
            "last_name" : user.last_name,
            "location_id" : location_id})

    return users

def decode_token(json_token: str) -> UserDb:
    js = jwt.decode(json_token, app.config['SECRET_KEY'], algorithms = 'HS256')
    user = DbHandler.UserHandler.get_user(int(js['id']))
    return user

@app.route('/api/get-booking-data/')#Fix??
def get_booking_data():
    json_token = request.json['jwt'][4:]
    master_id = request.json['master_id']
    try:
        user = decode_token(json_token)
        master = DbHandler.UserHandler.get_user(DbHandler.MasterHandler.get_master(master_id).user_id)

        response_data = user.toJSON()
        response_data['master'] = f"{master.first_name} {master.last_name}"

        if user != None:
            return make_response(response_data, 
                    200
            )
        else:
            return make_response(
                'Нет доступа',
                401
            )
    except:
        return make_response(
            'Некорректный токен',
            400
        )

def get_slot_user():
    json_token = request.json['jwt'][4:]
    try:
        user_json = decode_token(json_token).toJSON()

        master = DbHandler.UserHandler.get_user(DbHandler.MasterHandler.get_master(request.json['master_id']).user_id)

        user_json['master'] = f"{master.first_name} {master.last_name}"        

        return user_json
    except:
        return make_response(
            'Некорректный токен',
            400
        )


    
@app.route('/api/get-user-data/')
def get_jwt_user_data():
    json_token = request.json['jwt'][4:]
    try:
        user = decode_token(json_token).toJSON()
        return user
    except:
        return make_response(
            'Некорректный токен',
            400
        )

@app.route('/api/is-admin/')
def is_admin():
    admins = [admin.user_id for admin in DbHandler.AdminHandler.get_admins()]
    json_token = request.json['jwt'][4:]

    try:
        js = jwt.decode(json_token, app.config['SECRET_KEY'], algorithms = 'HS256')
        if js['id'] in admins:
            return make_response(
                'admin',
                200
            )
        else:
            return make_response(
                'Нет доступа',
                401
            )
    except:  
        return make_response(
            'Некорректный токен',
            400
        )


if __name__ == "__main__":
    app.run(debug=True, port=2000)
