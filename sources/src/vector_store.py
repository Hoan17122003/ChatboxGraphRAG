from db_config import documents_collection
from datetime import date
from pymongo import MongoClient
import numpy as np
from langchain.embeddings import OpenAIEmbeddings
# from src.main import Document

def insert_document(text:any):
    # Chuyển đổi văn bản thành vector embedding
    embedding = OpenAIEmbeddings.from_text(text)
    
    # Tạo tài liệu mới với embedding
    # document = {
    #     "text": text,
    #     "embedding": embedding.tolist(),  # Lưu vector dưới dạng danh sách
    #     "metadata": {
    #         "author": author,
    #         "date" : date.today()
    #     }
    # }
    document = {
        **text
    }
    embeddingField = {
        embedding
    }
    document.update(embedding)

    
    # Thêm tài liệu vào MongoDB
    documents_collection.insert_one(document)
    print("Document inserted into MongoDB.")


def retrieve_similar_documents(query: str, top_k: int = 5):
    # Chuyển đổi truy vấn thành vector embedding
    query_embedding = OpenAIEmbeddings.from_text(query)
    
    # Lấy tất cả các tài liệu từ MongoDB và tính toán độ tương đồng cosine
    documents = list(documents_collection.find())
    
    # Tính độ tương đồng cosine giữa query và từng document
    def cosine_similarity(v1, v2):
        return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))
    
    # Tạo danh sách các tài liệu với độ tương đồng
    similar_docs = []
    for doc in documents:
        doc_embedding = np.array(doc["embedding"])
        similarity = cosine_similarity(query_embedding, doc_embedding)
        similar_docs.append((similarity, doc["text"]))
    
    # Sắp xếp theo độ tương đồng giảm dần và lấy top K
    similar_docs = sorted(similar_docs, key=lambda x: x[0], reverse=True)
    return [doc for _, doc in similar_docs[:top_k]]
