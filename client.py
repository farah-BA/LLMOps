import requests

data = {
    "model": "llm",
    "prompt": "que vat 2+2 ?"
}

# Utilisez l'adresse IP correcte du service llmops-service et le port 80
url = "http://192.168.49.2:31949/choose_model"

try:
    response = requests.post(url, json=data)

    # Vérifier si la réponse est vide
    if response.status_code == 200:
        print(response.json())  # Afficher la réponse du serveur
    else:
        print("Erreur lors de la réception de la réponse du serveur:", response.text)
except requests.exceptions.RequestException as e:
    print("Une erreur s'est produite lors de la tentative de connexion au serveur:", e)
