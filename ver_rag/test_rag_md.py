import os
from langchain_community.document_loaders import TextLoader
from langchain_community.embeddings import GPT4AllEmbeddings
from langchain_openai import OpenAIEmbeddings
from langchain.embeddings.base import Embeddings
import google.generativeai as genai2
from langchain_community.llms import CTransformers
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain_community.embeddings import GPT4AllEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_chroma import Chroma
from langchain.prompts.chat import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
import os
from google import genai
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
from langchain.llms.base import LLM
from typing import Optional, List
from pydantic import BaseModel
from huggingface_hub import InferenceClient
from langchain.llms.base import LLM
from typing import Optional, List
from openai import OpenAI
from bs4 import BeautifulSoup
import os
from bs4 import BeautifulSoup

# def html_to_markdown_table(table_tag):
#     """Chuyển table HTML thành chuỗi markdown giữ hàng/cột."""
#     rows = []
#     for tr in table_tag.find_all("tr"):
#         cells = []
#         for cell in tr.find_all(["th", "td"]):
#             text = cell.get_text(strip=True)
#             cells.append(text)
#         rows.append("| " + " | ".join(cells) + " |")
    
#     # Nếu có ít nhất 2 dòng → thêm dòng phân cách markdown
#     if len(rows) >= 2:
#         header = rows[0]
#         separator = "| " + " | ".join(["---"] * (header.count("|") - 1)) + " |"
#         return "\n".join([header, separator] + rows[1:])
#     else:
#         return "\n".join(rows)

# def clean_markdown(folder_path, output_folder=None):
#     cleaned_docs = []
#     if output_folder:
#         os.makedirs(output_folder, exist_ok=True)

#     for filename in os.listdir(folder_path):
#         if filename.lower().endswith(".md"):
#             file_path = os.path.join(folder_path, filename)
            
#             with open(file_path, "r", encoding="utf-8") as f:
#                 raw_content = f.read()
            
#             soup = BeautifulSoup(raw_content, "html.parser")
            
#             # Chuyển từng table sang markdown
#             for table in soup.find_all("table"):
#                 md_table = html_to_markdown_table(table)
#                 table.replace_with(md_table)

#             cleaned_text = soup.get_text(separator="\n")
            
#             cleaned_docs.append({
#                 "filename": filename,
#                 "content": cleaned_text
#             })
            
#             if output_folder:
#                 out_path = os.path.join(output_folder, filename)
#                 with open(out_path, "w", encoding="utf-8") as f:
#                     f.write(cleaned_text)
    
#     return cleaned_docs

# clean_markdown('ocr_results','clear_mkd')
class GoogleEmbeddings(Embeddings):
    def __init__(self, api_key: str, model: str = "models/embedding-001"):
        genai2.configure(api_key=api_key)
        self.model = model

    def embed_documents(self, texts):
        return [genai2.embed_content(model=self.model, content=text)["embedding"] for text in texts]

    def embed_query(self, text):
        return genai2.embed_content(model=self.model, content=text)["embedding"]

# Sử dụng
embedding_fn = GoogleEmbeddings(api_key="AIzaSyDcqBdI_J_VPpY828RlFiB90fpG2kS-PQU")
# folder_path = "clear_mkd"

# # Đảm bảo đọc theo thứ tự file
# files = sorted([f for f in os.listdir(folder_path) if f.endswith(".md")])

# docs = []
# for idx, filename in enumerate(files, start=1):
#     loader = TextLoader(os.path.join(folder_path, filename), encoding="utf-8")
#     loaded_docs = loader.load()
#     for doc in loaded_docs:
#         doc.metadata.update({
#             "source": filename,
#             "page_number": idx,
#             "report_id": "report_2024_001",  # Nếu tất cả trang thuộc 1 báo cáo
#             "file_path": os.path.join(folder_path, filename)
#         })
#     docs.extend(loaded_docs)

# embedding_fn = OpenAIEmbeddings(model="text-embedding-3-large")
# vectordb = Chroma.from_documents(docs, embedding_fn, persist_directory="./chroma_finance_db")
# vectordb.persist()

# print("✅ Vector DB tài chính đã tạo xong")
def create_qa_chain(prompt, llm, db):
    llm_chain = RetrievalQA.from_chain_type(
        llm = llm,
        chain_type= "stuff",
        retriever = db.as_retriever(search_kwargs = {"k":7}, max_tokens_limit=1024),
        return_source_documents = False,
        chain_type_kwargs= {'prompt': prompt}

    )
    return llm_chain
# query = "NỢ PHẢI TRẢ VÀ VỐN CHỦ SỞ HỮU"
# results = vectordb.similarity_search(query, k=5)

# for r in results:
#     print(f"[Trang {r.metadata['page_number']}] {r.metadata['source']}")
#     print(r.page_content[:300], "...\n")
embedding_model = GPT4AllEmbeddings(model_file="backendFastAPI/model_LLM/model/all-MiniLM-L6-v2-f16.gguf")
os.environ["GOOGLE_API_KEY"] = "AIzaSyDcqBdI_J_VPpY828RlFiB90fpG2kS-PQU"
os.environ["GEMINI_API_KEY"] = "AIzaSyDcqBdI_J_VPpY828RlFiB90fpG2kS-PQU"
db = Chroma(persist_directory="./chroma_db", embedding_function=embedding_model)
llm = ChatGoogleGenerativeAI(
model="gemini-2.0-flash",  # hoặc gemini-1.5-pro nếu bạn được cấp
temperature=0.3,
max_output_tokens=1024
)
prompt = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template("Bạn là một chuyên gia tài chính."),
    HumanMessagePromptTemplate.from_template("""
{context}

Câu hỏi: {question}

Hãy dựa trên những thông tin có trong dữ liệu được cung cấp tìm những thông tin số liệu liên quan đến câu hỏi nhất và đưa ra câu trả lời kèm theo trích dẫn

Trả lời chi tiết, chính xác (nếu cần, trích số liệu).

""")
])
question = " cho vay khách hàng"
llm_chain = create_qa_chain(prompt, llm, db)
response = llm_chain.invoke({"query": question})
results = db.similarity_search(question, k=5)
print(response['result'])
# for r in results:
#     # print(f"[Trang {r.metadata['page_number']}] {r.metadata['source']}")
#     print(r.page_content)