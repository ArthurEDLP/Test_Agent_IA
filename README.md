# Agent IA — Lecture de Documents

Agent RAG (Retrieval-Augmented Generation) pour interroger des documents PDF en langage naturel.

---

## Architecture

```
documents/          → tes fichiers PDF
ingestion.py        → lecture et découpage des documents
embedder.py         → transformation du texte en vecteurs (Azure OpenAI)
vector_store.py     → stockage et recherche vectorielle
retriever.py        → pont entre embedding et recherche
agent.py            → construction du prompt et appel au LLM
api.py              → serveur Flask (API HTTP)
index.html          → interface de chat
```

---

## Prérequis

- Python 3.12+
- Un compte Azure avec accès à **Azure OpenAI**
- Docker Desktop (pour le déploiement)

---

## Installation

### 1. Cloner le projet

```bash
git clone <url-du-repo>
cd agent-ia
```

### 2. Créer un environnement virtuel

```bash
python -m venv venv
venv\Scripts\Activate  # Windows
```

### 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

---

## Configuration Azure OpenAI

### 1. Créer les déploiements sur Azure

Rendez-vous sur https://oai.azure.com et créez deux déploiements :

| Déploiement | Modèle | Usage |
|---|---|---|
| `gpt-4o` | gpt-4o | LLM (chat) |
| `text-embedding` | text-embedding-ada-002 | Embeddings |

### 2. Créer le fichier `.env`

Créez un fichier `.env` à la racine du projet :

```
AZURE_ENDPOINT=https://votre-resource.openai.azure.com/
AZURE_KEY=votre_clé_api
DEPLOY_LLM=gpt-4o
DEPLOY_EMBED=text-embedding
```

Récupérez `AZURE_ENDPOINT` et `AZURE_KEY` dans :
**Portal Azure → votre ressource Azure OpenAI → Keys and Endpoint**

---

## Ajouter des documents

Placez vos fichiers PDF dans le dossier `documents/` :

```
documents/
├── document1.pdf
├── document2.pdf
└── ...
```

Formats supportés : `.pdf`, `.txt`

---

## Lancer en local

```bash
python api.py
```

Le serveur démarre sur `http://localhost:5000`.

Ouvrez `index.html` dans votre navigateur pour utiliser l'interface de chat.

Pour réinitialiser la base de données (après ajout de nouveaux documents) :

```bash
# Windows
del store.json

# Mac/Linux
rm store.json
```

---

## Déploiement Docker

### 1. Builder l'image

```bash
docker build -t agent-ia .
```

### 2. Tester en local

```bash
docker run -p 5000:5000 --env-file .env agent-ia
```

### 3. Pousser sur Azure Container Registry

```bash
az login
az acr login --name agentiaregistry
docker tag agent-ia agentiaregistry.azurecr.io/agent-ia
docker push agentiaregistry.azurecr.io/agent-ia
```

---

## Déploiement Azure Container Apps

Rendez-vous sur https://portal.azure.com → **Container Apps** → **Create** et remplissez :

**Basics**
```
Resource group : votre-resource-group
App name       : agent-ia-app
Region         : Sweden Central
```

**Container**
```
Image source : Azure Container Registry
Registry     : agentiaregistry
Image        : agent-ia
Tag          : latest
```

**Environment variables**
```
AZURE_ENDPOINT = votre_endpoint
AZURE_KEY      = votre_clé
DEPLOY_LLM     = gpt-4o
DEPLOY_EMBED   = text-embedding
```

**Ingress**
```
Enabled     : ✅
External    : ✅
Target port : 5000
```

---

## Utilisation de l'API

### Poser une question

```http
POST /ask
Content-Type: application/json

{
    "question": "Votre question ici ?"
}
```

Réponse :

```json
{
    "reponse": "La réponse de l'agent..."
}
```

### Exemple avec PowerShell

```powershell
Invoke-WebRequest -Uri "http://localhost:5000/ask" `
  -Method POST `
  -Headers @{"Content-Type"="application/json"} `
  -Body '{"question": "De quoi parle ce document ?"}'
```

---

## Structure des fichiers

```
agent-ia/
├── .env                  ← variables d'environnement (ne pas committer)
├── .gitignore
├── Dockerfile
├── requirements.txt
├── api.py                ← point d'entrée du serveur
├── agent.py              ← logique principale de l'agent
├── retriever.py          ← récupération des chunks pertinents
├── embedder.py           ← embeddings via Azure OpenAI
├── vector_store.py       ← base de données vectorielle
├── ingestion.py          ← lecture et découpage des documents
├── index.html            ← interface de chat
├── store.json            ← cache des embeddings (généré automatiquement)
└── documents/            ← dossier pour vos PDF
```

---

## Notes importantes

- Le fichier `store.json` est généré automatiquement au premier lancement — il met en cache les embeddings pour accélérer les démarrages suivants.
- Si vous ajoutez de nouveaux documents, supprimez `store.json` pour forcer le recalcul.
- Ne committez jamais `.env` sur GitHub — il contient vos clés API.
