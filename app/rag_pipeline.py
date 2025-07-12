from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
from src.helper import download_hugging_face_embeddings
import pinecone
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from dotenv import load_dotenv
from src.prompt import bruno_prompt
import os

from pinecone import ServerlessSpec
from langchain_pinecone import PineconeVectorStore
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain_huggingface import HuggingFacePipeline
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate



# Load .env variables
load_dotenv()
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_API_ENV = os.environ.get('PINECONE_API_ENV')
HUGGINGFACEHUB_API_TOKEN = os.getenv("HUGGINGFACEHUB_API_TOKEN") 

# download embedding model
embeddings = download_hugging_face_embeddings()


# 2. Initialize Pinecone v3 client
pc = pinecone.init(api_key=PINECONE_API_KEY,
              environment=PINECONE_API_ENV)


index_name = "restaurant-chatbot"  

if index_name not in pc.list_indexes().names():
    pc.create_index(
        name=index_name,
        dimension=384,
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region="us-east-1"),
    )

index = pc.Index(index_name)
# Load the LangChain Pinecone VectorStore from index

docsearch = PineconeVectorStore(index=index, embedding=embeddings)

memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True,
    output_key="answer"
)

#  Load your prompt template
prompt = PromptTemplate(template=bruno_prompt, input_variables=["context", "question"])

chain_type_kwargs={"prompt": prompt}

#  Set up HuggingFace model (Locally or switch to HF Inference API)

model_name = "google/flan-t5-small"

tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

qa_pipeline = pipeline("text2text-generation", model=model, tokenizer=tokenizer)

llm = HuggingFacePipeline(pipeline=qa_pipeline)

#  Set up LangChain QA Chain
# qa_chain = load_qa_chain(
#     llm=llm,
#     prompt=bruno_prompt
# )

qa = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=docsearch.as_retriever(search_kwargs={'k': 2}),
    return_source_documents=True,
    chain_type_kwargs=chain_type_kwargs

)
# qa = ConversationalRetrievalChain.from_llm(
#     llm=llm,
#     retriever=docsearch.as_retriever(),
#     # chain_type="stuff",
#     memory=memory,
#     combine_docs_chain_kwargs={"prompt": bruno_prompt},
#     return_source_documents=True

# )
def get_rag_response(query: str) -> str:
    try:
        response = qa.invoke({"query": query})
        print(response["result"])
        return response["result"]
    except Exception as e:
        print(f"Error: {e}")
        return "Sorry, something went wrong."

