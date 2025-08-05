from core.receiver import find_information
from langchain.llms.base import LLM
from typing import Optional, List
from openai import OpenAI
#get user question and similar information -> create a prompt for LLM
def get_user_prompt(input_model='all-MiniLM-L6-v2', num_sim_docx=5, user_question = '',temp_path = None) ->str:
    user_question, similar_info = find_information(input_model=input_model, k=num_sim_docx,user_question=user_question,temp_path=temp_path)
    #get title and text in similar_info
    metadatas = []
    for el in similar_info:
        metadata = {
            'title': el['title'],
            'text': el['text']
        }
        metadatas.append(metadata)
    user_prompt = 'Từ các thông tin sau:\n'
    for el in metadatas:
        user_prompt += f"Tiêu đề: {el['title']}\nNội dung: {el['text']}\n"
    user_prompt += 'Hãy trả lời câu hỏi:\n'
    user_prompt += user_question

    return user_prompt

# #todo: call a LLM API then return output
# def call_llm_api(embedding_model='all-MiniLM-L6-v2', num_sim_docx=5, LLM_model="gpt-3.5-turbo", api_key="what do you expected? call your own API"):
#     openai.api_key = api_key
#     user_prompt = get_user_prompt(input_model=embedding_model, num_sim_docx=num_sim_docx)
#     sys_prompt = "Bạn là một trợ lý AI có khả năng truy xuất thông tin trong tài liệu mà người dùng cung cấp. Từ những thông tin đó, bạn trả lời câu hỏi mà người dùng đưa ra"
#     response = openai.ChatCompletion.create(
#         model=LLM_model,
#         messages=[
#             {"role": "system", "content": sys_prompt},
#             {"role": "user", "content": user_prompt}
#         ],
#         max_tokens=512,
#         temperature=0.7
#     )
#     return response.choices[0].message['content']

import os
from huggingface_hub import InferenceClient

def respond_user(user_question,temp_path):
    user_prompt = get_user_prompt(input_model='all-MiniLM-L6-v2', num_sim_docx=5, user_question=user_question,temp_path=temp_path)

    # client = InferenceClient (
    #     provider="nebius",
    #     api_key="",
    # )

    # completion = client.chat.completions.create(
    #     model="deepseek-ai/DeepSeek-R1-0528",
    #     messages=[
    #         {
    #             'role': "system",
    #             'content': 'Bạn là một trợ lý AI có khả năng truy xuất thông tin trong tài liệu mà người dùng cung cấp. Từ những thông tin đó, bạn trả lời câu hỏi mà người dùng đưa ra'
    #         },

    #         {
    #             "role": "user",
    #             "content": user_prompt
    #         }
    #     ],
    # )
    model= "phogpt-4b-chat"
    base_url="http://localhost:1234/v1"
    api_key = ""  # bất kỳ chuỗi nào
    temperature = 0.7


    client = OpenAI(base_url=base_url, api_key=api_key)
    response = client.chat.completions.create(
        model= model,
        messages=[
            {"role": "system", "content": "Bạn là một chuyên gia tài chính."},
            {"role": "user", "content": user_prompt}
        ],
        temperature=temperature
    )
    print(user_prompt)
    return response.choices[0].message.content
    # print(user_prompt)
    # return (completion.choices[0].message.content)
