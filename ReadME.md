# 🚀 Business AI Assistant (RAG-Powered)

An intelligent Document Assistant that allows users to upload multiple business PDFs and have a real-time, context-aware conversation. Powered by **LangChain**, **Groq (Llama 3)**, and **Google Gemini Embeddings**.



## 🌟 Features
* **Multi-PDF Processing:** Upload and index multiple business documents simultaneously.
* **Hybrid AI Architecture:** Uses **Google Gemini** for high-precision embeddings and **Groq (Llama 3.3)** for lightning-fast chat responses.
* **Contextual Intelligence:** Uses Retrieval-Augmented Generation (RAG) to ensure answers are grounded in your specific documents.
* **Business Summary:** Generate instant bullet-point summaries of long corporate files.
* **Persistent Vector Store:** Efficient document search using **FAISS**.

## 🏗️ Technical Stack
* **Backend:** FastAPI (Python)
* **AI Framework:** LangChain
* **LLM:** Llama-3.3-70b (via Groq Cloud)
* **Embeddings:** Google Generative AI (`models/embedding-001`)
* **Vector Database:** FAISS
* **Frontend:** HTML5, Tailwind CSS, Vanilla JavaScript

## 🛠️ How It Works (The Logic)
1.  **Ingestion:** PDFs are parsed using `PyPDF2` and broken into semantic chunks.
2.  **Vectorization:** Chunks are converted into high-dimensional vectors via Google Embeddings.
3.  **Storage:** Vectors are stored in a local FAISS index for millisecond-level retrieval.
4.  **Retrieval:** When a user asks a question, the system finds the most relevant chunks.
5.  **Generation:** The context + user question are sent to Groq's Llama-3.3 to generate a professional business response.

## 🚀 Setup & Installation

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/your-username/business-ai-assistant.git](https://github.com/your-username/business-ai-assistant.git)
   cd business-ai-assistant

2. ## Create a Virtual Environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. ## Install dependencies:
```bash
pip install -r requirements.txt
```
4. ## Environment Variables: Create a .env file and add your keys:
```bash
GOOGLE_API_KEY=your_google_key
GROQ_API_KEY=your_groq_key
```

5. ## Run the server:
```bash
uvicorn app:app --reload
```
