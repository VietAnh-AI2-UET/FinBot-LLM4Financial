from receiver import find_information

#get user question and similar information -> create a prompt for LLM
def get_prompt(input_model='all-MiniLM-L6-v2', k=5):
    user_question, similar_info = find_information(input_model=input_model, k=k)
    #get title and text in similar_info
    metadatas = []
    for el in similar_info:
        metadata = {
            'title': el['title'],
            'text': el['text']
        }
        metadatas.append(metadata)
    prompt = 'Từ các thông tin sau:\n'
    for el in metadatas:
        prompt += f"Tiêu đề: {el['title']}\nNội dung: {el['text']}\n"
    prompt += 'Hãy trả lời câu hỏi:\n'
    prompt += user_question

    return prompt

#todo: call a LLM API then return output