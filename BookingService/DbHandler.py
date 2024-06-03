from App import db
from DbModels import SlotDb, MasterDb, LocationDb
from flask import json

from datetime import datetime, timezone

class DbHandler:
    
    class LocationDbHandler:
        @staticmethod
        def add_location(address: str):
            location = LocationDb(address = address)

            db.session.add(location)
            db.session.commit()

        @staticmethod
        def get_locations():
            array = []
            for i, value in enumerate(LocationDb.query.order_by(LocationDb.address).all()):
                array.append((value.id, value.address))

            return array
        
        @staticmethod
        def delete_location(id: int):
            location = LocationDb.query.get_or_404(id)

            db.session.delete(location)
            db.session.commit()

    class MasterHandler:
        @staticmethod
        def add_master(first_name: str, last_name: str, location_id: int):
            master = MasterDb(first_name = first_name, last_name = last_name, location_id = location_id)

            db.session.add(master)
            db.session.commit()

            master_id = MasterDb.query.all()[-1].id

            DbHandler.SlotHandler.add_slots(master_id)
        
        @staticmethod
        def get_master_by_location(id: int):
            return db.session.query(MasterDb).filter(MasterDb.location_id == int(id)).all()

    class SlotHandler:

        @staticmethod
        def get_master_slots(person, dt: datetime):

            a = db.session.query(SlotDb).filter(SlotDb.master_id == person['master_id']).all()

            person_slots = [{"id" : x.id, "type" : x.slot_type, "booked_by" : x.booked_by, "time" : x.time} for x in a if x.time.day == dt.day and x.time.month == dt.month]

            return person, person_slots
        
        @staticmethod
        def delete_slots(id):
            slots = db.session.query(SlotDb).filter(SlotDb.master_id == id).all()

            for slot in slots:
                db.session.delete(slot)

            db.session.commit()   
                

        @staticmethod
        def add_slots(master_id: int):
            dt = datetime.now(timezone.utc)
            start_dt = datetime(dt.year, dt.month, dt.day, 9, 0, 0)

            new_dt = start_dt
            for i in range(4):
                for j in range(7):
                    for k in range(22):
                        if k % 2 == 0:
                            hrs = 0
                        else:
                            hrs = 1
                        slot = SlotDb(master_id = master_id, booked_by = None, slot_type = "empty", time = new_dt)
                        db.session.add(slot)
                        new_dt = datetime(new_dt.year, new_dt.month, new_dt.day, new_dt.hour + hrs, (new_dt.minute + 30) % 60, new_dt.second)
                    if new_dt.day == new_dt.max.day:
                        if new_dt.month == 12:
                            new_dt = datetime(new_dt.year + 1, 1, 1, 9, 0, 0)
                        else:
                            new_dt = datetime(new_dt.year, new_dt.month + 1, 1, 9, 0, 0)
                    else:
                        try:
                            new_dt = datetime(new_dt.year, new_dt.month, new_dt.day + 1, 9, 0, 0)
                        except:
                            new_dt = datetime(new_dt.year, new_dt.month + 1, 1, 9, 0, 0)
                    
            db.session.commit()