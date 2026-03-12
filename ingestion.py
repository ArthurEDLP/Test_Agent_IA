import fitz # PyMuPDF

def load_document(filepath: str) -> str:
    extension = filepath.split(".")[-1]

    if extension =="txt":
        with open(filepath, "r", encoding="utf-8") as f: # "r": mode de lecture (read)
            return f.read()

    elif extension =="pdf":
        doc = fitz.open(filepath) # ouvre le PDF
        text = ""
        for page in doc: # boucle sur chaque page
            text += page.get_text() # extrait le texte brut
        return text

def chunk_text(text: str, chunk_size: int=500, overlap: int=50) -> list[str]:
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size # (0 + 500 ; 450 + 500)
        chunk = text[start:end]
        chunks.append(chunk)
        start = end - overlap # le prochian découpage commencera légèrement avant la fin de ce découpage (0-> 500 ; 450 -> 950 ; 900 -> 1400)

    return chunks

