# db_config.py
import os
from pymongo import MongoClient
from neo4j import GraphDatabase
from dotenv import load_dotenv


load_dotenv()

# Kết nối MongoDB
MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client.graphRAG  # Tên database
documents_collection = db.documents  # Tên collection


neo4j_uri = os.getenv("NEO4J_URI")
print(f"neo4j {neo4j_uri}")
# Kết nối Neo4j
neo4j_user = os.getenv("NEO4J_USER")
neo4j_password = os.getenv("NEO4J_PASSWORD")
neo4j_driver = GraphDatabase.driver(neo4j_uri, auth=(neo4j_user, neo4j_password))
