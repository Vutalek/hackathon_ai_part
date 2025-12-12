from langchain_gigachat.chat_models import GigaChat
from chat import Chat
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


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
chat = Chat(llm)



@app.post("/ask")
async def ask(message: Message):
    result = chat(message.content)
    return {"message": "OK", "content": result}

@app.get("/get_history")
async def get_history():
    return {"message": chat.messages}

@app.get("/clear")
async def clear():
    chat.clear()
    return {"message": "history cleared"}