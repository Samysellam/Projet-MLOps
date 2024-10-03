import os
import sys
import pandas as pd

# Get the absolute path of the parent directory 
current_dir = os.path.dirname(__file__)

# going up one level from the test directory
src_dir = os.path.abspath(os.path.join(current_dir, '..', 'src'))

# Add the absolute path of src to sys.path
sys.path.append(src_dir)

# Now, you can import modules from the src directory
from features.build_features import build_features

# Load the data once as a global variable
DATA = pd.DataFrame({
    'HomeTeam': ['TeamA', 'TeamB', 'TeamC'],
    'AwayTeam': ['TeamB', 'TeamA', 'TeamC'],
    'FTHG': [1, 2, 3],
    'FTAG': [0, 1, 2],
    'FTR': ['H', 'A', 'D'],
    'HTHG': [1, 0, 2],
    'HTAG': [0, 1, 1],
    'HS': [10, 15, 12],
    'AS': [8, 10, 9],
    'HST': [5, 7, 6],
    'AST': [3, 5, 4],
    'HF': [12, 11, 13],
    'AF': [10, 9, 12],
    'HC': [4, 5, 3],
    'AC': [3, 4, 2],
    'HY': [1, 2, 1],
    'AY': [0, 1, 2],
    'HR': [0, 1, 0],
    'AR': [1, 0, 1]
})

def test_build_features_returns_dataframe():
    # Call the build_features function
    result = build_features(DATA)

    # Assert that the result is a DataFrame
    assert isinstance(result, pd.DataFrame)

def test_build_features_not_empty():
    # Call the build_features function
    result = build_features(DATA)

    # Assert that the result is not empty
    assert not result.empty
    
def test_build_features_contains_target_column():
    # Call the build_features function
    result = build_features(DATA)

    # Assert that the target 'FTR' column exists in the DataFrame
    assert 'FTR' in result.columns

def test_build_features_number_of_columns():
    # Call the build_features function
    result = build_features(DATA)

    # Assert that the 'Date' column is dropped
    assert len(result.columns) == 19
    
def test_build_features_no_null_values():
    # Call the build_features function
    result = build_features(DATA)

    # Assert that there are no null values in the DataFrame
    assert not result.isnull().values.any()
