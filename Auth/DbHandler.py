from App import db

from DbModels import UserDb, MasterDb, AdminDb

class DbHandler:

    class UserHandler:

        @staticmethod
        def get_user(id: int) -> UserDb:
            return db.session.query(UserDb).get(id)
        
        @staticmethod
        def get_users():
            return db.session.query(UserDb).all()
        
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
        def contains(user_id):
            potential_master = db.session.query(MasterDb).filter(MasterDb.user_id == user_id).first()
            return potential_master != None

        @staticmethod
        def get_master(master_id: int) -> MasterDb:
            a = db.session.query(MasterDb).get(master_id)
            return a
        
        def get_master_by_global(id: int):
            return db.session.query(MasterDb).filter(MasterDb.user_id == id).first()
        
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
        def delete_master(user_id: int):
            master = MasterDb.query.filter(user_id == MasterDb.user_id).first()

            master_id = master.master_id

            db.session.delete(master)
            db.session.commit()

            return master_id
        
    class AdminHandler:

        @staticmethod
        def create_admin(user_id: int):
            new_admin = AdminDb(user_id = user_id)

            db.session.add(new_admin)
            db.session.commit()

        @staticmethod
        def get_admins():
            admins = db.session.query(AdminDb).all()
            return admins