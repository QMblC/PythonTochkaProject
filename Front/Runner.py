from flask import Flask, render_template, request, redirect, json, flash, make_response
import requests
from datetime import datetime, timezone
from flask_login import login_user
from flask_jwt_extended import JWTManager

app = Flask(__name__)
app.secret_key = 'kdksa13ladjl'

@app.route('/')
def view_main_page():
    return render_template("index.html")

@app.route('/addresses/')
def view_addresses():
    locations = requests.get('http://127.0.0.1:3000/api/get-locations/').json()
    return render_template("addresses.html", locations = locations)

@app.route('/api/get-addresses/')
def get_addresses():
    return requests.get('http://127.0.0.1:3000/api/get-locations/').json()

@app.route('/addresses/<int:location_id>/', methods = ['GET', 'POST'])
def view_location_page(location_id: int):

    if request.method == 'POST':
        dt_json = requests.get('http://127.0.0.1:3000/api/get-dt/', json = {"dt" : request.form["date"].split('.')}).json()
        dt = datetime(dt_json['year'], dt_json['month'], dt_json['day'], dt_json['hour'], dt_json['minute'], dt_json['second'])
    else:
        dt = datetime.now(timezone.utc)

    days = requests.get('http://127.0.0.1:3000/api/timetable-day-options/', json = {"year" : dt.year,
        "month" : dt.month, "day" : dt.day, "hour" : dt.hour, "minute": dt.minute, "second" : dt.second}).json()
    
    #Получение мастеров-людей
    #Получение слотов

    masters = requests.get(f'http://127.0.0.1:2000/api/get-masters/{location_id}').json()

    slots = requests.get('http://127.0.0.1:3000/api/get-slots/', json={"masters" : masters,
        "year" : dt.year,
        "month" : dt.month,
        "day" : dt.day,
        "hour" : dt.hour, 
        "minute": dt.minute, 
        "second" : dt.second}).json()

    return render_template('location.html', masters = slots, days = days)

@app.route('/create-location/', methods = ['POST', 'GET'])
def view_create_location():
    if request.method == 'POST':
        address = request.form['address']

        try:
            requests.post('http://127.0.0.1:3000/api/create-location/', json = {"address" : address})
            return redirect('/addresses/')
        except:
            return "error"
    else:
        return render_template("location_form.html")

@app.route('/addresses/delete/<int:id>')
def delete(id: int):

    try:
        requests.delete('http://127.0.0.1:3000/api/delete-location/', json = {"value" : id})
        return redirect('/addresses/')
    except:
        return 'При удалении  произошла ошибка!'



@app.route('/login/', methods = ['GET', 'POST'])
def view_login_page():

    if request.method == 'POST':
        email = json.loads(request.data)['email']
        password = json.loads(request.data)['password']

        if email and password:
            response = requests.get('http://127.0.0.1:2000/api/login/', json = {"email" : email, "password" : password})
            
            if response.status_code == 200:
                text = response.text[1:-2]
                return text
            else:
                return make_response(
                    'Enter data',
                    403
                )
        else:
            return make_response(
                'Login or password is incorrect',
                400,
            )

    return render_template("login.html")

@app.route('/register/', methods = ['GET', 'POST'])
def view_register_page():
    if request.method == 'POST':
        first_name = request.json['first_name']
        last_name = request.json['last_name']
        email = request.json['email']
        password1 = request.json['password']
        password2 = request.json['password2']
        if not (first_name and last_name and email and password1 and password2):
            flash("Введите все данные")
        elif password1 != password2:
            flash("Пароли не совпадают")
        else:
            response = requests.post('http://127.0.0.1:2000/api/register/', json = {
                "first_name" : first_name,
                "last_name" : last_name,
                "email" : email,
                "password" : password1,
            })

            if response.status_code == 200:
                text = response.text[1:-2]
                return text
            else:
                return make_response(
                    'Enter data',
                    403
                )
    return render_template("register.html")

@app.route('/logout/')
def logout():
    requests.get('http://127.0.0.1:2000/api/logout/')
    return redirect('/')

@app.route('/change-status/')
def view_status_page():
    locations = requests.get('http://127.0.0.1:3000/api/get-locations/')
    return render_template("change_user_status.html", locations = locations.json())

@app.route('/api/change-status/', methods = ['POST'])
def change_status():
    user_id = request.json['user_id']
    status = request.json['status']
    location_id = request.json['location_id']

    requests.get('http://127.0.0.1:2000/api/change-user-status/', json = {"user_id" : user_id,
        "status" : status,
        "location_id" : location_id})

@app.route('/api/validate/', methods = ['POST'])
def validate():
    jwt =request.json['jwt']
    response = requests.get('http://127.0.0.1:2000/api/is-admin/', json={"jwt" : jwt})
    if response.status_code == 200:
        return json.jsonify(200)
    else:
        return json.jsonify(401)
    
@app.route('/booking/<int:slot_id>/')
def view_booking_page(slot_id: int):

    return render_template('booking.html', slot_id = slot_id)

@app.route('/api/get-booking-data/<int:slot_id>/', methods = ['GET', 'POST'])
def get_booking_data(slot_id: int):
    jwt = request.json['jwt']

    #найти инфу о пользователе
    #найти инфу о мастере
    #найти инфу о дате

    
    slot_response = requests.get(f'http://127.0.0.1:3000/api/get-slot-data/{slot_id}')
    slot = slot_response.json()
    booking_data = requests.get('http://127.0.0.1:2000/api/get-booking-data/', json = {"jwt" : jwt, "master_id" : slot['master_id']})
    if booking_data.status_code != 200:
        return make_response(
            "Error",
            403
        )
    data = booking_data.json()

    return {
        "firstName" : data['first_name'],
        "lastName" : data['last_name'],
        "masterName" : data['master'],
        "address" : slot['location'],
        "time" : slot["time"],
        "price" : 200
    }

@app.route('/payment/<int:slot_id>/')
def view_payment_page(slot_id: int):
    return render_template("payment.html")

@app.route('/api/pay/<int:slot_id>', methods = ['GET', 'POST'])
def pay(slot_id: int):
    jwt = request.json['jwt']
    requests.post(f'http://127.0.0.1:3000/api/book/{slot_id}', json={"slot_id" : slot_id, "jwt" : jwt})
    return redirect('/addresses/')

@app.route('/slot-info/<int:slot_id>/')
def view_slot_info_page(slot_id: int):
    return render_template('slot-info.html')

@app.route('/api/get-slot-info/<int:slot_id>', methods = ['GET', 'POST'])
def get_slot_info(slot_id: int):
    jwt = request.json['jwt']
    slot_response = requests.get(f'http://127.0.0.1:3000/api/get-slot-data/{slot_id}')
    slot = slot_response.json()
    slot_user_data_response = requests.get('http://127.0.0.1:2000/api/get-booking-data/', json={'jwt' : jwt, "master_id" : slot['master_id'] })
    slot_user_data = slot_user_data_response.json()

    admins = [3]

    if int(slot['booked_by'].split()[-1]) == slot_user_data['id'] or slot_user_data['id'] in admins:

        return make_response( {
            "firstName" : slot_user_data['first_name'],
            "lastName" : slot_user_data['last_name'],
            "master" : slot_user_data['master'],
            "time" : slot['time']
            },
            200
        )
    
    else:
        make_response(
            403
        )
if __name__ == '__main__':
    app.run(debug = True, port = 4000)