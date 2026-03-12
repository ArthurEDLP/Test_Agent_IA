import requests
from retriever import retrieve

OLLAMA_URL = "http://localhost:11434/api/chat"
LLM_MODEL = "llama3"

# ollama pull llama3

def ask(question: str, historique: list = []) -> str:
    # 1. récupérer les chunks pertinents avec retrieve()
    # 2. construire un prompt avec les chunks et la question
    # 3. ajouter l'historique de discussion
    # 4. appeler Ollama (on envoie le prompt au modèle llama3)

    contexte = retrieve(question)    

    # 2)
    prompt = f"""
    Tu es un assistant expert en lecture de documents.
    Réponds uniquement à partir du contexte suivant.
    Si la réponse n'est pas dans le contexte, dis-le.

    Contexte:
    {"\n".join(contexte)}

    Question : {question}

    """
    # 3)
    historique.append({"role": "user", "content": prompt + f"\nQuestion : {question}"})

    # 4)

    # Strucuture similaire à l'embedding, mais différente car ici on fait un chat
    # Embedding: on envoie un prompt, on reçoit un vecteur
    # Chat : on envoie un message, on reçoit du texte

    reponse = requests.post( 
        OLLAMA_URL,
        json = {
            "model": LLM_MODEL,
            "messages": historique,
            "stream": False
        }
    )

    result = reponse.json()
    texte = result["message"]["content"]

    historique.append({"role": "assistant", "content": texte})

    return texte