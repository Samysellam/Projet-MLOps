from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

def train_model(X, y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    modele_rf = RandomForestClassifier(random_state=42)
    modele_rf.fit(X_train, y_train)
    return modele_rf, X_test, y_test
