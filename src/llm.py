import openai
import time
import redis
import mlflow
import subprocess
import torch
import psutil
import yaml
import os
from langchain_community.llms import HuggingFaceHub

# Vérifier la disponibilité du GPU
gpu_available = torch.cuda.is_available()

# Connexion à Redis
redis_client = redis.Redis(host='redis', port=6379)

# Vérification du contenu de la queue Redis
queue_contents = redis_client.lrange("llm_queue", 0, -1)
if queue_contents:
    print("La queue Redis contient des prompts en attente :")
    for item in queue_contents:
        print(item.decode('utf-8'))  # Convertir en chaîne de caractères si nécessaire
else:
    print("La queue Redis est vide.")


# Récupérer la clé d'API à partir de la variable d'environnement
api_key = os.getenv("OPENAI_API_KEY")
huggingface_api_key = os.getenv("HUGGINGFACE_API_KEY")

# Nombre maximal de tokens à générer par le modèle
max_tokens = 50

# Fonction pour utiliser le modèle de Hugging Face
def hugging_face_model(prompt):
    """
    Utilise le modèle Hugging Face pour générer une réponse à partir d'un prompt récupéré depuis la queue.
    
    Args:
        prompt (str): Le prompt pour lequel générer la réponse.
        
    Returns:
        str: La réponse générée par le modèle Hugging Face.
    """
    
    # Instanciation du modèle Hugging Face
    llm = HuggingFaceHub(repo_id="google/flan-ul2", huggingfacehub_api_token=huggingface_api_key)
    
    # Début du chronomètre
    start_time = time.time()

    # Utilisation du modèle pour générer la réponse
    result = llm(prompt)

    # Fin du chronomètre
    end_time = time.time() - start_time

    # Affichage du résultat et du temps d'exécution
    print("\nRésultat du modèle Hugging Face : {}\n".format(result))
    print("Temps d'exécution du modèle Hugging Face : {}\n".format(end_time))

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
            "engine": "Hugging Face",
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

    return result
    
    
def llm_model():
    """
    Utilise le modèle gpt-3 d'openAI (Language Model) pour générer une réponse à partir d'un prompt récupéré depuis la queue Redis.
    """
    try:
        # Définition de la clé d'API
        openai.api_key = api_key

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

    except openai.error.AuthenticationError:
        # Si la clé d'API OpenAI est expirée, utilisez le modèle Hugging Face
        print("La clé d'API OpenAI a expiré. Utilisation du modèle Hugging Face...")
        result = hugging_face_model(prompt)
        print(result)

    except openai.error.RateLimitError:
        # Si la limite de taux est dépassée, utilisez le modèle Hugging Face
        print("La limite de taux OpenAI a été dépassée. Utilisation du modèle Hugging Face...")
        result = hugging_face_model(prompt)
        print(result)
    
    return result

# Exemple d'utilisation
if __name__ == "__main__":
    llm_model()
