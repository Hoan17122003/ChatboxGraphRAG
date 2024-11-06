# main.py
from fastapi import FastAPI, Query, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any
from vector_store import insert_document, retrieve_similar_documents
from graph_retriever import retrieve_related_entities
from llama_integration import generate_response


import tracemalloc

# Bắt đầu theo dõi việc cấp phát bộ nhớ
tracemalloc.start()

# Lấy thông tin về các đối tượng đang chiếm nhiều bộ nhớ nhất
snapshot = tracemalloc.take_snapshot()
top_stats = snapshot.statistics('lineno')

print("[ Top 10 memory consuming lines ]")
for stat in top_stats[:10]:
    print(stat)


# app = FastAPI()

# Định nghĩa Pydantic model cho tài liệu
# class Document(BaseModel):
#     id: str
#     text: str
#     metadata: Dict[str, Any]

documents = [
    {
        "id": "doc1",
        "text": "ChatGPT là một mô hình ngôn ngữ lớn do OpenAI phát triển, được sử dụng để xây dựng các ứng dụng chatbot và xử lý ngôn ngữ tự nhiên.",
        "metadata": {"author": "OpenAI", "created_at": "2023-01-01", "topic": "AI & NLP"}
    },
    {
        "id": "doc2",
        "text": "LangChain là một thư viện mã nguồn mở cho phép phát triển các ứng dụng AI bằng cách kết hợp các mô hình ngôn ngữ lớn với nhau.",
        "metadata": {"author": "LangChain", "created_at": "2023-02-01", "topic": "Framework"}
    },
    {
        "id": "doc3",
        "text": "MongoDB là một cơ sở dữ liệu NoSQL mạnh mẽ, thường được sử dụng để lưu trữ dữ liệu không cấu trúc hoặc bán cấu trúc.",
        "metadata": {"author": "MongoDB Inc.", "created_at": "2023-03-01", "topic": "Database"}
    },
    {
        "id": "doc4",
        "text": "LLaMA là một mô hình ngôn ngữ tạo văn bản được Meta phát triển để xử lý ngôn ngữ tự nhiên.",
        "metadata": {"author": "Meta", "created_at": "2023-04-01", "topic": "Model"}
    },
    {
        "id": "doc5",
        "text": "Neo4j là một cơ sở dữ liệu đồ thị nổi tiếng, thường được sử dụng để lưu trữ và phân tích dữ liệu dạng đồ thị.",
        "metadata": {"author": "Neo4j Inc.", "created_at": "2023-05-01", "topic": "Database"}
    }
]


# @app.post("/add_document")
async def add_document(document: any):
        # Chèn tài liệu vào vector_store
        insert_document(documents)
        return {"status": "Document inserted"}


# @app.get("/query")
async def query(q: str ):
        # Truy xuất tài liệu từ MongoDB
        similar_docs = retrieve_similar_documents(q)
        
        # Truy xuất các thực thể liên quan từ Neo4j
        entities = retrieve_related_entities(q)
        
        # Tạo phản hồi từ mô hình LLaMA 2
        context = "\n".join(similar_docs) + "\n" + "\n".join([f"{e['name']} ({e['relation']})" for e in entities])
        response = generate_response(q, context)
        
        return {"response": response}
   

add_document(documents)
query(input("query : "))

tracemalloc.stop()