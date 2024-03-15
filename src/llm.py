import openai
import time
import redis
import mlflow
import subprocess
import torch
import psutil
import yaml
import os

# Vérifier la disponibilité du GPU
gpu_available = torch.cuda.is_available()

# Nombre maximal de tokens à générer par le modèle
max_tokens = 50
# Connexion à Redis
# redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)
redis_client = redis.Redis(host='redis', port=6379) 

# Récupérer la clé d'API à partir de la variable d'environnement
api_key = os.getenv("OPENAI_API_KEY")

# Vérifier si la clé d'API est définie
if api_key is None:
    raise ValueError("La clé d'API OpenAI n'est pas définie.")
else:
    # Définition de la clé d'API
    openai.api_key = api_key


def llm_model():
    """
    Fonction pour le modèle LLM.
    """
    # Récupérer un prompt depuis la queue de Redis
    prompt = redis_client.lpop("llm_queue")
    
    if prompt:
        prompt = prompt.decode('utf-8')  # Convertir le prompt en string
        
        # Début du chronomètre
        start_time = time.time()

        # Appel de l'API pour générer la réponse
        response = openai.Completion.create(
            engine="gpt-3.5-turbo-instruct",
            prompt=prompt,
            max_tokens=max_tokens,
            n=1,
            stop=None
        )

        # Fin du chronomètre
        end_time = time.time() - start_time
        result = response.choices[0].text

        # Affichage du résultat et du temps d'exécution
        print("\nRésultat du modèle LLM : {}\n".format(result))
        print("Temps d'exécution du modèle LLM : {}\n".format(end_time))

        # Suivi des métriques avec MLflow
        with mlflow.start_run() as run:
            # Enregistrement des métriques
            mlflow.log_metric("execution_time", end_time)
            mlflow.log_metric("cpu_usage", psutil.cpu_percent())  # Utilisation du CPU
            mlflow.log_metric("gpu_usage", 0)  # GPU non utilisé dans cet exemple
            mlflow.log_metric("model_inference_time", end_time)  # Temps d'inférence du modèle
            mlflow.log_metric("ram_usage", psutil.virtual_memory().percent)  # Utilisation de la RAM

            # Enregistrement des paramètres
            mlflow.log_params({
                "engine": "gpt-3.5-turbo-instruct",
                "prompt": prompt,
                "max_tokens": max_tokens
            })
            # Récupérer les métriques du run
            run = mlflow.get_run(run.info.run_id)
            metrics = run.data.metrics
            
            # Afficher les métriques
            print("\n--- Métriques ---")
            print("execution_time:", metrics["execution_time"])
            print("cpu_usage:", metrics["cpu_usage"])
            print("gpu_usage:", metrics["gpu_usage"])
            print("model_inference_time:", metrics["model_inference_time"])
            print("ram_usage:", metrics["ram_usage"])

    else:
        result = "Aucun prompt en attente pour le modèle LLM."
    
    return result

# Exemple d'utilisation
if __name__ == "__main__":
    llm_model()

