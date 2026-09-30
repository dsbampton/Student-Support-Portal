import datetime
import random
import string
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from database import Base

def generate_ticket_id():
    digits = ''.join(random.choices(string.digits, k=4))
    return f"NIT-{digits}"

class Student(Base):
    __tablename__ = "students"

    student_id = Column(String, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    study_mode = Column(String, nullable=False)

    tickets = relationship("Ticket", back_populates="owner")

class Ticket(Base):
    __tablename__ = "tickets"

    ticket_id = Column(String, primary_key=True, default=generate_ticket_id, index=True)
    student_id = Column(String, ForeignKey("students.student_id"), nullable=False)
    category = Column(String, nullable=False)
    subject = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    priority = Column(String, default="Medium")
    status = Column(String, default="Pending")
    admin_notes = Column(Text, default="Ticket received. Awaiting review.")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    owner = relationship("Student", back_populates="tickets")