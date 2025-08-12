from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from typing import Optional
import tempfile
import shutil
import os
from data_process.table_data import create_json_data
from model_LLM.rag import response_user
from data_process.OCR_pdf import process_pdf_file
app = FastAPI()
saved_file_path = None
# Cho phép frontend truy cập
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # hoặc thay "*" bằng "http://localhost:3000" nếu cần giới hạn
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Message(BaseModel):
    message: str

@app.post("/chat")
async def chat(message: str = Form(...), file: Optional[UploadFile] = File(None)):
    global saved_file_path
    print(f"Message: {message}")

    if file:
        filename = file.filename.lower()
        print(f"Received file: {file.filename}")

        if filename.endswith('.doc') or filename.endswith('.docx'):
            with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(filename)[1]) as tmp:
                shutil.copyfileobj(file.file, tmp)
                saved_file_path = tmp.name
                create_json_data(saved_file_path)
        elif filename.endswith('.pdf'):
            # Xử lý file PDF riêng biệt, ví dụ lưu tạm và gọi hàm OCR riêng
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                shutil.copyfileobj(file.file, tmp)
                saved_file_path = tmp.name
                process_pdf_file(saved_file_path)
                print("PDF file nhận được, xử lý riêng tại đây")
        else:
            return {"response": "❌ Chỉ chấp nhận file .doc, .docx hoặc .pdf"}

    print(f"Saved file path: {saved_file_path}")

    if not saved_file_path:
        return {"response": "Bạn chưa upload file tài liệu nào."}
    
    if message:
        res = response_user(message)
        return {"response": res}
    else:
        return {"response": "❗Bạn chưa nhập câu hỏi."}