from App import db

from DbModels import UserDb, MasterDb, AdminDb

class DbHandler:

    class UserHandler:

        @staticmethod
        def get_user(id: int):
            return db.session.query(UserDb).get(id)
        
        @staticmethod
        def get_user_by_email(email: str):
            return db.session.query(UserDb).filter(UserDb.email == email).first()
        
        @staticmethod
        def create_user(first_name: str, last_name: str, email: str, password: str):
            new_user = UserDb(first_name = first_name, last_name = last_name, email = email)
            new_user.set_password(password)

            db.session.add(new_user)
            db.session.commit()

        @staticmethod
        def delete_user(id):
            user = UserDb.query.get_or_404(id)

            db.session.delete(user)
            db.session.commit()

    class MasterHandler:
        @staticmethod
        def get_master(id: int) -> MasterDb:
            return db.session.query(MasterDb).get(id)
        
        @staticmethod
        def get_master_by_email(email: str):
            return db.session.query(UserDb).filter(UserDb.email == email).first()
        
        @staticmethod
        def get_master_by_location(location_id: int):
            masters = db.session.query(MasterDb).filter(MasterDb.location_id == int(location_id)).all()
            return masters
        
        @staticmethod
        def create_master(user_id: int, location_id: int):
            new_master = MasterDb(user_id = user_id,
                location_id = location_id)
            
            db.session.add(new_master)
            db.session.commit()

        @staticmethod
        def delete_master(id: int):
            master = MasterDb.query.get_or_404(id)

            db.session.delete(master)
            db.session.commit()
