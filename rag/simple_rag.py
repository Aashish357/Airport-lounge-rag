import os

def load_knowledge():
    base = "rag/knowledge"
    text = ""
    for file in os.listdir(base):
        if file.endswith(".txt"):
            with open(os.path.join(base, file), "r") as f:
                text += f.read() + "\n"
    return text

def get_rag_context(query: str) -> str:
    knowledge = load_knowledge()
    words = query.lower().split()

    matches = []
    for line in knowledge.split("\n"):
        if any(w in line.lower() for w in words):
            matches.append(line)

    return "\n".join(matches[:8])
