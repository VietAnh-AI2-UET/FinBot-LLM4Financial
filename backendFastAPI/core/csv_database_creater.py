from csv_table_reader import get_dataframe
from sentence_transformers import SentenceTransformer

def get_embedding_vector(df, embedding_model='all-MiniLM-L6-v2') -> tuple:
    model = SentenceTransformer(embedding_model)
    embedding = []
    metadatas = []

    for idx, row in df.iterrows():
        vector = model.encode(row['Hạng mục'])
        embedding.append(vector)
        metadatas.append(
            {
                'Hạng mục': row['Hạng mục'],
                'Mã số': row['Mã số'],
                'Giá trị': row['Giá trị']
            }
        )
    return embedding, metadatas
