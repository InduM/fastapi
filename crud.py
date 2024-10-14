#https://sqlmodel.tiangolo.com/tutorial/insert/#review-all-the-code
from sqlmodel import Field, Session, SQLModel, create_engine,select

class User(SQLModel,table = True):
    id: int 
    username:str
    fullname:str
    email:str 
    password:str

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def create_users():  
    user_1 = User(id =1,username="Abby",fullname="Abby ALison",email="abby@gmail.com",password="password")  
    user_2 = User(id=2,username="Pedro",fullname="Pedro Parqueador",email="pedro@gmail.com",password="password")
    user_3 = User(id=3,username="Tommy",fullname="Tommy Sharp",email="tommy@gmail.com" ,password="password")

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
    
def update_users():
    with Session(engine) as session:
        statement = select(User).where(User.username == "Abby")
        results = session.exec(statement)
        user = results.one()
        print("Hero:", user)

        user.password = "Password12"
        session.add(user)
        session.commit()
        session.refresh(user)
        print("Updated user:", user)


def delete_users():
    with Session(engine) as session:
        statement = select(User).where(User.username == "Abby")
        results = session.exec(statement)
        user = results.one()
        print("User: ", user)

        session.delete(user)
        session.commit()


def main():  
    create_db_and_tables()  
    create_users()  
    select_users()
    update_users()


if __name__ == "__main__":  
    main()