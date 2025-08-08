from core.receiver import find_information
from huggingface_hub import InferenceClient

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

def respond_user(user_question,temp_path):
    user_prompt = get_user_prompt(input_model='all-MiniLM-L6-v2', num_sim_docx=5, user_question=user_question,temp_path=temp_path)

    client = InferenceClient (
        provider="nebius",
        # them api key để chạy
    )

    completion = client.chat.completions.create(
        model="deepseek-ai/DeepSeek-R1-0528",
        messages=[
            {
                'role': "system",
                'content': 'Bạn là một trợ lý AI có khả năng truy xuất thông tin trong tài liệu mà người dùng cung cấp. Từ những thông tin đó, bạn trả lời câu hỏi mà người dùng đưa ra nếu câu hỏi không có trong tài liệu hãy nói thẳng '
            },

            {
                "role": "user",
                "content": user_prompt
            }
        ],
    )
    
    # print(user_prompt)
    return (completion.choices[0].message.content)
