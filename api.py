from langchain_gigachat.chat_models import GigaChat
from chat import Chat
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8081",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Message(BaseModel):
    content: str

import getpass
import os
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

if "GIGACHAT_CREDENTIALS" not in os.environ:
    os.environ["GIGACHAT_CREDENTIALS"] = getpass.getpass("Credentials от GigaChat")

llm = GigaChat(
    temperature=0.1,
    max_tokens=1000,
    verify_ssl_certs=False,
    timeout=6000,
    model="GigaChat-Pro"
)
chats = {}



@app.post("/api/v1/ask/{grade}/{category}/{type}")
async def ask(grade: str, category: str, type: str, message: Message):
    if (grade, category, type) not in chats:
        chats[(grade, category, type)] = Chat(llm)
    result = await chats[(grade, category, type)](message.content)
    return {"message": "OK", "content": result}

@app.get("/api/v1/get_history/{grade}/{category}/{type}")
async def get_history(grade, category, type):
    try:
        result = {"message": chats[(grade, category, type)].messages}
    except:
        result = {"message": []}
    return result

@app.get("/api/v1/clear/{grade}/{category}/{type}")
async def clear(grade: str, category: str, type: str):
    try:
        chats[(grade, category, type)].clear()
        result = {"message": "history cleared"}
    except:
        result = {"message": "chat doesn't exist"}
    return result
    