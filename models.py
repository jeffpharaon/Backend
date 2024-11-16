from sqlmodel import SQLModel, Field
from typing import Optional
from uuid import UUID, uuid4

class Note(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    title: str
    content: Optional[str] = ""
