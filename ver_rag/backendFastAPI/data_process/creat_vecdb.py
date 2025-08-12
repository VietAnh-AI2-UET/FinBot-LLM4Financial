from langchain_chroma import Chroma
from langchain_community.embeddings import GPT4AllEmbeddings
from langchain.chains import RetrievalQA
import shutil
import os
import os
import json
from langchain.schema import Document
embedding_model = GPT4AllEmbeddings(model_file="model\\all-MiniLM-L6-v2-f16.gguf") 
persist_dir = "./vector_store"
# Load JSON
def get_text_data(path):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    docs = []

    # Duyệt qua từng bảng
    for table in data["tables"]:
        metadata = {
            "name_company": data["name_company"],
            "name_report": data["name_report"],
            "table_title": table["title"],
            "table_index": table["table_index"]
        }
        # Ghép tiêu đề + nội dung thành 1 chuỗi text
        text = f"{table['title']}\n\n{table['content']}"
        
        doc = Document(page_content=text, metadata=metadata)
        docs.append(doc)
    return docs

db = None

def add_new_doc(path_json):
    global db

    # Nếu db đã tồn tại thì đóng/giải phóng nó trước
    if db is not None:
        try:
            # db.persist()    # nếu có
            db = None       # hoặc gọi hàm đóng nếu thư viện có hỗ trợ
        except Exception:
            pass
    
    # Xóa thư mục cũ nếu có
    if os.path.exists(persist_dir):
        shutil.rmtree(persist_dir)
    
    docs = get_text_data(path_json)
    
    # Tạo lại db từ đầu với docs mới
    db = Chroma.from_documents(
        documents=docs,
        embedding=embedding_model,
        persist_directory=persist_dir
    )