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

@app.route('/addresses/<int:id>/', methods = ['GET', 'POST'])
def view_location_page(id: int):

    if request == 'POST':
        dt = requests.get('http://127.0.0.1:3000/api/get-dt/', json = {"dt" : request.form["date"].split('.')}).json()
    else:
        dt = datetime.now(timezone.utc)

    days = requests.get('http://127.0.0.1:3000/api/timetable-day-options/', json = {"year" : dt.year,\
        "month" : dt.month, "day" : dt.day, "hour" : dt.hour, "minute": dt.minute, "second" : dt.second}).json()
    
    masters = requests.post(f'http://127.0.0.1:3000/api/get-master-slots/{id}', json = {"year" : dt.year,\
        "month" : dt.month, "day" : dt.day, "hour" : dt.hour, "minute": dt.minute, "second" : dt.second}).json()

    return render_template('location.html', masters = masters, days = days)

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
    
@app.route('/create-master/', methods = ['POST', 'GET'])
def create_master():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        location_id = request.form['location_id']

        try:
            
            requests.post('http://127.0.0.1:3000/api/create-master/', json = {"first_name" : first_name, "last_name" : last_name, "location_id" : location_id})
            return redirect('/addresses/')
        except:
            return "Возникла непредвиденная ошибка!"
    else:
        locations = requests.get('http://127.0.0.1:3000/api/get-locations/').json()
        return render_template("master_form.html", locations = locations)

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
                flash('Неверный логин или пароль')
        else:
            flash('Введите данные')

    return render_template("login.html")

@app.route('/register/', methods = ['GET', 'POST'])
def view_register_page():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        password1 = request.form['password']
        password2 = request.form['password2']
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

            return redirect('/login/')
    return render_template("register.html")

@app.route('/logout/')
def logout():
    requests.get('http://127.0.0.1:2000/api/logout/')
    return redirect('/')

@app.route('/test/')
def test():
    a = requests.get('http://127.0.0.1:2000/api/test/').json()
    return a['answer']


if __name__ == '__main__':
    app.run(debug = True, port = 4000)