from dotenv import load_dotenv

load_dotenv()
from flask import Flask, request, jsonify
from agent import ask
import os
from ingestion import load_document, chunk_text
from embedder import get_embedding
from vector_store import add_chunks, save_store, load_store
from flask_cors import CORS


app = Flask(__name__)
CORS(app)
app.config['JSON_ENSURE_ASCII'] = False

if os.path.exists("store.json"):
    load_store()
else:
    chunks = []
    for fichier in os.listdir('documents/'):
        texte = load_document(f"documents/{fichier}")
        chunks += chunk_text(texte)
    embeddings = [get_embedding(chunk) for chunk in chunks]
    add_chunks(chunks, embeddings)
    save_store()

# Historique par session : on le stocke dans un dict pour éviter
# de mélanger les conversations si plusieurs onglets sont ouverts
historiques = {}

@app.route("/ask", methods=["POST"])
def handle_question():
    data = request.json

    if not data or "question" not in data:
        return jsonify({"error": "Champ 'question' manquant"}), 400

    question = data["question"]
    session_id = data.get("session_id", "default")  # optionnel, pour multi-sessions

    if session_id not in historiques:
        historiques[session_id] = []

    try:
        reponse = ask(question, historiques[session_id])
        return jsonify({"reponse": reponse})
    except Exception as e:
        print(f"[ERREUR] {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":  # ← FIX PRINCIPAL : app.run() doit être ici
    app.run(host="0.0.0.0", port=5000, debug=True)
