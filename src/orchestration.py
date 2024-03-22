from flask import Flask, request, jsonify
import redis
from redis import Redis
import subprocess

app = Flask(__name__)
redis_client = redis.Redis(host='redis', port=6379) 


@app.route('/choose_model', methods=['POST'])
def choose_model():
    data = request.json
    model_choice = data.get('model')

    if model_choice == 'llm':
        # Si le modèle choisi est LLM, ajouter le prompt à la queue Redis
        prompt = data.get('prompt')
        redis_client.rpush("llm_queue", prompt)
        subprocess.run(["python", "llm.py"])
        return jsonify({"message": "Prompt ajouté à la queue pour le modèle LLM."})
    
    elif model_choice == 'embedding':
        # Si le modèle choisi est Embedding, effectuez les actions nécessaires
        subprocess.run(["python", "embedding.py"])
        return jsonify({"message": "Modèle d'embedding exécuté."})

    else:
        return jsonify({"error": "Modèle non pris en charge."})

if __name__ == "__main__":
   # app.run(debug=True)
    app.run(host='0.0.0.0', port=5000)
