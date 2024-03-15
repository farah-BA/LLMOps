from gensim.models import Word2Vec

def read_training_data(file_path):
    """
    Lit les données d'entraînement à partir d'un fichier texte.
    Chaque ligne du fichier texte doit contenir une phrase tokenisée.
    """
    training_data = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            tokens = line.strip().split()
            training_data.append(tokens)
    return training_data

def train_word2vec_model(training_data):
    """
    Entraîne un modèle Word2Vec à partir des données d'entraînement fournies.
    """
    model = Word2Vec(sentences=training_data, vector_size=100, window=5, min_count=1, workers=4)
    return model

def main():
    # Chemin du fichier contenant les données d'entraînement
    training_data_file = "data.txt"

    # Lecture des données d'entraînement à partir du fichier
    training_data = read_training_data(training_data_file)

    # Entraînement du modèle Word2Vec
    model = train_word2vec_model(training_data)

    # Exemples de mots similaires et de vectorisation de mots
    similar_words = model.wv.most_similar("chat", topn=3)
    print("Mots similaires à 'chat' :", similar_words)

    similar_words = model.wv.most_similar("chien", topn=3)
    print("Mots similaires à 'chien' :", similar_words)

    vector = model.wv["chat"]
    print("Vectorisation du mot 'chat' :", vector)

if __name__ == "__main__":
    main()

