from openai import AzureOpenAI
 
AZURE_ENDPOINT = "https://test-agent-ia-90057.services.ai.azure.com/"
AZURE_KEY      = "V6x8ynGn7ZEe3FXNVTLn4BflY6lLDh4mKXMSnbRo1OrnBcAbroVRJQQJ99CCACYeBjFXJ3w3AAAAACOGpwLT"
DEPLOY_EMBED   = "text-embedding"
 
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