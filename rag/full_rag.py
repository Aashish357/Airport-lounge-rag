from dotenv import load_dotenv
import os
import chromadb
import numpy as np
from sentence_transformers import SentenceTransformer

# ===============================
# LOAD ENV (not required now but safe)
# ===============================

load_dotenv()

# ===============================
# CONFIG
# ===============================

CHROMA_PATH = "chroma_db"
COLLECTION_NAME = "lounge_docs"

MIN_SIMILARITY = 0.45
TOP_K = 3

LOUNGE_KEYWORDS = [
    "lounge", "guest", "access", "policy",
    "food", "timing", "membership",
    "entry", "services", "wifi", "baggage",
    "airport", "boarding", "complimentary",
    "pnr", "card", "bin", "payment", "delay",
    "cost", "price", "refund"
]

# ===============================
# INITIALIZE
# ===============================

client = chromadb.PersistentClient(path=CHROMA_PATH)
collection = client.get_collection(name=COLLECTION_NAME)

embed_model = SentenceTransformer("all-MiniLM-L6-v2")

# ===============================
# UTILITY
# ===============================

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def is_lounge_related(query):
    return any(word in query.lower() for word in LOUNGE_KEYWORDS)

# ===============================
# MAIN LOOP
# ===============================

while True:
    query = input("\nAsk something (type 'exit' to quit): ")

    if query.lower() == "exit":
        break

    # 1️⃣ Domain Guard
    if not is_lounge_related(query):
        print("\n⚠️ I can only answer airport lounge related questions.\n")
        continue

    # 2️⃣ Embed Query
    q_emb = embed_model.encode(query)

    # 3️⃣ Retrieve from Chroma
    results = collection.query(
        query_embeddings=[q_emb.tolist()],
        n_results=5,
        include=["documents", "embeddings"]
    )

    docs = results["documents"][0]
    embeddings = results["embeddings"][0]

    if not docs:
        print("\nNo relevant information found.\n")
        continue

    # 4️⃣ Cosine Similarity Filtering
    scored = []

    for doc, emb in zip(docs, embeddings):
        sim = cosine_similarity(q_emb, np.array(emb))
        scored.append((sim, doc))

    scored.sort(reverse=True, key=lambda x: x[0])

    filtered_docs = [doc for sim, doc in scored if sim >= MIN_SIMILARITY]

    if not filtered_docs:
        print("\n⚠️ That question seems unrelated to lounge services.\n")
        continue

    # 5️⃣ Return Best Match
    best_answer = filtered_docs[0]

    print("\n🧠 Retrieved Answer:\n")
    print(best_answer)
    print("\n--------------------------------")