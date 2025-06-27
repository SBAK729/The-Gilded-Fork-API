from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from app.chat import get_chat_response
import os

load_dotenv()

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    question = data.get("question", "").strip()

    if not question:
        return {"error": "Question cannot be empty."}

    try:
        response = await get_chat_response(question)
        return {"answer": response}
    except Exception as e:
        return {"error": "Something went wrong. Please try again."}
