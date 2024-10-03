import logging
from logging.handlers import RotatingFileHandler
import os
import bcrypt
import pandas as pd
from flask import Flask, request, jsonify, render_template, flash, redirect, url_for
from flask_login import LoginManager, login_user, login_required, UserMixin
from joblib import load
print("Répertoire de travail courant :", os.getcwd())
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'votre_secret_très_secret'
logger = logging.getLogger(__name__)
log_file = "app.log"
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler = RotatingFileHandler(log_file, maxBytes=1024 * 1024, backupCount=10)
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

users = {
    "admin": bcrypt.hashpw("password123".encode('utf-8'), bcrypt.gensalt())
}


class User(UserMixin):
    def __init__(self, username):
        self.id = username

    @classmethod
    def query(cls, username):
        if username in users:
            return cls(username)
        return None

    def verify_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), users[self.id])


@login_manager.user_loader
def load_user(user_id):
    return User.query(user_id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query(username)
        if user and user.verify_password(password):
            login_user(user)
            print("Login successful")
            return redirect(url_for('home'))
        else:
            flash('Invalid credentials.')
    return render_template('login.html')


# Chemins relatifs par rapport au dossier src
chemin_fichier_csv = os.path.join("..", "data", "premiere_moitie_2021-22.csv")
chemin_fichier_excel = os.path.join("..", "data", "seconde_moitie_2021-22.xlsx")
modele_chemin = os.path.join("..", "models", "modele_rf.joblib")
label_encoder_path = os.path.join("..", "models", "equivalence_equipes.joblib")
donnees = pd.read_csv(chemin_fichier_csv)
# Chargement du modèle et du LabelEncoder
try:
    modele = load(modele_chemin)
    donnees_seconde_moitie = pd.read_excel(chemin_fichier_excel)
except FileNotFoundError as e:
    logger.error("Erreur de chargement des fichiers : %s", e)
    raise


# Imprimer les valeurs prédites possibles
if hasattr(modele, 'classes_'):
    print("Classes prédites par le modèle :")
    print(modele.classes_)
else:
    # Si le modèle est utilisé pour la régression, imprimer les valeurs prédites minimales et maximales
    print("Plage de valeurs possibles prédites par le modèle :")
    print("Min:", min(modele.predict()))
    print("Max:", max(modele.predict()))

@app.route('/')
@login_required
def home():
    jours = sorted(donnees_seconde_moitie['Journée'].unique())
    return render_template('formulaire.html', jours=jours)


@app.route('/get_matches', methods=['GET'])
@login_required
def get_matches():
    jour = request.args.get('jour', type=int)
    if not jour:
        flash('Aucun jour spécifié pour la récupération des matchs', 'error')
        return redirect(url_for('home'))

    try:
        print(f"Recherche des matchs pour la journée {jour}")
        matchs_du_jour = donnees_seconde_moitie[donnees_seconde_moitie['Journée'] == jour]
        if matchs_du_jour.empty:
            flash(f'Aucun match trouvé pour la journée {jour}', 'error')
            return redirect(url_for('home'))

        # Renvoyer les matchs avec éventuellement des informations sur la dernière prédiction réalisée
        last_prediction = request.args.get('prediction', default=None)
        if last_prediction:
            flash(f'Dernière prédiction: {last_prediction}', 'success')

        return render_template('matches.html', matches=matchs_du_jour.to_dict('records'), jour=jour)
    except Exception as e:
        logger.error(f'Erreur lors de la récupération des matchs pour la journée {jour}: {e}')
        flash('Erreur interne du serveur lors de la récupération des matchs', 'error')
        return redirect(url_for('home'))


@app.route('/predict', methods=['POST'])
@login_required
def predict():
    donnees = pd.read_csv(chemin_fichier_csv)
    print("Début de la prédiction")
    jour = request.args.get('jour', default=None)  # Récupération du jour depuis les arguments de la requête
    try:
        data = request.get_json() if request.is_json else request.form
        home_team = data['HomeTeam']
        away_team = data['AwayTeam']
        print(f"Équipes reçues pour prédiction: {home_team} vs {away_team}")

        # Encodage des variables catégorielles 'HomeTeam' et 'AwayTeam'
        print("Encodage des variables 'HomeTeam' et 'AwayTeam'...")
        # Importer le mapping
        equivalence_equipes = {
            'Arsenal': 0,
            'Aston Villa': 1,
            'Brentford': 2,
            'Brighton': 3,
            'Burnley': 4,
            'Chelsea': 5,
            'Crystal Palace': 6,
            'Everton': 7,
            'Fulham': 8,
            'Leeds': 9,
            'Leicester': 10,
            'Liverpool': 11,
            'Man City': 12,
            'Man United': 13,
            'Newcastle': 14,
            'Norwich': 15,
            'Southampton': 16,
            'Tottenham': 17,
            'Watford': 18,
            'West Ham': 19,
            'Wolves': 20,
            'Bournemouth': 21,
            'Swansea': 22,
            'Stoke': 23,
            'West Brom': 24,
            'Huddersfield': 25,
            'Sheffield United': 26,
            'Reading': 27,
            'Blackburn': 28,
            'Derby': 29,
            'Cardiff': 30,
            'Middlesbrough': 31,
            'Sunderland': 32,
            'Birmingham': 33,
            'Wigan': 34,
            'Portsmouth': 35,
            'Fulham': 36,
            'Bolton': 37,
            'Blackpool': 38,
            'Hull': 39,
            'QPR': 40,
            'Burnley': 41,
            'Brighton': 42,
            'Huddersfield': 43,
            'Swansea': 44,
            'Norwich': 45,
            'Bournemouth': 46,
            'Watford': 47,
            'Stoke': 48,
            'Reading': 49
        }


        # Encodage des noms des équipes
        home_team_code = equivalence_equipes.get(home_team)
        away_team_code = equivalence_equipes.get(away_team)
        print(home_team_code)
        print(away_team_code)

        if home_team_code is None or away_team_code is None:
            flash('Une des équipes est non reconnue.', 'error')
            return redirect(url_for('get_matches'))

        # Encodage des variables catégorielles 'HomeTeam' et 'AwayTeam'
        print("Encodage des variables 'HomeTeam' et 'AwayTeam'...")
        # Utiliser le mapping pour encoder les noms d'équipes dans votre ensemble de données
        donnees['HomeTeam'] = donnees['HomeTeam'].map(equivalence_equipes)
        donnees['AwayTeam'] = donnees['AwayTeam'].map(equivalence_equipes)
        print(donnees['HomeTeam'])
        print(donnees['AwayTeam'])
        print("Encodage terminé.")

        # Filtrage des données pour les matchs à domicile et à l'extérieur
        donnees_home = donnees[donnees['HomeTeam'] == equivalence_equipes[home_team]]
        donnees_away = donnees[donnees['AwayTeam'] == equivalence_equipes[away_team]]
        print(donnees_home)
        print(donnees_away)
        if donnees_home.empty or donnees_away.empty:
            flash("Aucun match trouvé pour une ou les deux équipes", 'error')
            return redirect(url_for('get_matches'))

        # Calcul des moyennes
        moyennes_home = donnees_home[['FTHG', 'HTHG', 'HS', 'HST', 'HF', 'HC', 'HY', 'HR']].tail(5).mean()
        moyennes_away = donnees_away[['FTAG', 'HTAG', 'AS', 'AST', 'AF', 'AC', 'AY', 'AR']].tail(5).mean()
        moyennes = pd.concat([moyennes_home, moyennes_away]).to_frame().T
        print(moyennes)

        # Créer un DataFrame pour la prédiction
        moyennes = pd.DataFrame({
            'HomeTeam': [home_team_code],
            'AwayTeam': [away_team_code],
            **moyennes_home.to_dict(),
            **moyennes_away.to_dict()
        })

        # Prédiction
        colonnes_modele = ['HomeTeam', 'AwayTeam', 'FTHG', 'FTAG', 'HTHG', 'HTAG', 'HS', 'AS', 'HST', 'AST', 'HF',
                               'AF',
                               'HC', 'AC', 'HY', 'AY', 'HR', 'AR']
        input_data = moyennes.reindex(columns=colonnes_modele).fillna(0)
        print(input_data)
        prediction = modele.predict(input_data)
        print(prediction)

        # Interprétation de la prédiction
        if prediction[0] == 'H':
            result = f"Victoire de {home_team}"
        elif prediction[0] == 'A':
            result = f"Victoire de {away_team}"
        else:
            result = "Match nul"

        # Réinitialisation des données de prédiction précédentes
        reset_prediction_data()

        return render_template('prediction_result.html', result=result)
    
    

    except Exception as e:
        logger.error(f'Erreur lors de la prédiction: {e}')
        flash('Erreur lors de la prédiction', 'error')
        return redirect(url_for('get_matches'))
    
@app.route('/reset_prediction_data', methods=['POST'])
@login_required
def reset_prediction_data():
    global previous_prediction_data
    # Réinitialiser les données de prédiction précédentes ici
    # Par exemple, réinitialiser previous_prediction_data à sa valeur par défaut ou vide
    previous_prediction_data = None
    return redirect(url_for('get_matches'))

if __name__ == '__main__':
    app.run(debug=True)
