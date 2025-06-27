import os
import json
import google.generativeai as genai
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Configure Gemini
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)

# Load prompts and context files
SYSTEM_PROMPT = Path("app/prompts/system_prompt.txt").read_text()
menu = json.loads(Path("app/prompts/menu.json").read_text())
hours = json.loads(Path("app/prompts/hours.json").read_text())
info = json.loads(Path("app/prompts/info.json").read_text())

async def get_chat_response(user_input: str) -> str:
    # Combine all context for the prompt
    full_context = f"""
{SYSTEM_PROMPT}

Here are the restaurant details:

Menu:
{json.dumps(menu, indent=2)}

Hours:
{json.dumps(hours, indent=2)}

Info:
{json.dumps(info, indent=2)}

Guest asked: {user_input}
"""

    # Initialize model
    model = genai.GenerativeModel("gemini-2.0-flash")

    # Start chat and send message
    chat = model.start_chat(history=[])
    response = chat.send_message(full_context)

    return response.text.strip()

