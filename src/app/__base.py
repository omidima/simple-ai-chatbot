
import os
from openai import AsyncOpenAI
import chainlit as cl
from chainlit.data.sql_alchemy import SQLAlchemyDataLayer

from src.utils.password_hasher import hash_password


client = AsyncOpenAI(base_url="http://g4f:1337/v1", api_key="lm-studio")

cl.instrument_openai()

settings = {"model": "gpt-4o-mini", "temperature": 0}

db_conn = None

DATABASE_URL = os.environ["DATABASE_URL"]

@cl.data_layer
def get_data_layer():
    global db_conn
    db_conn =  SQLAlchemyDataLayer(conninfo=DATABASE_URL)
    return db_conn
    
@cl.password_auth_callback
async def auth_callback(username: str, password: str):
    if (username, password):
        user = await db_conn.execute_sql(f"SELECT * FROM app_users WHERE username = '{username}'", [])
        if user and (len(user) > 0 )and(user[0]["password"] == hash_password(password)):
            return cl.User(
                identifier=username, metadata={"role": "admin", "provider": "credentials"}
            )
        
    return None

COMMANDS = []