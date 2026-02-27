from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import os

os.environ["HF_HUB_OFFLINE"] = "1"

model = SentenceTransformer(
    "all-MiniLM-L6-v2",
    device="cpu"
)

sentences = [
    # card
    "card details",
    "credit card information",
    "debit card issue",
    "card not working",

    # flight
    "flight delay",
    "is my flight delayed",
    "flight status",
    "boarding time update",

    # lounge
    "lounge access",
    "can I enter lounge",
    "lounge availability",
    "lounge session status",

    # payment
    "payment status",
    "order payment failed",
    "transaction pending",
    "payment order id",
    "refund details of payment"
]

labels = [
    "card", "card", "card", "card",
    "flight", "flight", "flight", "flight",
    "lounge", "lounge", "lounge", "lounge",
    "payment", "payment", "payment", "payment", "payment"
]

embeddings = model.encode(sentences, normalize_embeddings=True)

def classify(query, threshold=0.45):
    q_emb = model.encode([query], normalize_embeddings=True)
    sims = cosine_similarity(q_emb, embeddings)[0]
    best_idx = int(np.argmax(sims))

    if sims[best_idx] < threshold:
        return "unknown"

    return labels[best_idx]



