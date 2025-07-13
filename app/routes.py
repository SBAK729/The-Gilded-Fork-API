from fastapi import APIRouter, Request
from pydantic import BaseModel
from app.chat import get_chat_response

router = APIRouter()

class ChatRequest(BaseModel):
    user_query: str

@router.post("/chat")
def chat(request: ChatRequest):
  question = request.user_query.strip()
  
  if not question:
        return {"error": "Question cannot be empty."}
  try:
        response = get_chat_response(question)
        print(response)
        return {"answer": response}
  except Exception as e:
        print(e)
        return {"error": "Something went wrong. Please try again."}
