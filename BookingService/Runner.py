from App import app
from flask import request, redirect, json, Response, make_response
from DbHandler import DbHandler
from TimeHandler import TimeHandler
import requests
from datetime import datetime, timezone

@app.route('/api/create-location/', methods = ['POST'])
def create_location():
    a = request.json
    DbHandler.LocationDbHandler.add_location(request.json['address'])

@app.route('/api/get-locations/')
def get_locations():
     locations = DbHandler.LocationDbHandler.get_locations()
     return locations

@app.route('/api/delete-location/', methods = ['DELETE'])
def delete_location():
    DbHandler.LocationDbHandler.delete_location(request.json["value"])

@app.route('/api/timetable-day-options/')
def get_next_two_weeks():
    days = TimeHandler.get_next_two_weeks()
    js = request.json
    dt = datetime(js["year"], js["month"], js["day"], js["hour"], js["minute"], js["second"])
    for id, day_info in enumerate(days):
        days[0], days[id] = days[id], days[0]
        if day_info[1] == "{0:02d}.{1:02d}.{2}".format(dt.day, dt.month, dt.year):       
            break

    return days

@app.route('/api/create-master/', methods = ['POST'])
def create_master():
    
    DbHandler.MasterHandler.add_master(request.json["first_name"], request.json["last_name"], request.json["location_id"])

    return "a"

@app.route('/api/create-clots/', methods = ['POST'])
def create_slots():
    try:
        master_id = request.json['master_id']
        DbHandler.SlotHandler.add_slots(master_id)
        return make_response(
            'Слоты созданы',
            200
            )
    except:
        return make_response(
            'Произошла непредвиденная ошибка',
            500
    )

@app.route('/api/get-slots/', methods = ['POST', 'GET'])
def get_master_slots():
    js = request.json
    dt = datetime(js["year"], js["month"], js["day"], js["hour"], js["minute"], js["second"])

    masters = []

    people = js['masters']

    for person in people:
        masters.append(DbHandler.SlotHandler.get_master_slots(person, dt))

    return masters

@app.route('/api/get-dt/')
def get_dt():
    return TimeHandler.array_to_date(request.json["dt"])

if __name__ == '__main__':
    app.run(debug = True, port = 3000)