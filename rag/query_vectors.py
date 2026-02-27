import os
from dotenv import load_dotenv
import chromadb
from sentence_transformers import SentenceTransformer
from groq import Groq

# ===============================
# LOAD ENV
# ===============================
load_dotenv()

# ===============================
# CONFIG
# ===============================
CHROMA_PATH = "chroma_db"
COLLECTION_NAME = "lounge_docs"
TOP_K = 5

# ===============================
# INITIALIZE
# ===============================
# Chroma
client = chromadb.PersistentClient(path=CHROMA_PATH)
collection = client.get_collection(name=COLLECTION_NAME)

# Embedding model
embed_model = SentenceTransformer("all-MiniLM-L6-v2")

# Groq LLM client
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# ===============================
# MAIN LOOP
# ===============================
while True:
    query = input("\nAsk something (type 'exit' to quit): ")

    if query.lower() == "exit":
        break

    if not query.strip():
        continue

    try:
        # 1️⃣ Embed Query
        query_embedding = embed_model.encode(query)

        # 2️⃣ Retrieve from Chroma
        results = collection.query(
            query_embeddings=[query_embedding.tolist()],
            n_results=TOP_K,
            include=["documents"]
        )

        docs = results["documents"][0]

        if not docs:
            print("\n⚠️ No relevant information found in the lounge database.\n")
            continue

        # 3️⃣ Build Context
        context = "\n\n".join(docs)

        # 4️⃣ Strong Prompt
        prompt = f"""
You are an expert airport lounge operations assistant.

Use ONLY the context provided below to answer the user's question.
Provide a clear, structured, and professional response in complete sentences.

If the answer is not explicitly mentioned in the context, say exactly:
"I don't have that information in the lounge policy database."

Context:
{context}

User Question:
{query}

Answer:
"""

        # 5️⃣ Call Groq LLM
        response = groq_client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "You are a professional airport lounge policy assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )

        final_answer = response.choices[0].message.content

        print("\n🧠 AI Generated Answer:\n")
        print(final_answer)
        print("\n--------------------------------")

    except Exception as e:
        print(f"\n❌ Error occurred: {e}\n")