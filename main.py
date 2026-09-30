from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import List

import models
import schemas
from database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Student Support Portal API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return FileResponse("index.html")

@app.post("/tickets", response_model=schemas.TicketResponse, status_code=status.HTTP_201_CREATED)
def create_ticket(ticket_data: schemas.TicketCreate, db: Session = Depends(get_db)):
    student = db.query(models.Student).filter(models.Student.student_id == ticket_data.student_id).first()
    
    if not student:
        student = models.Student(
            student_id=ticket_data.student_id,
            full_name=ticket_data.full_name,
            email=ticket_data.email,
            study_mode=ticket_data.study_mode
        )
        db.add(student)
        db.commit()
        db.refresh(student)

    new_ticket = models.Ticket(
        student_id=ticket_data.student_id,
        category=ticket_data.category,
        subject=ticket_data.subject,
        description=ticket_data.description,
        priority=ticket_data.priority
    )
    
    db.add(new_ticket)
    db.commit()
    db.refresh(new_ticket)
    return new_ticket

@app.get("/tickets/track/{ticket_id}", response_model=schemas.TicketResponse)
def track_ticket(ticket_id: str, db: Session = Depends(get_db)):
    ticket = db.query(models.Ticket).filter(models.Ticket.ticket_id == ticket_id.upper()).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket ID not found")
    return ticket

@app.get("/tickets/student/{student_id}", response_model=List[schemas.TicketResponse])
def get_student_tickets(student_id: str, db: Session = Depends(get_db)):
    tickets = db.query(models.Ticket).filter(models.Ticket.student_id == student_id).all()
    return tickets

@app.get("/admin/tickets", response_model=List[schemas.TicketResponse])
def get_all_tickets(db: Session = Depends(get_db)):
    return db.query(models.Ticket).all()

@app.patch("/admin/tickets/{ticket_id}", response_model=schemas.TicketResponse)
def update_ticket_status(ticket_id: str, update_data: schemas.TicketUpdate, db: Session = Depends(get_db)):
    ticket = db.query(models.Ticket).filter(models.Ticket.ticket_id == ticket_id.upper()).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket ID not found")
    
    ticket.status = update_data.status
    if update_data.admin_notes:
        ticket.admin_notes = update_data.admin_notes
        
    db.commit()
    db.refresh(ticket)
    return ticket