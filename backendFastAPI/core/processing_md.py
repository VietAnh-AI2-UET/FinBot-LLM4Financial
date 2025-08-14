import pypandoc
from bs4 import BeautifulSoup
from markdownify import markdownify as mdify
import os
from bs4 import BeautifulSoup
from markdownify import markdownify as mdify
from langchain.schema import Document
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
import os

from langchain_community.embeddings import GPT4AllEmbeddings
# Đường dẫn thư mục chứa các file Markdown
# input_dir = "tmp_ocr_results"

def clear_folder_files(folder_path):
    """
    Xóa tất cả file trong folder_path, không xóa thư mục con.
    """
    if not os.path.exists(folder_path):
        print(f"Folder '{folder_path}' không tồn tại.")
        return
    
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            try:
                os.remove(file_path)
                print(f"Đã xóa file: {file_path}")
            except Exception as e:
                print(f"Lỗi khi xóa file {file_path}: {e}")
def preprocessing_md(input_dir):
    # Đảm bảo thư mục đầu ra tồn tại
    output_dir = "preprocessed_md"
    os.makedirs(output_dir, exist_ok=True)
    clear_folder_files(output_dir)
    # Lấy danh sách tất cả file Markdown trong thư mục
    md_files = [f for f in os.listdir(input_dir) if f.endswith('.md')]

    # Xử lý từng file Markdown
    for md_file in md_files:
        input_path = os.path.join(input_dir, md_file)
        with open(input_path, "r", encoding="utf-8") as file:
            md_content = file.read()

        # Parse và chuyển HTML tables sang Markdown tables
        soup = BeautifulSoup(md_content, "html.parser")
        for table in soup.find_all("table"):
            md_table = mdify(str(table), heading_style="ATX")  # Chuyển table HTML sang Markdown
            table.replace_with(md_table)

        # Lưu file Markdown mới đã preprocess
        output_path = os.path.join(output_dir, md_file.replace(".md", "_preprocessed.md"))
        preprocessed_md = str(soup)
        with open(output_path, "w", encoding="utf-8") as file:
            file.write(preprocessed_md)
        print(f"Đã xử lý và lưu {output_path}")
    # creat_db_for_md(output_dir)
    
def creat_db_for_md(data_dir):
    embedding_model = GPT4AllEmbeddings(model_file="backendFastAPI/model_LLM/model/all-MiniLM-L6-v2-f16.gguf") # Mô hình nhúng miễn phí
    # Thiết lập đường dẫn và mô hình
    persist_dir = "./vector_store"  # Thư mục lưu trữ Chroma DB
    # Đảm bảo thư mục tồn tại
    os.makedirs(persist_dir, exist_ok=True)

    # Lấy danh sách tất cả file Markdown trong thư mục
    md_files = [f for f in os.listdir(data_dir) if f.endswith('.md')]

    # Danh sách để lưu tất cả Document
    all_documents = []

    # Xử lý từng file Markdown
    for md_file in md_files:
        file_path = os.path.join(data_dir, md_file)
        with open(file_path, "r", encoding="utf-8") as file:
            markdown_content = file.read()

        # Chia nhỏ nội dung thành các chunk
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,  # Kích thước mỗi chunk (tùy chỉnh)
            chunk_overlap=100,  # Độ chồng chéo để giữ ngữ cảnh
            separators=["\n\n", "\n", ".", " "]  # Các điểm cắt ưu tiên
        )
        texts = text_splitter.split_text(markdown_content)

        # Tạo danh sách Document với metadata (tên file làm số trang hoặc ID)
        page_number = md_file.replace(".md", "")  # Giả sử tên file là số trang (ví dụ: page1.md)
        documents = [Document(page_content=text, metadata={"source": md_file, "page": page_number}) for text in texts]
        all_documents.extend(documents)
        print(f"Đã xử lý {md_file} với {len(documents)} chunk(s).")

    # Khởi tạo hoặc tải Chroma DB
    if os.path.exists(persist_dir):
        db = Chroma(persist_directory=persist_dir, embedding_function=embedding_model)
        print("Đã tải Chroma DB từ thư mục hiện có.")
    else:
        db = Chroma.from_documents(
            documents=[],  # Khởi tạo rỗng
            embedding_function=embedding_model,
            persist_directory=persist_dir
        )
        print("Đã tạo mới Chroma DB và lưu vào thư mục.")

    # Thêm tất cả Document vào DB
    if all_documents:
        db.add_documents(all_documents)
        print(f"Đã thêm {len(all_documents)} tài liệu từ {len(md_files)} file vào Chroma DB.")
    db.persist()
    print(f"Chroma DB đã được lưu tại {persist_dir}.")
