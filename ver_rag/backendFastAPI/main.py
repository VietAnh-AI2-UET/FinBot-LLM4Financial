from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from typing import Optional
import tempfile
import shutil
from data_process.table_data import create_json_data
from model_LLM.rag import response_user
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
    # if message:
    if file:
        print(f"Received file: {file.filename}")
        with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as tmp:
            shutil.copyfileobj(file.file, tmp)
            saved_file_path = tmp.name
            create_json_data(saved_file_path)
    print(saved_file_path)
    if not saved_file_path:
        return {"response": "Bạn chưa upload file tài liệu nào."}
    
    if message:
        res = response_user(message)
        return {"response": res}
    else:
        return {"response": "❗Bạn chưa nhập câu hỏi."}

    # return {"response": f" {message}"}
