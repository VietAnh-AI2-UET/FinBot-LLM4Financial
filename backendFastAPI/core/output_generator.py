from core.receiver import find_information
from huggingface_hub import InferenceClient
from google import genai
import os
GOOGLE_API = "AIzaSyCP4IUNUxYmPTY3dtU_nMacWJg_61Patzg" #https://aistudio.google.com/apikey truy cập để lấy API
#get user question and similar information -> create a prompt for LLM

def get_user_prompt_docx(user_question, similar_infos: list[dict]):
    user_prompt = 'Từ các thông tin sau:\n'
    for similar_info in similar_infos:
        user_prompt += f"Tiêu đề: {similar_info['title']}\nNội dung: {similar_info['text']}\n"
    user_prompt += 'Hãy trả lời câu hỏi:\n'
    user_prompt += user_question
    return user_prompt

def get_user_prompt_csv(user_question, similar_infos: list[dict]):
    user_prompt = 'Từ các thông tin sau:\n'
    for similar_info in similar_infos:
        user_prompt += f"Hạng mục: {similar_info['Hạng mục']}\nMã số: {similar_info['Mã số']}\nGiá trị: {similar_info['Giá trị']}\n"
    user_prompt += 'Hãy trả lời câu hỏi:\n'
    user_prompt += user_question
    return user_prompt

def get_user_prompt_md(user_question, similar_infos: list[dict]):
    user_prompt = 'Từ các thông tin sau:\n'
    for similar_info in similar_infos:
        user_prompt += f"Trang: {similar_info['Page']}\nNội dung: {similar_info['content']}\n"
    user_prompt += 'Hãy trả lời câu hỏi:\n'
    user_prompt += user_question
    return user_prompt

def get_user_prompt(input_model='all-MiniLM-L6-v2', num_sim_docx=5, user_question = '',temp_path = None) ->str:
    user_question, similar_infos = find_information(input_model=input_model, k=num_sim_docx,user_question=user_question,temp_path=temp_path)
    #todo: identify if metadatas if of docx or csv or md
    keys = list(similar_infos[0].keys())
    
    if 'title' in keys:
        user_prompt = get_user_prompt_docx(user_question=user_question, similar_infos=similar_infos)
    elif 'Mã số' in keys:
        user_prompt = get_user_prompt_csv(user_question=user_question, similar_infos=similar_infos)
    else:
        user_prompt = get_user_prompt_md(user_question=user_question, similar_infos=similar_infos)

    return user_prompt

def respond_user(user_question,temp_path):
    user_prompt = get_user_prompt(input_model='all-MiniLM-L6-v2', num_sim_docx=5, user_question=user_question,temp_path=temp_path)
    client = genai.Client(api_key= GOOGLE_API)
    os.environ["GEMINI_API_KEY"] = GOOGLE_API
    response = client.models.generate_content(
        model="gemini-2.5-flash", contents=user_prompt
    )
    return response.text
