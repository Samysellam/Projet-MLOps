# Projet MLOps : Prédiction du résultat d'un match de Premier League
======================================================================

## Exécuter via Docker
- Cloner le projet et se rendre dans le dossier dec23_mlops_paris_sportifs
- Installer les packages en lançant la commande `pip install -r src/requirements.txt`
- Exécuter la commande `sh start.sh` et visualiser sur l'url http://127.0.0.1:5000 l'interface Web
- Vérifier le démarrage des Docker dans logs/docker.log

## (Optionnel) Exécuter l'API Flask directement
- Cloner le projet et se rendre dans le dossier dec23_mlops_paris_sportifs
- Installer les packages en lançant la commande `pip install -r src/requirements.txt`
- Exécuter la commande `sh launch_api.sh` et visualiser sur l'url proposée (a priori http://127.0.0.1:5000)

## Interface Web
- Page d'authentification : permet de s'authentifier en renseignant l'utilisateur et le mot de passe associé
- Page de sélection de la journée : choisir une journée de Premier League afin d'obtenir la liste des matchs de cette journée
- Page des matchs de la journée sélectionnée : choisir un match afin d'obtenir la prédiction du résultat du match (Victoire d'une des 2 équipes ou Match nul)

## Données de Premier League
- Issues du site https://www.football-data.co.uk/englandm.php
- Dictionnaire des données : https://www.football-data.co.uk/notes.txt

## Project Organization
------------

    ├── LICENSE
    ├── README.md          <- The top-level README for developers using this project.
    ├── data
    │   ├── api            <- api data
    │   └── raw            <- The original, immutable data dump.
    │
    ├── logs               <- Logs from training and predicting
    │
    ├── models             <- Trained and serialized models, model predictions, or model summaries
    │
    ├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
    │                         the creator's initials, and a short `-` delimited description, e.g.
    │                         `1.0-jqp-initial-data-exploration`.
    │
    ├── references         <- Data dictionaries, manuals, and all other explanatory materials.
    │
    ├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
    │   └── figures        <- Generated graphics and figures to be used in reporting
    │
    ├── requirements.txt   <- The requirements file for reproducing the environment
    │
    ├── src                <- Source code for use in this project.
    │   ├── __init__.py    <- Makes src a Python module
    │   │
    │   ├── data           <- Scripts to download or generate data
    │   │   └── make_dataset.py
    │   │
    │   ├── features       <- Scripts to turn raw data into features for modeling
    │   │   └── build_features.py
    │   │
    │   ├── models         <- Scripts to train models and then use trained models to make
    │   │   │                 predictions
    │   │   ├── predict_model.py
    │   │   └── train_model.py
    │   ├── config         <- Describe the parameters used in train_model.py and predict_model.py
    |   └── main.py        <- main script to execute the Flask app
    | 
    ├── tests
    |    ├── test_make_dataset.py   <- Test if the data is correctly loaded
    |    ├── test_build_features.py <- Test if the features are correctly builded
    |    └── test_train_model.py  <- Test if the training was successuful and evaluate the model
    | 
    ├── launch_api.sh      <- execute Flask api
    └── start.sh           <- launch docker-compose
--------

# Routes API
## Route `/login`

Permet à un utilisateur de se connecter à l'application.

### Exemple de requête curl :

```bash
curl -X POST http://localhost:5000/login -c cookie.txt -d "username=santa&password=secret"
```

### Description :
- Envoie une requête POST avec les identifiants de connexion.
- Le cookie de session est stocké dans le fichier `cookie.txt` pour une utilisation ultérieure.

---

## Route `/get_matches`

Renvoie les matchs pour une journée spécifiée.
Pour l'instant uniquement à partir de la journée 20.

### Exemple de requête curl :

```bash
curl -X GET http://localhost:5000/get_matches?jour=30 -b cookie.txt
```
### Description :
- Envoie une requête GET pour récupérer les matchs pour la journée spécifiée.
- Utilise le cookie de session stocké dans le fichier cookie.txt pour maintenir la session.
---

## Route `/predict`

Effectue une prédiction pour un match donné (Victoire d'une des 2 équipes ou Match Nul).

### Exemple de requête curl :

```bash
curl -X POST http://localhost:5000/predict -b cookie.txt -d "HomeTeam=Arsenal&AwayTeam=Chelsea&jour=10"
```

### Description :
- Envoie une requête POST avec les données du match à prédire.
- Utilise le cookie de session stocké dans le fichier `cookie.txt` pour maintenir la session.

---

## Route `/reset_prediction_data`

Réinitialise les données de prédiction précédentes.
Nécessaire au fonctionnement interne de l'API.

### Exemple de requête curl :

```bash
curl -X POST http://localhost:5000/reset_prediction_data -b cookie.txt
```

### Description :
- Envoie une requête POST pour réinitialiser les données de prédiction précédentes.
- Utilise le cookie de session stocké dans le fichier `cookie.txt` pour maintenir la session.

-----

<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>
