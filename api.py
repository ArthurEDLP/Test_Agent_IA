from flask import Flask, request, jsonify
from agent import ask
import os
from ingestion import load_document, chunk_text
from embedder import get_embedding
from vector_store import add_chunks, save_store, load_store
from flask_cors import CORS

app = Flask(__name__) # création d'un serveur web stocké dans app
CORS(app)
app.config['JSON_ENSURE_ASCII'] = False

if os.path.exists("store.json"):
    load_store()
else:
    # initialisation au démarrage
    chunks = []
    for fichier in os.listdir('documents/'):
        texte = load_document(f"documents/{fichier}")
        chunks += chunk_text(texte)
    # on sauvegarde en dehors de la boucle, une fois que tout les doc sont importés    
    embeddings = [get_embedding(chunk) for chunk in chunks]
    add_chunks(chunks, embeddings)
    save_store()

historique = []

@app.route("/ask", methods=["POST"]) # Quand quelqu'un envoie un POST sur /ask, exécute la fonction juste en dessous
def handle_question():
    # Extraire la question du body
    data = request.json
    question = data["question"]

    reponse = ask(question, historique)

    return jsonify({"reponse": reponse})

app.run(port=5000)