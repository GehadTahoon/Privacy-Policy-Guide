import streamlit as st
import tempfile
import os
from Data_processing import read_pdf, split_text
from Vector_store import create_embeddings, create_vector_db
from QA_chain import generate_rag_response

# 1. Page Configuration
st.set_page_config(page_title="Privacy Policy AI", page_icon="🛡️", layout="wide")

# 2. Initialize Session States
if "chat_histories" not in st.session_state:
    st.session_state.chat_histories = {
        "Upload PDF": [{"role": "assistant", "content": "Hello! Please upload your privacy policy PDF to begin."}]
    }

if "vector_dbs" not in st.session_state:
    st.session_state.vector_dbs = {
        "Upload PDF": None
    }

# 3. Sidebar Configuration
with st.sidebar:
    st.title("Settings ⚙️")
    st.markdown("---")
    
    st.write("**Choose Input Method:**")
    st.markdown("🔘 **Upload PDF**")
    active_key = "Upload PDF"
    
    # Disabled visual indicators for future expansion roadmap
    st.markdown(
        "<span style='color: #888888; cursor: not-allowed; opacity: 0.6;'>⚪ URL 🌐 <i>(Coming Soon 🔒)</i></span>", 
        unsafe_allow_html=True
    )
    st.markdown(
        "<span style='color: #888888; cursor: not-allowed; opacity: 0.6;'>⚪ Paste Text ✍️ <i>(Coming Soon 🔒)</i></span>", 
        unsafe_allow_html=True
    )
    
    st.markdown("---")
    
    if st.button("Clear This Conversation 🗑️"):
        st.session_state.chat_histories[active_key] = [
            {"role": "assistant", "content": "Chat history cleared. How can I help you with this document now?"}
        ]
        st.rerun()

# 4. Main UI Title
st.title("🛡️ Privacy Policy Intelligence")

pages_to_process = None

# 5. Data Ingestion
uploaded_file = st.file_uploader("Upload your privacy policy document", type="pdf")
if uploaded_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
        temp_file.write(uploaded_file.getbuffer())
        temp_file_path = temp_file.name
    try:
        pages_to_process = read_pdf(temp_file_path)
    finally:
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)

# 6. Shared Processing Pipeline
if pages_to_process and st.session_state.vector_dbs[active_key] is None:
    with st.status("Analyzing document...", expanded=True) as status:
        chunks = split_text(pages_to_process)
        embedding_llm = create_embeddings(chunks)
        st.session_state.vector_dbs[active_key] = create_vector_db(chunks, embedding_llm)
        status.update(label="Analysis Complete!", state="complete", expanded=False)

if st.session_state.vector_dbs[active_key] is not None:
    st.success("Analysis complete! I am ready to answer your questions below.")

st.markdown("---")

# 7. Isolated Chat Interface using Fragment
@st.fragment
def show_chat_interface(method):
    current_db = st.session_state.vector_dbs.get(method)
    chat_container = st.container()
    
    # Render historical chat context
    with chat_container:
        for message in st.session_state.chat_histories[method]:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    # Handle locked system states cleanly within the input element itself
    if current_db is None:
        st.chat_input("Chat is locked. Please upload and process a PDF first...", disabled=True)
        return

    # Handle active user input inside the safe context window
    if prompt := st.chat_input("Ask me anything about the privacy policy..."):
        st.session_state.chat_histories[method].append({"role": "user", "content": prompt})
        with chat_container.chat_message("user"):
            st.markdown(prompt)

        # Generate response from RAG Chain orchestrator
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    answer = generate_rag_response(
                        vector_db=current_db,
                        user_query=prompt,
                        raw_st_history=st.session_state.chat_histories[method]
                    )
                except Exception as e:
                    answer = f"⚠️ An error occurred: {str(e)}"

                st.markdown(answer)
                st.session_state.chat_histories[method].append({"role": "assistant", "content": answer})

# Run the isolated chat UI
show_chat_interface(active_key)