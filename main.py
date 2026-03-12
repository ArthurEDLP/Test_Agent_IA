from ingestion import load_document, chunk_text
from embedder import get_embedding
from vector_store import add_chunks
from agent import ask

texte = load_document("documents/mon_fichier.pdf")

chunks = chunk_text(texte)

embeddings = []
for chunk in chunks:
    embeddings.append(get_embedding(chunk))

# stocke dans le vector store
add_chunks(chunks, embeddings)

while True:
    question = input("Question : ")
    if question == "exit":
        break
    reponse = ask(question)
    print(reponse)

# python install pymupdf numpy requests