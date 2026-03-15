import json
import os
import numpy as np

# A simple vector store using numpy for distance calculations
# This avoids needing a full database for the prototype phase

STORAGE_FILE = "app/memory/vectors.json"
EMBEDDINGS_FILE = "app/memory/embeddings.npy"

# Global cache for documents and their embeddings
_documents = []
_embeddings = None

def _get_embedding(text):
    # This is a placeholder for a real embedding model
    # In a real setup, we would use sentence-transformers:
    # from sentence_transformers import SentenceTransformer
    # model = SentenceTransformer('all-MiniLM-L6-v2')
    # return model.encode(text)
    
    # For now, let's use a dummy embedding based on character counts 
    # (just to make the code functional without heavy imports)
    vec = np.zeros(384) # Standard MiniLM size
    for char in text:
        vec[ord(char) % 384] += 1
    norm = np.linalg.norm(vec)
    return vec / norm if norm > 0 else vec

def add_documents(docs):
    global _documents, _embeddings
    
    new_vectors = []
    for doc in docs:
        _documents.append(doc)
        new_vectors.append(_get_embedding(doc["text"]))
    
    if _embeddings is None:
        _embeddings = np.array(new_vectors)
    else:
        _embeddings = np.vstack([_embeddings, np.array(new_vectors)])
        
    # Save to disk
    with open(STORAGE_FILE, "w") as f:
        json.dump(_documents, f)
    np.save(EMBEDDINGS_FILE, _embeddings)
    print(f"Added {len(docs)} documents to vector store.")

def search(query, top_k=2):
    global _documents, _embeddings
    
    if _embeddings is None:
        if os.path.exists(STORAGE_FILE) and os.path.exists(EMBEDDINGS_FILE):
            with open(STORAGE_FILE, "r") as f:
                _documents = json.load(f)
            _embeddings = np.load(EMBEDDINGS_FILE)
        else:
            return []
            
    query_vec = _get_embedding(query)
    
    # Cosine similarity using dot product (vectors are normalized)
    similarities = np.dot(_embeddings, query_vec)
    top_indices = np.argsort(similarities)[::-1][:top_k]
    
    results = []
    for idx in top_indices:
        results.append({
            "document": _documents[idx],
            "score": float(similarities[idx])
        })
    return results
