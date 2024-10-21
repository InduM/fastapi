from fastapi import FastAPI
from sqlmodel import Field, Session, SQLModel, create_engine,select


class User(SQLModel,table = True):
    id: int | None = Field(default=None, primary_key=True)
    username:str
    fullname:str
    email:str 
    password:str

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

app = FastAPI()


@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/{name}")
async def read_user(name: str):
    return {"Hello": name}


@app.post("/users/")
def create_user(user: User):
    with Session(engine) as session:
        session.add(user)
        session.commit()
        session.refresh(user)
        return user


@app.get("/users/")
def read_users():
    with Session(engine) as session:
        users = session.exec(select(User)).all()
        return users