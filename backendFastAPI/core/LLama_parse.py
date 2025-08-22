import os
from llama_index.core import Settings
from llama_index.llms.gemini import Gemini
from llama_index.embeddings.gemini import GeminiEmbedding
from llama_parse import LlamaParse
import json
os.environ["LLAMA_CLOUD_API_KEY"] = ''
os.environ["GOOGLE_API_KEY"] = ''
Settings.llm = Gemini(model="gemini-2.5-flash")
Settings.embed_model = GeminiEmbedding()

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
parser = LlamaParse(
    result_type="markdown",
    auto_mode=True,
    auto_mode_trigger_on_image_in_page=True,
    auto_mode_trigger_on_table_in_page=True,
    # auto_mode_trigger_on_text_in_page="<text_on_page>"
    # auto_mode_trigger_on_regexp_in_page="<regexp_on_page>"
)
# file_path = "20250724 - ACB - BCTC hop nhat Quy 02 nam 2025.pdf"

def pdf_to_md(file_path,type):
    name_file =  os.path.splitext(os.path.basename(file_path))[0]
    save_path = f'../database/{name_file}.json'
    if os.path.exists(save_path):
        print("file pdf này đã được xử lý.")
        return None
    save_data =  {
            "isSave": 'đã parse',
            "type": f"{type}"
        }
    
    print("đang viết")
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    with open(save_path, "w", encoding="utf-8") as f:
        json.dump(save_data, f, indent=2, ensure_ascii=False)
    print("viết xong")
    documents = parser.load_data(file_path)
    output_folder = "preprocessed_md"
    os.makedirs(output_folder, exist_ok=True)
    clear_folder_files(output_folder)
    for i in range(len(documents)):
        with open(f"{output_folder}/page_{i}.md", "w", encoding="utf-8") as f:
            f.write(documents[i].text_resource.text)