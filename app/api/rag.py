from fastapi import APIRouter, HTTPException
from app.models.interview import InterviewBooking
from app.services.email_service import send_email
from app.services.rag_agent import get_rag_agent

router = APIRouter()


@router.post("/rag/query")
async def rag_query(query: str, user_id: str = "default"):
    try:
        agent = get_rag_agent(user_id)
        result = agent.run(query)
        return {"response": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/rag/book-interview")
async def book_interview(data: InterviewBooking):
    # Store info (you can expand with DB later)
    try:
        subject = "Interview Confirmation"
        content = (
            f"Dear {data.full_name},\n\n"
            f"Your interview has been scheduled on {data.date} at {data.time}.\n"
            f"We'll contact you shortly.\n\nRegards,\nPalm Mind Technology"
        )
        send_email(data.email, subject, content)
        return {"status": "Interview booked and email sent"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
