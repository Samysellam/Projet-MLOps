#!/usr/bin/env python
# coding: utf-8

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder
from joblib import dump

# Chargement des données
donnees = pd.read_csv("/Users/samy/Desktop/MLOPS FOOT PRED/Datasets/2020-21.csv")

# Supprimer les colonnes non pertinentes
colonnes_a_garder = ['HomeTeam', 'AwayTeam', 'FTHG', 'FTAG', 'FTR', 'HTHG', 'HTAG', 'HS', 'AS', 'HST', 'AST', 'HF', 'AF', 'HC', 'AC', 'HY', 'AY', 'HR', 'AR']
donnees = donnees[colonnes_a_garder]

# Encodage des variables catégorielles 'HomeTeam' et 'AwayTeam'
label_encoder = LabelEncoder()
donnees['HomeTeam'] = label_encoder.fit_transform(donnees['HomeTeam'])
donnees['AwayTeam'] = label_encoder.transform(donnees['AwayTeam'])

# Vérifier s'il y a des valeurs manquantes dans les données
if donnees.isnull().values.any():
    print("\nAttention : Il y a des valeurs manquantes dans les données. Traitement en cours...")
    # Remplacer les valeurs manquantes par la moyenne des colonnes
    donnees.fillna(donnees.mean(), inplace=True)
    print("Les valeurs manquantes ont été traitées.")

# Sélection des caractéristiques et de la cible
X = donnees.drop(['FTR'], axis=1)
y = donnees['FTR']

# Répéter la division des données en ensembles d'entraînement et de test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Répéter la création et l'entraînement du modèle
modele_rf = RandomForestClassifier(random_state=42)
modele_rf.fit(X_train, y_train)

# Prédiction et évaluation
predictions = modele_rf.predict(X_test)
print("\nPrécision :", accuracy_score(y_test, predictions))

# Enregistrer le modèle
modele_chemin = "/Users/samy/Desktop/MLOPS FOOT PRED/Datasets/modele_rf.joblib"
dump(modele_rf, modele_chemin)
print(f"Modèle enregistré à : {modele_chemin}")

# Enregistrer le LabelEncoder utilisé pour 'HomeTeam' et 'AwayTeam'
label_encoder_chemin = "/Users/samy/Desktop/MLOPS FOOT PRED/Datasets/label_encoder.joblib"
dump(label_encoder, label_encoder_chemin)
print(f"LabelEncoder enregistré à : {label_encoder_chemin}")

# Enregistrer le tableau d'équivalence des équipes
equipe_chemin = "/Users/samy/Desktop/MLOPS FOOT PRED/Datasets/equivalence_equipes.joblib"
equivalence_equipes = dict(zip(label_encoder.classes_, label_encoder.transform(label_encoder.classes_)))
dump(equivalence_equipes, equipe_chemin)
print(f"Tableau d'équivalence des équipes enregistré à : {equipe_chemin}")
import pandas as pd

# Chemin vers le fichier complet de la saison 2021-22
chemin_fichier_complet = "/Users/samy/Desktop/MLOPS FOOT PRED/Datasets/2020-21.csv"

# Charger les données
donnees_completes = pd.read_csv(chemin_fichier_complet)

# Trier les données par date pour s'assurer de l'ordre chronologique
donnees_completes.sort_values('Date', inplace=True)

# Diviser le jeu de données pour ne garder que la première moitié de la saison
donnees_premiere_moitie = donnees_completes.head(len(donnees_completes) // 2)

# Chemin pour enregistrer le nouveau jeu de données
chemin_enregistrement = "/Users/samy/Desktop/MLOPS FOOT PRED/Datasets/premiere_moitie_2020-21.csv"

# Enregistrer le nouveau jeu de données
donnees_premiere_moitie.to_csv(chemin_enregistrement, index=False)

print("Le nouveau jeu de données a été enregistré.")
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from joblib import load

# Chargement des données
chemin_fichier_csv = "/Users/samy/Desktop/MLOPS FOOT PRED/Datasets/premiere_moitie_2020-21.csv"
donnees = pd.read_csv(chemin_fichier_csv)

# Chargement du LabelEncoder
label_encoder = load("/Users/samy/Desktop/MLOPS FOOT PRED/Datasets/label_encoder.joblib")

# Encodage des équipes avec LabelEncoder en gérant les labels inconnus
donnees['HomeTeam'] = label_encoder.transform(donnees['HomeTeam'])
donnees['AwayTeam'] = label_encoder.transform(donnees['AwayTeam'])

# Filtrer et trier les données pour Liverpool à domicile et Arsenal à l'extérieur
donnees_liverpool_home = donnees[donnees['HomeTeam'] == label_encoder.transform(['Liverpool'])[0]].sort_values(by='Date')
donnees_arsenal_away = donnees[donnees['AwayTeam'] == label_encoder.transform(['Arsenal'])[0]].sort_values(by='Date')

# Calcul des moyennes des cinq derniers matchs
moyennes_liverpool_home = donnees_liverpool_home[['FTHG', 'HTHG', 'HS', 'HST', 'HF', 'HC', 'HY', 'HR']].tail(5).mean()
moyennes_arsenal_away = donnees_arsenal_away[['FTAG', 'HTAG', 'AS', 'AST', 'AF', 'AC', 'AY', 'AR']].tail(5).mean()

# Fusionner les moyennes en une seule ligne de DataFrame pour la prédiction
moyennes = pd.concat([moyennes_liverpool_home, moyennes_arsenal_away]).to_frame().T

# Assurer que toutes les colonnes nécessaires sont là et dans le bon ordre
colonnes_modele = ['HomeTeam', 'AwayTeam', 'FTHG', 'FTAG', 'HTHG', 'HTAG', 'HS', 'AS', 'HST', 'AST', 'HF', 'AF', 'HC', 'AC', 'HY', 'AY', 'HR', 'AR']  # Remplacer par la liste des colonnes attendues par le modèle
moyennes = moyennes.reindex(columns=colonnes_modele).fillna(0)

# Charger le modèle
modele_rf = load("/Users/samy/Desktop/MLOPS FOOT PRED/Datasets/modele_rf.joblib")

# Prédiction
prediction = modele_rf.predict(moyennes)
print("Prédiction pour le match Liverpool vs Arsenal :", prediction)


# In[ ]:




