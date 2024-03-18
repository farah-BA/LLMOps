# LLMOps projet

Ce projet vise à fournir une solution complète d'orchestration pour des modèles LLM &amp; Embedding, en utilisant Kubernetes pour le déploiement et la gestion des conteneurs.
## Table of Contents

- [Description](#description)
- [Prérequis](#prérequis)
- [Premiers pas](#premier-pas)
- [Liens utiles](#liens-utiles)

  
## Description
L'application est composée de scripts Python qui interagissent les uns avec les autres pour fournir une expérience utilisateur fluide lors de l'utilisation de différents modèles d'IA. Voici une vue d'ensemble des composants principaux :

* orchestration.py : Constitue le cœur de l'application, intégrant Flask pour fournir une interface API REST. Cette API permet aux utilisateurs de choisir un modèle spécifique, tel que le Langage Model (LLM) ou l'embedding. Lorsqu'un utilisateur soumet une requête pour le modèle LLM, ce script gère la mise en file d'attente dans Redis et déclenche le processus de génération de texte correspondant.
* llm.py:  Contient la logique du modèle de Langage de Grande Taille (LLM). Ce script utilise l'API OpenAI pour générer des réponses textuelles en fonction des prompts récupérés depuis la file d'attente Redis. De plus, il surveille les métriques d'exécution telles que le temps de réponse à l'aide de MLflow, offrant ainsi une vision détaillée des performances du modèle.
* embedding.py: Implémente un modèle d'embedding basé sur Word2Vec, un algorithme permettant d'apprendre à intégrer des mots à partir d'un corpus de textes. Les modèles Word2Vec nécessitent beaucoup de texte, par exemple l'ensemble du corpus Wikipédia. Néanmoins, nous démontrerons les principes en utilisant un petit exemple de texte.
* client.py: Fournit une interface utilisateur permettant aux utilisateurs d'interagir avec l'API via la ligne de commande. Il facilite l'envoi de requêtes au serveur pour choisir un modèle spécifique et fournir les données nécessaires pour l'exécution du modèle LLM .

## Prérequis
Avant de commencer, assurez-vous d'avoir votre machine :
- Python 3.7 ou version ultérieure installé sur votre machine.
- Docker installé si vous prévoyez de déployer avec Kubernetes.
- [kubectl installé avec Minikube](https://kubernetes.io/docs/tasks/tools/).
- [Une clé API pour accéder à l'API OpenAI](https://platform.openai.com/account/api-keys).

## Premiers pas: 

1. **Cloner le dépôt** : Commencez par cloner le dépôt sur votre machine locale en utilisant la commande suivante :
   ```bash
   git clone https://github.com/farah-BA/LLMOps.git

2. **Ajout de la clé API d'OpenAI dans le Dockerfile** : Ouvrez votre Dockerfile et ajoutez la clé API d'OpenAI comme une variable d'environnement.
3. **Construire l'image Docker** : Assurez-vous de remplacer nom-de-l-image:tag par le nom et la version souhaités pour votre image Docker. 
   ```bash
   docker build -t nom-de-l-image:tag .
4. **Pousser l'image sur une plateforme d'hébergement :** Pour pousser votre image Docker sur une plateforme d'hébergement telle que Docker Hub, vous devez d'abord vous connecter à votre compte Docker Hub :
 ```bash
   docker login
```

Ensuite, vous pouvez pousser votre image avec la commande :
 ```bash
   docker push nom-de-l-image:tag
```
 **NB:** Assurez-vous de remplacer nom-de-l-image:tag par le nom et la version de votre image Docker que vous avez utilisée lors de la construction.
