from core.csv_table_reader import get_dataframe
from sentence_transformers import SentenceTransformer
import numpy as np
import faiss

def get_embedding_vector(input_path=None, embedding_model='all-MiniLM-L6-v2') -> tuple:
    df = get_dataframe(input_path=input_path)

    model = SentenceTransformer(embedding_model)
    embeddings = []
    metadatas = []

    for idx, row in df.iterrows():
        vector = model.encode(row['Hạng mục'])
        embeddings.append(vector)
        metadatas.append(
            {
                'Hạng mục': row['Hạng mục'],
                'Mã số': row['Mã số'],
                'Giá trị': row['Giá trị']
            }
        )
    return embeddings, metadatas

def create_database_for_csv(input_path=None, embedding_model='all-MiniLM-L6-v2'):
    # Convert to numpy
    embeddings, metadatas = get_embedding_vector(input_path=input_path, embedding_model=embedding_model)
    embedding_matrix = np.stack(embeddings).astype("float32")
    faiss.normalize_L2(embedding_matrix)

    # FAISS index
    dimension = embedding_matrix.shape[1]
    index = faiss.IndexFlatIP(dimension)
    index.add(embedding_matrix)
    print('database created')
    return index, metadatas
