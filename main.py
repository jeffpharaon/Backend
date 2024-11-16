# main.py

from fastapi import FastAPI, HTTPException
from sqlmodel import SQLModel, Field, Session, create_engine, select
from typing import List
from uuid import UUID
from fastapi.middleware.cors import CORSMiddleware

from models import Note  

app = FastAPI()

# Настройка CORS для разрешения запросов с фронтенда
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Создание базы данных SQLite
DATABASE_URL = "sqlite:///./notes.db"
engine = create_engine(DATABASE_URL, echo=True)

# Создание таблиц при запуске приложения
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

# Получение всех заметок
@app.get("/notes/", response_model=List[Note])
def read_notes():
    with Session(engine) as session:
        notes = session.exec(select(Note)).all()
        return notes

# Получение одной заметки по ID
@app.get("/notes/{note_id}", response_model=Note)
def read_note(note_id: UUID):
    with Session(engine) as session:
        note = session.get(Note, note_id)
        if not note:
            raise HTTPException(status_code=404, detail="Note not found")
        return note

# Создание новой заметки
@app.post("/notes/", response_model=Note)
def create_note(note: Note):
    with Session(engine) as session:
        session.add(note)
        session.commit()
        session.refresh(note)
        return note

# Обновление существующей заметки
@app.put("/notes/{note_id}", response_model=Note)
def update_note(note_id: UUID, updated_note: Note):
    with Session(engine) as session:
        note = session.get(Note, note_id)
        if not note:
            raise HTTPException(status_code=404, detail="Note not found")
        note.title = updated_note.title
        note.content = updated_note.content
        session.commit()
        session.refresh(note)
        return note

# Удаление заметки
@app.delete("/notes/{note_id}")
def delete_note(note_id: UUID):
    with Session(engine) as session:
        note = session.get(Note, note_id)
        if not note:
            raise HTTPException(status_code=404, detail="Note not found")
        session.delete(note)
        session.commit()
        return {"detail": "Note deleted"}
