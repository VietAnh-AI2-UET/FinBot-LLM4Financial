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
GG_API = ''
class HuggingFaceLLM(LLM, BaseModel):
    model: str
    api_token: str
    temperature: float = 0.01

    @property
    def _llm_type(self) -> str:
        return "huggingface-inference"

    def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        
        client = InferenceClient(
            provider="novita",
            api_key="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"
        )
        response = client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=self.temperature,
        )
        return response.choices[0].message.content


class LMStudioLLM(LLM):
    model: str = "phogpt-4b-chat"
    base_url: str = "http://localhost:1234/v1"
  # bất kỳ chuỗi nào api
    temperature: float = 0.7

    def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        client = OpenAI(base_url=self.base_url, api_key=self.api_key)
        response = client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "Bạn là một chuyên gia tài chính."},
                {"role": "user", "content": prompt}
            ],
            temperature=self.temperature
        )
        return response.choices[0].message.content

    @property
    def _llm_type(self) -> str:
        return "lm-studio"

    
# llm = HuggingFaceLLM(model="deepseek-ai/DeepSeek-R1")
# llm = LMStudioLLM() 
# Load LLM

def load_llm(model_file):
    llm = CTransformers(
        model=model_file,
        model_type="llama",
        max_new_tokens=1024,
        temperature=0.01
    )
    return llm

# Tao prompt template
def creat_prompt(template):
    prompt = PromptTemplate(template = template, input_variables=["context", "question"])
    return prompt


# Tao simple chain
def create_qa_chain(prompt, llm, db):
    llm_chain = RetrievalQA.from_chain_type(
        llm = llm,
        chain_type= "stuff",
        retriever = db.as_retriever(search_kwargs = {"k":3}, max_tokens_limit=1024),
        return_source_documents = False,
        chain_type_kwargs= {'prompt': prompt}

    )
    return llm_chain

# Read tu VectorDB
os.environ["GOOGLE_API_KEY"] = GG_API
os.environ["GEMINI_API_KEY"] = GG_API

# Bat dau thu nghiem
def response_user(question):
    embedding_model = GPT4AllEmbeddings(model_file="model\\all-MiniLM-L6-v2-f16.gguf")
    db = Chroma(persist_directory="./vector_store", embedding_function=embedding_model)
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

    llm_chain = create_qa_chain(prompt, llm, db)
    response = llm_chain.invoke({"query": question})
    print(response['result'])
    return response['result']
#tabula