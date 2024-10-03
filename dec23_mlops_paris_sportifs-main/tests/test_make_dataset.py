import os
import sys
import pandas as pd

# Get the absolute path of the parent directory 
current_dir = os.path.dirname(__file__)

# going up one level from the test directory
src_dir = os.path.abspath(os.path.join(current_dir, '..', 'src'))

# Add the absolute path of src to sys.path
sys.path.append(src_dir)

# Maintenant, vous pouvez importer les modules depuis le répertoire src
from data.make_dataset import load_data

# Load the data once as a global variable
DATA = load_data()

def test_load_data_returns_dataframe():
    # Assert that the result is a DataFrame
    assert isinstance(DATA, pd.DataFrame)

def test_load_data_not_empty():
    # Assert that the result is not empty
    assert not DATA.empty
    
def test_load_data_contains_target_column():
    # Assert that the target 'FTR' column exists in the DataFrame
    assert 'FTR' in DATA.columns