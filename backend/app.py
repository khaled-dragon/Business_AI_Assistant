from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import os

from logic import (
    process_user_query,
    chat_with_llm,
    get_pdf_text,
    get_text_chunks,
    get_vector_store,
    get_summary
)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    question: str
    chat_history: Optional[List[List[str]]] = []
    mode: str

@app.get("/")
def root():
    return {"status": "OptiVerse AI backend is running"}

@app.post("/chat")
async def chat_endpoint(request: QueryRequest):
    try:
        if request.mode == "rag":
            response = process_user_query(request.question, request.chat_history)
        else:
            response = chat_with_llm(request.question, request.chat_history)
        
        return {"response": response}
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/upload")
async def upload_files(files: List[UploadFile] = File(...)):
    if not files:
        raise HTTPException(status_code=400, detail="No files uploaded")
    try:
        for f in files:
            f.file.seek(0)
        raw_text = get_pdf_text(files)
        if not raw_text.strip():
            raise HTTPException(status_code=400, detail="No text extracted from PDFs")
        text_chunks = get_text_chunks(raw_text)
        get_vector_store(text_chunks)
        return {"message": "Files processed and indexed successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/summarize")
async def summarize_endpoint(files: List[UploadFile] = File(...)):
    if not files:
        raise HTTPException(status_code=400, detail="No files uploaded")
    try:
        for f in files:
            f.file.seek(0)
        raw_text = get_pdf_text(files)
        if not raw_text.strip():
            raise HTTPException(status_code=400, detail="No text extracted from PDFs")
        summary = get_summary(raw_text)
        return {"summary": summary}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7860)
