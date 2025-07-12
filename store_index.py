from src.helper import load_txt, text_split, download_hugging_face_embeddings
from langchain_community.vectorstores import Pinecone as LangchainPinecone
from pinecone import Pinecone
from pinecone import ServerlessSpec
from dotenv import load_dotenv
from uuid import uuid4
import os

load_dotenv()

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")

# Load and process your data
extracted_data = load_txt("data/")
text_chunks = text_split(extracted_data)
# print(text_chunks)
embeddings = download_hugging_face_embeddings()

# Initialize Pinecone client
pc = Pinecone(api_key=PINECONE_API_KEY)

index_name = "restaurant-chatbot"

# Create index if not exists
if index_name not in pc.list_indexes().names():
    pc.create_index(
        name=index_name,
        dimension=384,  
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region="us-east-1"),
    )

index = pc.Index(index_name)

# Prepare and upsert vectors
docsearch = LangchainPinecone.from_documents(text_chunks, embedding=embeddings, index_name=index_name)
