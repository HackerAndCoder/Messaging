from datetime import datetime
from fastapi import Depends
from typing import Optional, List
from sqlmodel import SQLModel, Field, Session, create_engine, select

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key = True)
    username: str = Field(index = True, unique = True)

class Chat(SQLModel, table = True):
    id: Optional[int] = Field(default = None, primary_key = True)
    title: str

class Message(SQLModel, table = True):
    id: Optional[int] = Field(default=None, primary_key = True)
    chat_id: int = Field(foreign_key = "chat.id", index = True)
    user_id: int = Field(foreign_key = "user.id", index = True)
    text: str
    created_at: datetime = Field(default_factory = datetime.utcfromtimestamp)

class Membership(SQLModel, table = True):
    chat_id: int = Field(foreign_key = "chat.id", primary_key = True)
    user_id: int = Field(foreign_key = "user.id", primary_key = True)

engine = create_engine("sqlite:///chat.db", connect_args={"check_same_thread": False})

def create_db():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as s:
        yield s

def create_user(username : str, s : Session = Depends(get_session)) -> User | None:
    if s.exec(select(User).where(User.username == username)).first():
        return None
    user = User(username = username)
    s.add(user)
    s.commit()
    s.refresh(user)
    return user

def create_chat(title : str, s : Session = Depends(get_session)) -> Chat:
    chat = Chat(title = title)
    s.add(chat)
    s.commit()
    s.refresh(chat)
    return chat

def get_user_chats(user_id : int, s : Session = Depends(get_session)):
    subq = select(Membership.chat_id).where(Membership.user_id == user_id)
    query = select(Chat).where(Chat.id.in_(subq))
    chats = s.exec(query).all()
    return chats

def send_message(chat_id : int, user_id : int, text : str, s : Session = Depends(get_session)) -> Message | None:
    m = s.exec(select(Membership).where(Membership.chat_id==chat_id, Membership.user_id==user_id)).first()
    if not m: return None
    message = Message(chat_id=chat_id, user_id = user_id, text = text)
    s.add(message)
    s.commit()
    s.refresh(message)
    return message

def list_messages(chat_id : int, s : Session = Depends(get_session)):
    q = select(Message).where(Message.chat_id == chat_id).order_by(Message.created_at.asc())
    return list(s.exec(q))