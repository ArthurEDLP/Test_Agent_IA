from openai import AzureOpenAI
 
client = AzureOpenAI(
    azure_endpoint="https://agent90057.openai.azure.com/",
    api_key="9enqzvcbr5OgzrQud80ER6lqfgj7sdS9WFezxYUFXkeH7focKYu2JQQJ99CCACYeBjFXJ3w3AAABACOGEE3v",
    api_version="2023-05-15"
)
 
response = client.embeddings.create(
    input="test",
    model="text-embedding")

print(response.data[0].embedding[:5])