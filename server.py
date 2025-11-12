import json, database
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],   # includes OPTIONS
    allow_headers=["*"],   # e.g. Content-Type, Authorization
)

class Message(BaseModel):
    message: str
    chat: int

class ChatRequest(BaseModel):
    chat: int

@app.on_event("startup")
def _startup(): database.create_db()

@app.get("/")
def root():
    return {"message": "error"}

@app.post("/send")
def message_send(msg : Message):
    print(msg)
    return {"response": "test"}

@app.post("/chat")
def get_chat(chat : ChatRequest):
    print(f"chat {chat}")
    return {"id": chat.chat, "messages": []}