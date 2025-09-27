import pandas as pd
import json
import hashlib

from langchain.vectorstores import FAISS
from langchain.docstore.document import Document

from utils.call_models import get_embedding_model
from utils.config import CONFIG

EMBEDDING_MODEL = CONFIG["EMBEDDING_MODEL"]

# Example CSV
file = "/home/mayank/Documents/personal/visualisation-charts/data/Amazon Customer Behavior Survey.csv"
df = pd.read_csv(file)

# Extract schema
schema_text = "\n".join([f"{col}: {str(dtype)}" for col, dtype in df.dtypes.items()])
print('*'*50)
print(schema_text)

# Chunk schema + KB
def chunk_text(text, size=300):
    return [text[i:i+size] for i in range(0, len(text), size)]

def get_chunk_id(text: str, file_name: str, chunk_idx: int) -> str:
    hash_digest = hashlib.md5(text.encode("utf-8")).hexdigest()[:8]
    return f"{file_name}_chunk{chunk_idx}_{hash_digest}"

chunks = chunk_text(schema_text)
docs = [Document(page_content=chunk, metadata={"id": get_chunk_id(chunk, file, i)}) 
        for i, chunk in enumerate(chunks)]

# Add KB patterns

with open("kb_visualization.json") as f:
    kb_patterns = json.load(f)

for i, pattern in enumerate(kb_patterns):
    docs.append(Document(page_content=json.dumps(pattern), metadata={"id": f"kb_{i}"}))

# Store in FAISS
embeddings = get_embedding_model(EMBEDDING_MODEL)
vectorstore = FAISS.from_documents(docs, embeddings)
vectorstore.save_local("/home/mayank/Documents/personal/visualisation-charts/vec_store/faiss_store")
