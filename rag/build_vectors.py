import os
import re
import chromadb
from sentence_transformers import SentenceTransformer

# ===============================
# CONFIG
# ===============================

DATA_FOLDER = "data"
CHROMA_PATH = "chroma_db"
COLLECTION_NAME = "lounge_docs"

CHUNK_SIZE = 500
CHUNK_OVERLAP = 100

# ===============================
# CLEAN TEXT
# ===============================

def clean_text(text):
    text = re.sub(r"\s+", " ", text)
    return text.strip()

# ===============================
# SMART CHUNKING WITH OVERLAP
# ===============================

def split_into_chunks(text, chunk_size=500, overlap=100):
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start += chunk_size - overlap

    return chunks

# ===============================
# LOAD DOCUMENTS
# ===============================

documents = []
metadatas = []

for file in os.listdir(DATA_FOLDER):
    if file.endswith(".txt"):
        with open(os.path.join(DATA_FOLDER, file), "r", encoding="utf-8") as f:
            content = clean_text(f.read())
            chunks = split_into_chunks(content, CHUNK_SIZE, CHUNK_OVERLAP)

            for i, chunk in enumerate(chunks):
                documents.append(chunk)
                metadatas.append({
                    "source": file,
                    "chunk_id": i
                })

print(f"Documents found: {len(documents)}")

# ===============================
# EMBEDDING MODEL
# ===============================

embed_model = SentenceTransformer("all-MiniLM-L6-v2")
embeddings = embed_model.encode(documents)

# ===============================
# STORE IN CHROMA (PERSISTENT)
# ===============================

client = chromadb.PersistentClient(path=CHROMA_PATH)

# Delete old collection if exists
try:
    client.delete_collection(name=COLLECTION_NAME)
except:
    pass

collection = client.create_collection(name=COLLECTION_NAME)

collection.add(
    documents=documents,
    embeddings=embeddings.tolist(),
    metadatas=metadatas,
    ids=[f"id_{i}" for i in range(len(documents))]
)

print("✅ Data stored persistently in Chroma.")