from embedder import get_embedding
from vector_store import search

def retrieve(question: str, n_results: int = 3) -> list[str]:

    text = get_embedding(question) # on transforme la question en vecteur

    result = search(text, n_results) # on cherche les chunks les plus proches
    
    return result