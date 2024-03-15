# Utilisez une image de base qui inclut Python
FROM python:3.10

# Installez les outils Redis
RUN apt-get update && apt-get install -y redis-tools

# Définissez le répertoire de travail dans le conteneur
WORKDIR /app

# Definiton de la clé API d'openAI
ENV OPENAI_API_KEY="clé api d'openAI"

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiez le code de l'application dans le conteneur
COPY src/ .

# Exposez le port sur lequel l'application fonctionne
EXPOSE 5000

# Commande pour démarrer l'application lorsque le conteneur est lancé
CMD ["python3", "orchestration.py"]