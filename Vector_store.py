from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
import os

def create_embeddings(chunks):
    if not chunks:
        return None
    
    os.environ["HF_HOME"] = "./cache"
    embedding_llm = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        cache_folder="./cache"
    )
    
    return embedding_llm

def create_vector_db(chunks, embedding_llm):
    vector_db = FAISS.from_documents(chunks, embedding_llm)

    return vector_db