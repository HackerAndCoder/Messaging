import json, database
from database import User, Chat, Message
from fastapi import Depends, FastAPI
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

class MessageSendRequest(BaseModel):
    text : str
    chat_id : int

class ChatCreateRequest(BaseModel):
    title : str


@app.on_event("startup")
def _startup(): 
    database.create_db()

@app.get("/")
def root():
    return {"message": "error"}

@app.post("/send")
def message_send(msg : MessageSendRequest):
    print(msg)
    return {"response": "test"}

@app.post("/request-chat")
def get_chat(chat_id : int):
    print(f"chat {chat_id}")
    return {"id": chat_id, "messages": []}

@app.post("/create-chat")
def create_chat(chat : ChatCreateRequest):
    print(f"{chat}")
    return {}

# NO AUTH FOR NOW
@app.post("/get-user")
def get_user(username : str, s : database.Session = Depends(database.get_session)):
    # TEST
    
    database.create_user("test", s)
    
    user = database.get_user(username, s)
    if not user:
        return {"error": "No user found"}
    return user

