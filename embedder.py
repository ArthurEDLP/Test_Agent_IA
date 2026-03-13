from openai import AzureOpenAI
import os

AZURE_ENDPOINT = os.environ.get("AZURE_ENDPOINT")
AZURE_KEY      = os.environ.get("AZURE_KEY")
DEPLOY_EMBED   = os.environ.get("DEPLOY_EMBED")

client = AzureOpenAI(
    azure_endpoint=AZURE_ENDPOINT,
    api_key=AZURE_KEY,
    api_version="2024-02-15-preview"
)
 
def get_embedding(text: str) -> list[float]:
    response = client.embeddings.create(
        input=text,
        model=DEPLOY_EMBED
    )
    return response.data[0].embedding