import requests

OLLAMA_URL = "http://localhost:11434/api/embeddings"
EMBED_MODEL = "mxbai-embed-large"

# ollama pull mxbai-embed-large

def get_embedding(text: str) ->list[float]:
    # on fait un POST sur OLLAMA_URL avec le bon body
    response = requests.post(
        OLLAMA_URL,
        json = {
            "model": EMBED_MODEL,
            "prompt": text
        }
    )
    result = response.json()
    return result["embedding"] # On extrait "embedding" de la réponse JSON