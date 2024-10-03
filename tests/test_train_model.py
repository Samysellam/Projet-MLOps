import numpy as np
import sys
import os
from sklearn.ensemble import RandomForestClassifier


# Get the absolute path of the parent directory 
current_dir = os.path.dirname(__file__)

# going up one level from the test directory
src_dir = os.path.abspath(os.path.join(current_dir, '..', 'src'))

# Add the absolute path of src to sys.path
sys.path.append(src_dir)

from models.train_model import train_model
from models.predict_model import evaluate_model

def generate_sample_data(num_samples=1000, num_features=19):
    X = np.random.rand(num_samples, num_features)
    y = np.random.randint(0, 2, num_samples)
    return X, y

# Generate sample data
X, y = generate_sample_data()

##################### Train Model Unit tests #####################

def test_model_instance():
    # Train model
    model, _, _ = train_model(X, y)

    # Check if model is instance of RandomForestClassifier
    assert isinstance(model, RandomForestClassifier)

def test_X_test_not_empty():
    # Train model
    _, X_test, _ = train_model(X, y)

    # Check if X_test is not empty
    assert len(X_test) > 0

def test_y_test_not_empty():
    # Train model
    _, _, y_test = train_model(X, y)

    # Check if y_test is not empty
    assert len(y_test) > 0

def test_X_test_shape():
    # Train model
    _, X_test, _ = train_model(X, y)

    # Check if X_test has the correct shape
    assert X_test.shape[1] == X.shape[1]

def test_y_test_shape():
    # Train model
    _, X_test, y_test = train_model(X, y)

    # Check if y_test has the correct shape
    assert len(y_test) == X_test.shape[0]

def test_model_trained():
    # Train model
    model, _, _ = train_model(X, y)

    # Check if the model has been trained
    assert model.n_estimators > 0

def test_model_predict():
    # Train model
    model, _, _ = train_model(X, y)

    # Check if the model can predict
    assert hasattr(model, "predict")

##################### Predict Model Unit tests #####################

def test_evaluate_model_accuracy_reasonable():
    # Train model
    model, X_test, y_test = train_model(X, y)

    # Evaluate model
    accuracy = evaluate_model(model, X_test, y_test)
    assert 0 <= accuracy <= 1

def test_evaluate_model_instance():
    # Train model
    model, X_test, y_test = train_model(X, y)

    # Evaluate model
    accuracy = evaluate_model(model, X_test, y_test)

    # Check if accuracy is a float
    assert isinstance(accuracy, float)



