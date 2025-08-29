import os
from openai import OpenAI

try:
    # Assurez-vous que votre clé d'API est définie comme variable d'environnement
    api_key = os.environ.get("PERPLEXITY_API_KEY")
    if not api_key:
        raise ValueError("La variable d'environnement PERPLEXITY_API_KEY n'est pas définie.")

    client = OpenAI(api_key=api_key, base_url="https://api.perplexity.ai")

    print("Envoi d'une requête de test à l'API Perplexity...")

    response = client.chat.completions.create(
        model="sonar-pro",
        messages=[
            {"role": "system", "content": "You are an artificial intelligence assistant."},
            {"role": "user", "content": "Bonjour, qui es-tu ?"},
        ],
    )

    print("\nRéponse complète de l'API :")
    print(response)

    print("\nContenu du message :")
    print(response.choices[0].message.content)

except Exception as e:
    print(f"\nUne erreur est survenue : {e}")
