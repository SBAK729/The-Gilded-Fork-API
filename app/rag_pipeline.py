from langchain_groq import ChatGroq 
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from pinecone import Pinecone, ServerlessSpec
from langchain_pinecone import PineconeVectorStore
from src.helper import download_hugging_face_embeddings
from src.prompt import bruno_prompt
from dotenv import load_dotenv
import os

# Load .env variables
load_dotenv()
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")  # Add this to your .env

# Download embeddings (unchanged)
embeddings = download_hugging_face_embeddings()

# Initialize Pinecone
pc = Pinecone(api_key=PINECONE_API_KEY)
index_name = "restaurant-chatbot"

if index_name not in pc.list_indexes().names():
    pc.create_index(
        name=index_name,
        dimension=384,
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region="us-east-1"),
    )

index = pc.Index(index_name)
docsearch = PineconeVectorStore(index=index, embedding=embeddings)

# Load prompt template (unchanged)
prompt = PromptTemplate(template=bruno_prompt, input_variables=["context", "question"])
chain_type_kwargs = {"prompt": prompt}

# Initialize Groq (replaces HuggingFaceEndpoint)
llm = ChatGroq(
    groq_api_key=GROQ_API_KEY,
    model_name="llama3-70b-8192",  # New Llama 3 70B (recommended)
    # model_name="llama2-70b-4096",  # Older version (if still available)
    # model_name="mixtral-8x7b-32768",  # Alternative: Mixtral MoE
    temperature=0.1,
    max_tokens=512
)

# Set up QA chain (unchanged)
qa = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=docsearch.as_retriever(search_kwargs={'k': 2}),
    return_source_documents=True,
    chain_type_kwargs=chain_type_kwargs
)

def get_rag_response(query: str) -> str:
    try:
        response = qa.invoke({"query": query})
        return response["result"]
    except Exception as e:
        print(f"Error: {e}")
        return "Sorry, something went wrong."