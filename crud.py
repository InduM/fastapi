from sqlmodel import Field, Session, SQLModel, create_engine,select
from datetime import datetime

import hashlib
#IntegrityError (sqlite3.IntegrityError) UNIQUE constraint failed: user.id
#MultipleResultsFound: Multiple rows were found when exactly one was required

def hash_password(password):
   password_bytes = password.encode('utf-8')
   hash_object = hashlib.sha256(password_bytes)
   return hash_object.hexdigest()


class User(SQLModel,table = True):
    id: int | None = Field(default=None, primary_key=True)
    username:str
    fullname:str
    email:str 
    password:str
    created_at : datetime = Field(default_factory=datetime.utcnow, nullable=False)

class User_Activity(SQLModel,table = True):
        id: int | None = Field(default=None, primary_key=True)
        login: datetime | None =Field(default=None)
        logout_time : datetime| None = Field(default=None)

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True)

def create_user_activity(id):
    userActivity = User_Activity(id = id,login = datetime.now(),logout_time = datetime.now())
    with Session(engine) as session:  
        session.add(userActivity) 
        session.commit()  


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def create_users():  
    user_1 = User(id =1,username="Abby",fullname="Abby ALison",email="abby@gmail.com",password=hash_password("password") ,created_at = datetime.now() )
    user_2 = User(id=2,username="Pedro",fullname="Pedro Parqueador",email="pedro@gmail.com",password=hash_password("password"),created_at = datetime.now())
    user_3 = User(id=3,username="Tommy",fullname="Tommy Sharp",email="tommy@gmail.com" ,password=hash_password("password"),created_at = datetime.now())

    create_user_activity(user_1.id)
    create_user_activity(user_2.id)
    create_user_activity(user_3.id)
    with Session(engine) as session:  
        session.add(user_1)  
        session.add(user_2)
        session.add(user_3)

        session.commit()  
    
def select_users():
    with Session(engine) as session:  
        statement = select(User)  
        results = session.exec(statement)  
        for user in results:  
            print(user)  
    
def update_users(username,password):
    with Session(engine) as session:
        statement = select(User).where(User.username == username)
        results = session.exec(statement)
        user = results.one()
        print("User:", user)

        user.password = hash_password(password)
        session.add(user)
        session.commit()
        session.refresh(user)
        print("Updated user:", user)



def delete_users(username):
    with Session(engine) as session:
        statement = select(User).where(User.username == username)
        results = session.exec(statement)
        user = results.one()
        print("User: ", user)

        session.delete(user)
        session.commit()


def update_user_logout_time(id):
    with Session(engine) as session:
        statement = select(User_Activity).where(User.id == id)
        results = session.exec(statement)
        user = results.one()

        user.logout_time = datetime.now()
        session.add(user)
        session.commit()
        session.refresh(user)
        print("Updated user:", user)


def update_user_login_time(id):
    with Session(engine) as session:
        statement = select(User_Activity).where(User_Activity.id == id)
        results = session.exec(statement)
        user = results.one()

        user.login = datetime.now()
        session.add(user)
        session.commit()
        session.refresh(user)
        print("Updated user:", user)


def login_user(id, password) -> bool:
    with Session(engine) as session:
        statement = select(User).where(User.id == id).where( User.password == hash_password(password))
        results = session.exec(statement)
        user = results.one_or_none()

        print (f"Login {'success' if user else 'failed'}")
        if user:
            update_user_login_time(id)
        return user or False

def logout_user(id):
    with Session(engine) as session:
        update_user_logout_time(id)
        




def main():  
    create_db_and_tables()  
    create_users()  
    select_users()
    update_users()


if __name__ == "__main__":  
    main()