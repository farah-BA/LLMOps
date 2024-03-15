# Utilisez une image de base qui inclut Python
FROM python:3.10

# Install Redis tools
RUN apt-get update && apt-get install -y redis-tools

# Set the working directory inside the container
WORKDIR /app

ENV OPENAI_API_KEY="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"

# Copy and install python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy scripts from the src/ directory
COPY src/ .
# Exposez le port sur lequel l'application fonctionne
EXPOSE 5000

# Commande pour démarrer l'application lorsque le conteneur est lancé
CMD ["python3", "orchestration.py"]

