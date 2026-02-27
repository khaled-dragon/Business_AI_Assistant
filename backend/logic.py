import os
from PyPDF2 import PdfReader
from dotenv import load_dotenv
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_groq import ChatGroq
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage

load_dotenv()

def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        try:
            pdf_reader = PdfReader(pdf.file)
            for page in pdf_reader.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted
        except Exception as e:
            print(f"DEBUG: PDF Read Error: {e}")
    return text

def get_text_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=100
    )
    chunks = text_splitter.split_text(text)
    print(f"DEBUG: Created {len(chunks)} chunks")
    return chunks

def get_vector_store(text_chunks):
    try:
        embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        vector_store = FAISS.from_texts(text_chunks, embedding=embeddings)
        index_path = "/tmp/faiss_index"
        if not os.path.exists(index_path):
            os.makedirs(index_path)
        vector_store.save_local(index_path)
        return True
    except Exception as e:
        print(f"DEBUG: Vector Store Error: {e}")
        return False

def chat_with_llm(question, chat_history=[]):
    model = ChatGroq(
        model_name="llama-3.3-70b-versatile",
        groq_api_key="yout API"
    )
        
    langchain_history = []
    for role, content in chat_history:
        if role == "human":
            langchain_history.append(HumanMessage(content=content))
        else:
            langchain_history.append(AIMessage(content=content))
                
    langchain_history.append(HumanMessage(content=question))
    response = model.invoke(langchain_history)
    return response.content

def process_user_query(user_question, chat_history=[]):
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    index_path = "/tmp/faiss_index"
    model = ChatGroq(
        model_name="llama-3.3-70b-versatile",
        groq_api_key="your API"
    )
        
    faiss_file = os.path.join(index_path, "index.faiss")
        
    if os.path.exists(faiss_file):
        try:
            db = FAISS.load_local(index_path, embeddings, allow_dangerous_deserialization=True)
            docs = db.similarity_search(user_question, k=3)
            context = "\n".join([doc.page_content for doc in docs])
                        
            system_prompt = (
                "You are a professional business assistant. "
                "Use the following pieces of retrieved context to answer the user's question. "
                "If the answer is not in the context, use your general knowledge but mention that. "
                "Keep the conversation history in mind.\n\n"
                f"Context:\n{context}"
            )
            messages = [("system", system_prompt)]
            for role, content in chat_history:
                messages.append((role, content))
            messages.append(("human", user_question))
                        
            prompt = ChatPromptTemplate.from_messages(messages)
            chain = prompt | model
            response = chain.invoke({})
            return response.content
                    
        except Exception as e:
            print(f"DEBUG: RAG Error: {e}")
            return f"Error in document retrieval: {str(e)}"
            
    return "No documents found. Please upload and process a PDF first, or switch to General AI mode."

def get_summary(text):
    model = ChatGroq(
        model_name="llama-3.3-70b-versatile",
        groq_api_key="your API"
    )
    summary_prompt = f"Summarize the following text professionally and highlight key business points:\n\n{text[:15000]}"
    response = model.invoke(summary_prompt)
    return response.content
