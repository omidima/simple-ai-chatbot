import uuid
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from chainlit.utils import mount_chainlit
from pydantic import BaseModel
from src.app.__base import get_data_layer
from src.utils.password_hasher import hash_password
from src.app.database import AppUsers, Base, engine, get_db
from sqlalchemy.orm import Session

app = FastAPI()

@app.on_event("startup")
async def startup():
    # Init database and tables
    Base.metadata.create_all(bind=engine)
    get_data_layer()

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:4173",
    "http://192.168.1.6:4173",
    "http://192.168.1.6",
    "http://0.0.0.0",
    "http://0.0.0.0:4173",
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class UserInfo(BaseModel):
    username: str
    password: str
    confirmPassword: str


@app.post("/client/signup")
async def signup_users(data: UserInfo, db: Session = Depends(get_db)):
    print("Received data for signup:", data)

    # Generate a new UUID for the user ID
    user_id = str(uuid.uuid4())

    # Secure password hashing (using bcrypt as an example)
    hashed_password = hash_password(data.password)

    # SQL query with parameterized input to prevent SQL injection
    query = """
    INSERT INTO app_users (id, identifier, username, password)
    VALUES ($1, 'admin', $2, $3)
    """

    db.add(AppUsers(username=data.username, password=hashed_password, id=user_id))
    db.commit()

    return {"message": "OK"}


mount_chainlit(app=app, target="src/app/__init__.py", path="/api")
