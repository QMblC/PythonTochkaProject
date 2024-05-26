from App import db, login_manager

from DbModels import UserDb, MasterDb, AdminDb

class DbHandler:

    class UserHandler:

        @staticmethod
        @login_manager.user_loader
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

            print(new_user.first_name, new_user.last_name, new_user.email, new_user.password)
