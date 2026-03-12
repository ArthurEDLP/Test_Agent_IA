## Installation et configuration

Ce projet nécessite **Ollama** pour fonctionner, à la fois pour le modèle de langage (LLM) et l’API d’embeddings.

### Étapes

1. **Installer Ollama**  
   Télécharge et installe Ollama depuis le site officiel : [https://ollama.com](https://ollama.com)

2. **Ouvrir le terminal / console** de ton ordinateur.

3. **Télécharger les modèles nécessaires** :

```bash
# Modèle LLM pour le chat et la génération de texte
ollama pull llama3

# Modèle pour générer les embeddings
ollama pull mxbai-embed-large
