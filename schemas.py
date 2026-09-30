from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class TicketCreate(BaseModel):
    student_id: str
    full_name: str
    email: str
    study_mode: str
    category: str
    subject: str
    description: str
    priority: Optional[str] = "Medium"

class TicketUpdate(BaseModel):
    status: str
    admin_notes: Optional[str] = None

class TicketResponse(BaseModel):
    ticket_id: str
    student_id: str
    category: str
    subject: str
    description: str
    priority: str
    status: str
    admin_notes: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True