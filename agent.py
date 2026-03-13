import requests
from retriever import retrieve
from openai import AzureOpenAI
import os

AZURE_ENDPOINT = os.getenv("AZURE_ENDPOINT")
AZURE_KEY      = os.getenv("AZURE_KEY")
LLM_MODEL = os.environ.get("LLM_MODEL")

client = AzureOpenAI(
    azure_endpoint=AZURE_ENDPOINT,
    api_key=AZURE_KEY,
    api_version="2024-02-15-preview"
)

def ask(question: str, historique: list = []) -> str:
    # 1. récupérer les chunks pertinents avec retrieve()
    # 2. construire un prompt avec les chunks et la question
    # 3. ajouter l'historique de discussion
    # 4. appeler Ollama (on envoie le prompt au modèle llama3)

    contexte = retrieve(question)    

    contexte_hist = "\n".join(contexte)

    # 2)
    prompt = f"""
    Tu es un assistant expert en lecture de documents.
    Réponds uniquement à partir du contexte suivant.
    Si la réponse n'est pas dans le contexte, dis-le.

    Contexte:
    {contexte_hist}

    Question : {question}

    """
    # 3)
    historique.append({"role": "user", "content": prompt})

    # 4)

    # Strucuture similaire à l'embedding, mais différente car ici on fait un chat
    # Embedding: on envoie un prompt, on reçoit un vecteur
    # Chat : on envoie un message, on reçoit du texte

    reponse = client.chat.completions.create( 
        model=LLM_MODEL,
        messages=historique
    )

    texte = reponse.choices[0].message.content

    historique.append({"role": "assistant", "content": texte})

    return texte