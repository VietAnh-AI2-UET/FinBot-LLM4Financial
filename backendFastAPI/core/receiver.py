from core.docx_database_creater import create_database
from sentence_transformers import SentenceTransformer
import os

#read input file
def get_input_path() -> str:
    try:
        base_dir = os.path.dirname(__file__)
        input_path = os.path.abspath(os.path.join(base_dir, '..', '000000014601738_VI_BaoCaoTaiChinh_KiemToan_2024_HopNhat_14032025110908.docx'))
        return input_path
    
    except Exception as e:
        print('cant locate docx file')
        print(f'error: {e}')

#get vector database and metadatas
def get_database(input_model='all-MiniLM-L6-v2',temp_path=None) -> tuple:
    if temp_path is None:
        input_path = get_input_path()
    input_path = temp_path
    
    try:
        index, metadatas = create_database(input_path=input_path, input_model=input_model)
        return index, metadatas

    except Exception as e:
        print('cant get database')
        print(f'error: {e}')

#get user prompt
def get_user_question() -> str:
    user_question = input('What do you want to know: ')
    return user_question

#embedd user question into a vector
def get_user_question_embedding(input_model='all-MiniLM-L6-v2', user_question = '') -> tuple:
    user_question = user_question
    model = SentenceTransformer(input_model)
    user_question_embeddings = model.encode([user_question])
    return user_question, user_question_embeddings[0]

#find k similar information in vector database
def find_information(input_model='all-MiniLM-L6-v2', k=5, user_question = '',temp_path = None) -> tuple:
    user_question, user_question_vector = get_user_question_embedding(input_model=input_model, user_question = user_question)
    index, metadatas = get_database(input_model='all-MiniLM-L6-v2',temp_path = temp_path)

    #search for similar information in FAISS database
    D, I = index.search(user_question_vector.reshape(1, -1), k)  # D: distances, I: indices
    
    similar_info = []
    for idx in I[0]:
        similar_info.append(metadatas[idx])
    return user_question, similar_info