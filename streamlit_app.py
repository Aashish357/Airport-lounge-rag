import streamlit as st
import numpy as np
import os
from groq import Groq

st.set_page_config(page_title="Airport Lounge RAG", page_icon="✈️")

# Get API key safely
GROQ_API_KEY = st.secrets["GROQ_API_KEY"]

# Initialize client correctly
client = Groq(api_key=GROQ_API_KEY)

VECTOR_FILE = "rag/vectors.npy"
TEXT_FILE = "rag/chunks.txt"

@st.cache_resource
def load_data():
    vectors = np.load(VECTOR_FILE)
    with open(TEXT_FILE, "r") as f:
        chunks = f.read().split("\n---\n")
    return vectors, chunks

vectors, chunks = load_data()

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

st.title("✈️ Airport Lounge Assistant")
st.write("Ask anything about lounge policies, booking, access rules, etc.")

query = st.text_input("Ask your question:")

if query:
    np.random.seed(abs(hash(query)) % (10**6))
    query_vector = np.random.rand(vectors.shape[1])

    scores = [cosine_similarity(query_vector, v) for v in vectors]
    top_index = np.argmax(scores)

    context = chunks[top_index]

    prompt = f"""
You are an airport lounge assistant.
Use the context below to answer clearly.

Context:
{context}

Question:
{query}
"""

    response = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )

    answer = response.choices[0].message.content
    st.markdown("### 🧠 Answer")
    st.write(answer)
