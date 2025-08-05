from langchain_community.llms import CTransformers
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain_community.embeddings import GPT4AllEmbeddings
from langchain_community.vectorstores import FAISS

from langchain.prompts.chat import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
# Cau hinh
import os

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
vector_db_path = os.path.join(CURRENT_DIR, "..", "vectorstores", "db_faiss")
model_file = "model/vinallama-2.7b-chat-Q5_0.gguf"
# vector_db_path = "../vectorstores/db_faiss"
from langchain.llms.base import LLM
from typing import Optional, List
from pydantic import BaseModel
from huggingface_hub import InferenceClient

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
            api_key="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",
        )
        response = client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=self.temperature,
        )
        return response.choices[0].message.content
from langchain.llms.base import LLM
from typing import Optional, List
from openai import OpenAI

class LMStudioLLM(LLM):
    model: str = "phogpt-4b-chat"
    base_url: str = "http://localhost:1234/v1"
    api_key: str = "lm-studio"  # bất kỳ chuỗi nào
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
    
# llm = HuggingFaceLLM(model="deepseek-ai/DeepSeek-R1", api_token='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')
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
def read_vectors_db():
    # Embeding
    embedding_model = GPT4AllEmbeddings(model_file="model\\all-MiniLM-L6-v2-f16.gguf")
    db = FAISS.load_local(vector_db_path, embedding_model, allow_dangerous_deserialization=True)
    return db


# Bat dau thu nghiem
def response_user(question):
    db = read_vectors_db()
    llm = HuggingFaceLLM(model="deepseek-ai/DeepSeek-R1", api_token='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')
    #Tao Prompt
    prompt = ChatPromptTemplate.from_messages([
        SystemMessagePromptTemplate.from_template("Bạn là một chuyên gia tài chính."),
        HumanMessagePromptTemplate.from_template("""
    {context}

    Câu hỏi: {question}

    Trả lời chi tiết, chính xác (nếu cần, trích số liệu).
    """)
    ])

    llm_chain = create_qa_chain(prompt, llm, db)

    # Chay cai chain
    # question = "ai là Chủ tịch HĐQT "
    response = llm_chain.invoke({"query": question})
    print(response['result'])
    return response['result']
#tabula