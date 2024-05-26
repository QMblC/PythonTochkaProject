from App import db, app

class LocationDb(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    address = db.Column(db.String(100), nullable = False)

    def __repr__(self) -> str:
        return '<Location %r>' % self.id
    
class MasterDb(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    location_id = db.Column(db.Integer, nullable = False)
    first_name = db.Column(db.String(50), nullable = False)
    last_name = db.Column(db.String(50), nullable = False)

    def __repr__(self):
        return '<Master %r>' % self.id
    
class SlotDb(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    master_id = db.Column(db.Integer, nullable = False)
    booked_by = db.Column(db.Integer)
    slot_type = db.Column(db.String(20), nullable = False)
    time = db.Column(db.DateTime, nullable = False)

    def __repr__(self):
        return '<Slot %r>' % self.id
    
with app.app_context():
    db.create_all()