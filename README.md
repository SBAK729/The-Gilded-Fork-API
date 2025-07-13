# The Gilded Fork API 🍴

A restaurant chatbot API powered by **Groq's Llama 3 70B** for ultra-fast inference, with Pinecone vector search for context-aware responses.

## Features ✨

- **LLM Backend**: Groq's `llama3-70b-8192` model (300+ tokens/sec)
- **Vector Database**: Pinecone for semantic search
- **RAG Pipeline**: Retrieval-Augmented Generation for accurate responses
- **FastAPI**: REST API endpoint for chatbot queries

## Tech Stack 🛠️

| Component       | Technology                         |
| --------------- | ---------------------------------- |
| LLM             | Groq (Llama 3 70B)                 |
| Vector Database | Pinecone                           |
| Embeddings      | Hugging Face Sentence Transformers |
| API Framework   | FastAPI                            |
| Language        | Python 3.10                        |

## Setup Instructions 🚀

### Prerequisites

- Python 3.10+
- [Groq API Key](https://console.groq.com/keys)
- [Pinecone API Key](https://www.pinecone.io/)
- [HuggingFace Account](https://huggingface.co/)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/The-Gilded-Fork-API.git
   cd The-Gilded-Fork-API
   ```

## Installation & Setup 🛠️

### Step 2: Environment Setup

1. **Create & activate virtual environment**
   ```bash
   python -m venv venv
   # Linux/Mac:
   source venv/bin/activate
   # Windows:
   .\venv\Scripts\activate
   ```
2. **Create and activate virtual environment:**
   ```bash
    python -m venv cafe
    source cafe/bin/activate  # Linux/Mac
    cafe\Scripts\activate    # Windows
   ```
3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Create .env file:**
   ```bash
    PINECONE_API_KEY=your_pinecone_key
    GROQ_API_KEY=your_groq_key
   ```

# Running the API

    ```bash
    uvicorn app.main:app --reload
    ```
