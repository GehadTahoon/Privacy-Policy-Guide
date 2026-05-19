# 🛡️ Privacy Policy Guide

An interactive AI chatbot that helps users easily read and understand long, complex Privacy Policy documents. 

Instead of relying on general AI knowledge, this application implements a **Retrieval-Augmented Generation (RAG)** architecture. This ensures that every answer is strictly based on the uploaded document, eliminating guessing (hallucinations) and ensuring maximum factual accuracy.

---

## 🏗️ Architectural Overview & Technical Workflow

The application is engineered around a modular RAG pipeline divided into three main phases:

### 1. Document Reading & Text Splitting (`Data_processing.py`)
*   **PDF Parsing:** Uses `PyPDF` to extract raw text from multi-page legal documents easily.
*   **Smart Text Splitting:** Breaks dense legal text into smaller, overlapping paragraphs. This keeps the sentences in context and ensures that important clauses are not cut in half.

### 2. Vector Embeddings & Local Indexing
*   **Embedding Generation:** Transforms text paragraphs into mathematical numbers (Embeddings) that capture the real meaning of the text.
*   **Vector Store (FAISS):** Stores and indexes these embeddings locally using Facebook AI Similarity Search (`FAISS`). When a user asks a question, the system quickly searches and finds the top most relevant text blocks.

### 3. Smart Generation & UI Optimization (`app.py`)
*   **Orchestration (LangChain):** Connects the retrieved text blocks and the user's question together into a structured prompt.
*   **LLM Integration:** Sends this prompt to **Google Gemini** (via `langchain-google-genai`) to write a natural, precise, and professional answer.
*   **Streamlit UI Fragments:** Optimizes performance by wrapping the chat interface in isolated Streamlit fragments. This ensures that the chat updates instantly without reloading the whole app or re-processing the PDF file.

---

## 🛠️ Tech Stack & Dependencies

*   **User Interface:** `Streamlit` (using optimized runtime fragments for a fast UI experience).
*   **LLM Orchestration:** `LangChain` (for clean, modular chain workflow).
*   **Vector Database:** `FAISS-CPU` (for high-performance local text search).
*   **Core LLM:** `Google Gemini API` (using Gemini 2.5 Flash for super-fast responses).
*   **Document Processing:** `PyPDF` (to read and extract text from PDF files).
*   **Environment Configuration:** `Python-Dotenv` (to keep your private Google API key safe and hidden).

---

## ✨ Key Engineering Features

*   **Zero-Hallucination Guardrails:** The system prompt restricts the AI from using external knowledge. If the answer is missing from the PDF, the chatbot will honestly say it cannot find it.
*   **State & Session Isolation:** Uses Streamlit's `session_state` to separate the file-upload process from the live chat memory. This prevents screen flickering and data loss during active chats.
*   **Clean, Modular Codebase:** The code is completely separated into two clean files: one for data processing and one for the visual design, following professional software principles.

---

## 📊 Evaluation & Quality Assurance (The RAG Triad)

To ensure the reliability, accuracy, and safety of this RAG application, the system was thoroughly evaluated against the **RAG Triad** framework using specialized test cases derived from the WhatsApp Privacy Policy document. 

Below is the visual breakdown of how the pipeline satisfies each architectural pillar:

### 1. Context Relevance (High-Quality Retrieval)
* **Objective:** Verifies if the Vector Store extracts the exact technical or policy details from the database based on the user query without bringing irrelevant text.
* **Test Case:** *"Does WhatsApp allow third-party banner ads, and what are their future plans regarding ads?"*
* **Observation:** The retriever precisely located the specific clause regarding monetization and advertisements (Page 8), allowing the LLM to provide a highly granular and contextual response.

![Context Relevance](images/context_relevance.png)

---

### 2. Groundedness & Anti-Hallucination Guardrails
* **Objective:** Ensures the system remains 100% faithful to the provided document and strictly refuses to "hallucinate" or invent facts from its general knowledge if the answer is missing.
* **Test Case:** *"What is the capital of France?"*
* **Observation:** Rather than responding with its pre-trained global data, the LLM strictly adhered to the system instructions and safely declared that the information was missing from the uploaded context.

![Groundedness](images/groundedness.png)

---

### 3. Answer Relevance & Chat Memory Continuity
* **Objective:** Measures whether the generated answers directly address the user's intent, and evaluates the system's multi-turn conversational memory using ambiguous pronouns.
* **Test Case:** * *User (Turn 1):* *"If I just delete the WhatsApp app from my phone... what happens to my data?"*
    * *User (Turn 2):* *"And if I use the actual in-app feature instead, what specific items will be deleted?"*
* **Observation:** The system perfectly linked the pronoun *"instead"* to the historical context of Turn 1, utilized the chat history state, and structured the comparative response beautifully in clear bullet points.

![Answer Relevance](images/answer_relevance.png)

---


## 📦 Installation & Local Setup

1. **Clone the Repository:**
   ```bash
   git clone [https://github.com/GehadTahoon/Privacy-Policy-Guide.git](https://github.com/GehadTahoon/Privacy-Policy-Guide.git)
   cd Privacy-Policy-Guide

2. **Configure Environment Variables**
    Create a new file named `.env` in the root directory and securely add your API key:
    ```env
    GOOGLE_API_KEY=your_actual_api_key_here

3. **Install Dependencies**
    Install all the required Python libraries using pip:
    ```bash
    pip install -r requirements.txt

4. **Run the Application**
    Start the Streamlit local server to launch the chatbot in your browser:
    ```bash
    streamlit run app.py

---

## 👥 Contributing & Support
This project was developed as a specialized AI tool for analyzing privacy policies. If you have any questions or suggestions to improve the RAG pipeline, feel free to open an issue or pull request!
