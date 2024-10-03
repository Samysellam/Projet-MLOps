from sklearn.preprocessing import LabelEncoder
from datetime import datetime
import pandas as pd

# Désactiver les avertissements de type SettingWithCopyWarning
pd.options.mode.chained_assignment = None

def build_features(donnees):
    
    columns_to_keep = ['HomeTeam', 'AwayTeam', 'FTHG', 'FTAG', 'FTR', 'HTHG', 'HTAG', 'HS', 'AS', 'HST', 'AST', 'HF', 'AF', 'HC', 'AC', 'HY', 'AY', 'HR', 'AR']
    
    donnees = donnees[columns_to_keep]

    label_encoder = LabelEncoder()
    
    donnees['HomeTeam'] = label_encoder.fit_transform(donnees['HomeTeam'])
    donnees['AwayTeam'] = label_encoder.transform(donnees['AwayTeam'])
    donnees['FTR'] = label_encoder.fit_transform(donnees['FTR'])

    donnees.fillna(donnees.mean(), inplace=True)
    
    return donnees
