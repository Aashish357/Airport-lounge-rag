import os
from pathlib import Path
from flask import Flask, request, jsonify
from dotenv import load_dotenv

# =====================================================
# 🔹 FORCE LOAD .env
# =====================================================
BASE_DIR = Path(__file__).parent
ENV_PATH = BASE_DIR / ".env"
load_dotenv(dotenv_path=ENV_PATH)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise RuntimeError("❌ GROQ_API_KEY not found in .env")

print("✅ GROQ_API_KEY loaded successfully")

# =====================================================
# 🔹 LLM (STABLE)
# =====================================================
from langchain_groq import ChatGroq
from langchain.schema import HumanMessage

llm = ChatGroq(
    groq_api_key=GROQ_API_KEY,
    model="llama-3.3-70b-versatile",
    temperature=0
)

# =====================================================
# 🔹 SIMPLE RAG (NO DEPENDENCY ON rag MODULE)
# =====================================================
def load_rag_documents_safe(folder="rag_knowledge"):
    docs = []
    rag_path = BASE_DIR / folder

    if not rag_path.exists():
        print("⚠️ RAG folder not found, continuing without RAG")
        return docs

    for file in rag_path.glob("**/*.md"):
        try:
            docs.append(file.read_text(encoding="utf-8"))
        except Exception:
            pass

    return docs


def rag_search_safe(query, docs):
    query = query.lower()
    matches = []

    for doc in docs:
        if any(word in doc.lower() for word in query.split()):
            matches.append(doc)

    return "\n\n".join(matches[:2])  # limit context


rag_docs = load_rag_documents_safe()
print(f"✅ RAG loaded with {len(rag_docs)} documents")

# =====================================================
# 🔹 OFFLINE INTENT CLASSIFIER
# =====================================================
from rag.offline_model import classify

# =====================================================
# 🔹 FLASK APP
# =====================================================
app = Flask(__name__)

@app.route("/query", methods=["POST"])
def query():
    data = request.get_json()
    user_query = data.get("msg", "").strip()

    if not user_query:
        return jsonify({"error": "msg is required"}), 400

    intent = classify(user_query)

    rag_context = ""
    if intent in ["card", "lounge"] and rag_docs:
        rag_context = rag_search_safe(user_query, rag_docs)

    final_prompt = f"""
You are an AI assistant for airport lounge services.

Intent: {intent}

Relevant policy information:
{rag_context}

User question:
{user_query}

Answer clearly, politely, and accurately.
"""

    response = llm.invoke([
        HumanMessage(content=final_prompt)
    ])

    return jsonify({
        "intent": intent,
        "result": response.content
    }), 200


# =====================================================
# 🔹 RUN SERVER
# =====================================================
if __name__ == "__main__":
    app.run(debug=True, port=8000, use_reloader=False)
