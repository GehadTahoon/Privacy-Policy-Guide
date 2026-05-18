from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import os

def read_pdf(file_path):
    if not os.path.exists(file_path):
        return None
        
    loader = PyPDFLoader(file_path)
    pages = loader.load_and_split()
    return pages

def split_text(documents):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
        add_start_index=True,
    )
    chunks = text_splitter.split_documents(documents)
    return chunks

#print(split_text(read_pdf('whatsapp_policy.pdf'))[1].page_content)