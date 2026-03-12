import numpy as np
import json

store = [] # une liste de dictionnaire

def add_chunks(chunks: list[str], embeddings: list[list[float]]):
    # ajouter chaque chunk + son vecteur dans store
    for i, chunk in enumerate(chunks): # me donne l'index "i" et la valeur "chunk" en même temps
        store.append({"id": f"chunk_{i}", "text": chunk, "vector": embeddings[i]})


def cosine_similarity(a: list[float], b: list[float]) -> float:
    # calculer la similarité cosinus entre a et b
    a = np.array(a)
    b = np.array(b)

    # produit scalaire  -> np.dot(a, b)
    # norme d'un vecteur -> np.linalg.norm(a)
    #similarity = (A · B) / (||A|| × ||B||)

    similarity = np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
    
    return similarity

def search(query_embedding: list[float], n_results: int = 3) -> list[str]:
    # 1. Calculer la similarité entre query_embedding et chaque vecteur du store
    # 2. trier par similarité décroissante et retourner les n_results chunks les plus similaires
    
    similarity = []

    for item in store: # item = chaque dictionnaire un par un
        X = cosine_similarity(query_embedding, item["vector"])
        similarity.append({"text": item["text"], "score": X})

    similarity = sorted(similarity, key=lambda x: x["score"], reverse=True) # je précise avec la clé "score" sur quoi trier   ;   reverse=True car sinon tri croissant

    return [r["text"] for r in similarity[:n_results]]

#store[0] = {        # ← chaque élément est un dictionnaire
#    "id": "chunk_0",
#    "text": "Le chat mange...",
#    "vector": [0.32, -0.91, ...]
#}


# On va sauvegarder le vector store sur disque pour ne pas re-embedder à chaque lancement et gagner du temps sur la deuxième requête

# Sauvegarde
def save_store(filepath: str = "store.json"):
    with open("store.json", "w") as f:
        json.dump(store, f)

# Charger
def load_store(filepath: str = "store.json"):
    global store # le store que je modifie ici, c'est le store global pas une nouvelle variable locale
    with open("store.json", "r") as f:
        store = json.load(f)