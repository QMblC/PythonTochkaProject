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
        location_id = request.json['location_id']
        DbHandler.SlotHandler.add_slots(master_id, location_id)
        return make_response(
            'Слоты созданы',
            200
            )
    except:
        return make_response(
            'Произошла непредвиденная ошибка',
            500
    )

@app.route('/api/delete-slots/', methods = ['DELETE'])
def delete_slots():
    try:
        master_id = request.json['master_id']
        DbHandler.SlotHandler.delete_slots(master_id)
        return make_response(
            'Слоты удалены',
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
    if len(people) > 0:

        DbHandler.SlotHandler.upgrade_time()

    for person in people:
        masters.append(DbHandler.SlotHandler.get_master_slots(person, dt))

    return masters

def upgrade_slots(dt: datetime):
    pass

@app.route('/api/get-slot-data/<int:slot_id>')
def get_slot_data(slot_id: int):
    slot = DbHandler.SlotHandler.get_slot(slot_id)
    location = DbHandler.LocationDbHandler.get_location(slot.location_id)
    string = "{0:02d}:{1:02d} {2:02d}.{3:02d}.{4}".format(slot.time.hour, slot.time.minute, slot.time.day, slot.time.month, slot.time.year)
    return {
        "location" : location.address,
        "master_id" : slot.master_id,
        "booked_by" : slot.booked_by,
        "time" : string
    }

    

@app.route('/api/get-dt/')
def get_dt():
    dt = TimeHandler.array_to_date(request.json["dt"])
    return {"year" : dt.year,
        "month" : dt.month,
        "day" : dt.day,
        "hour" : dt.hour,
        "minute" : dt.minute,
        "second" : dt.second}

@app.route('/api/book/<int:slot_id>', methods = ['GET','POST'])
def book_slot(slot_id: int):
    jwt = request.json['jwt']
    user_data_response = requests.get('http://127.0.0.1:2000/api/get-user-data/', json={'jwt' : jwt})
    user_data = user_data_response.json()
    slot = DbHandler.SlotHandler.get_slot(slot_id)

    slot.slot_type = "Забронировано"
    slot.booked_by = f"{user_data['first_name']} {user_data['last_name']} {user_data['id']}"

    DbHandler.SlotHandler.upgrade_slot(slot)

    return make_response(
        "OK",
        200
    )

if __name__ == '__main__':
    app.run(debug = True, port = 3000)