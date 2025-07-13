from app.rag_pipeline import get_rag_response

def get_chat_response(query: str) -> str:
    response = get_rag_response(query)

    return response
