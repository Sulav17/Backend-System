from pydantic import BaseModel, EmailStr
from datetime import date, time

class InterviewBooking(BaseModel):
    full_name: str
    email: EmailStr
    date: date
    time: time
