import os
from PyPDF2 import PdfReader
from dotenv import load_dotenv
import google.generativeai as genai

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_community.vectorstores import FAISS

from langchain_classic.chains.retrieval import create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf.file)
        for page in pdf_reader.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted
    return text

def get_text_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=10000,
        chunk_overlap=1000
    )
    return text_splitter.split_text(text)

def get_vector_store(text_chunks):
    try:
        embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
        vector_store = FAISS.from_texts(text_chunks, embedding=embeddings)
        index_path = os.path.join(os.getcwd(), "faiss_index")
        vector_store.save_local(index_path)
        return True
    except Exception as e:
        raise e

def process_user_query(user_question):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    index_path = os.path.join(os.getcwd(), "faiss_index")
    model = ChatGoogleGenerativeAI(model="gemini-1.5-pro", temperature=0.3)

    faiss_file = os.path.join(index_path, "index.faiss")
    
    if os.path.exists(faiss_file):
        try:
            db = FAISS.load_local(index_path, embeddings, allow_dangerous_deserialization=True)
            retriever = db.as_retriever()
            
            system_prompt = (
                "You are a professional Business AI Assistant. "
                "Use the provided context to answer the question accurately. "
                "If the answer is NOT in the context, use your general business knowledge. "
                "\n\n"
                "Context: {context}"
            )
            
            prompt = ChatPromptTemplate.from_messages([
                ("system", system_prompt),
                ("human", "{input}"),
            ])

            question_answer_chain = create_stuff_documents_chain(model, prompt)
            rag_chain = create_retrieval_chain(retriever, question_answer_chain)
            
            response = rag_chain.invoke({"input": user_question})
            return response["answer"]
        except Exception:
            return model.invoke(user_question).content
    else:
        return model.invoke(user_question).content

def get_summary(text):
    model = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.3)
    summary_prompt = f"Summarize the following business document into clear bullet points:\n\n{text}"
    return model.invoke(summary_prompt).content