from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

load_dotenv()

def initialize_llm(model_name="gemini-2.5-flash", temperature=0.2):
    """Initialize the Google Gemini model wrapper."""

    return ChatGoogleGenerativeAI(model=model_name, temperature=temperature)

def convert_to_langchain_message(st_message):
    """Map Streamlit chat dictionary to LangChain message objects."""
    if st_message["role"] == "user":
        return HumanMessage(content=st_message["content"])
    elif st_message["role"] == "assistant":
        return AIMessage(content=st_message["content"])
    return None

def rewrite_query_with_history(user_query, chat_history, llm):
    """1. Reformulate the user query to be a standalone question using Chat History."""
    system_prompt = (
        "Given a chat history and the latest user question "
        "which might reference context in the chat history, "
        "formulate a standalone question which can be understood without the chat history. "
        "Do NOT answer the question, just reformulate it and return it."
    )
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
    ])
    
    # Modern LCEL Chain syntax linking: Prompt -> LLM -> Output Text
    rewriter_chain = prompt | llm | StrOutputParser()
    
    return rewriter_chain.invoke({"input": user_query, "chat_history": chat_history})

def generate_final_answer(context, user_query, chat_history, llm):
    """2. Generate the final answer using the retrieved context and history."""
    system_prompt = (
        "You are an expert legal AI assistant specializing in analyzing privacy policies.\n"
        "Your task is to answer the user's question using ONLY the provided context below.\n\n"
        "CRITICAL INSTRUCTIONS:\n"
        "1. If the user's question is ambiguous, incomplete, or requires more details/context from their side to give a precise legal answer, do NOT guess. Instead, politely ask the user for the specific clarifications or details needed.\n"
        "2. If the question is clear but the answer is genuinely NOT present in the provided context, say honestly that you cannot find it in the document.\n"
        "3. If the answer is present, answer it accurately and concisely based ONLY on the context.\n\n"
        "Context:\n{context}"
    )
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
    ])
    
    final_chain = prompt | llm | StrOutputParser()
    
    return final_chain.invoke({
        "input": user_query,
        "chat_history": chat_history,
        "context": context
    })

def generate_rag_response(vector_db, user_query, raw_st_history):
    """3. Orchestrator function: Coordinates history, retrieval, and generation."""
    # Process and slice history to keep only the last 4 messages (2 turns)
    chat_history = [
        convert_to_langchain_message(msg) 
        for msg in raw_st_history[-4:] 
        if convert_to_langchain_message(msg) is not None
    ]
    
    llm = initialize_llm()
    retriever = vector_db.as_retriever(search_kwargs={"k": 8})
    
    # Step 1: Rewrite the question based on context history
    standalone_query = rewrite_query_with_history(user_query, chat_history, llm)
    
    # Step 2: Retrieve relevant documents using the clean query
    docs = retriever.invoke(standalone_query)
    context = "\n\n".join(doc.page_content for doc in docs)
    
    # Step 3: Generate the final legal answer
    answer = generate_final_answer(context, user_query, chat_history, llm)
    
    return answer