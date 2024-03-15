# LLMOps projet

Ce projet vise à fournir une solution complète d'orchestration pour des modèles LLM &amp; Embedding, en utilisant Kubernetes pour le déploiement et la gestion des conteneurs.

#3 Description
L'application est composée de plusieurs scripts Python qui interagissent les uns avec les autres pour fournir une expérience utilisateur fluide lors de l'utilisation de différents modèles d'IA. Voici une vue d'ensemble des composants principaux :

### orchestration.py : Ce script utilise Flask pour fournir une API REST permettant aux utilisateurs de soumettre des requêtes pour choisir un modèle spécifique (LLM ou Embedding). En fonction de la demande de l'utilisateur, il remplit la queue Redis appropriée et lance le modèle correspondant.

### llm.py : Ce script contient la logique du modèle de langage de grande taille (LLM). Il utilise l'API OpenAI pour générer des réponses textuelles en fonction des prompts reçus depuis la file d'attente Redis. Il suit également les métriques d'exécution à l'aide de MLflow.

### embedding.py : Ce script implémente un modèle d'embedding basé sur Word2Vec. Il peut être utilisé pour effectuer des tâches telles que la recherche de mots similaires dans un corpus de texte.

### client.py : Ce script fournit une interface utilisateur simple permettant aux utilisateurs d'interagir avec l'API via la ligne de commande.
