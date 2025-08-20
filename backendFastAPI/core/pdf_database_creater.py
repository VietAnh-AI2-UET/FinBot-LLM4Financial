from core.pdf_reader import get_md_content
from sentence_transformers import SentenceTransformer
import numpy as np
import faiss

def get_embedding_vector(md_contents: list[dict], embedding_model='all-MiniLM-L6-v2') -> tuple:
    model = SentenceTransformer(embedding_model)
    embeddings = []
    metadatas = []

    for md_content in md_contents:
        vector = model.encode(md_content['content'])
        embeddings.append(vector)
        metadatas.append(md_content)

    return embeddings, metadatas

def create_database_for_pdf(embedding_model='all-MiniLM-L6-v2') -> tuple:
    md_contents = get_md_content()
    embeddings, metadatas = get_embedding_vector(md_contents=md_contents, embedding_model=embedding_model)

    # convert to numpy
    embedding_matrix = np.stack(embeddings).astype("float32")
    faiss.normalize_L2(embedding_matrix)

    # FAISS index
    dimension = embedding_matrix.shape[1]
    index = faiss.IndexFlatIP(dimension)
    index.add(embedding_matrix)
    print('database created')
    return index, metadatas