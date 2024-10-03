import pandas as pd
import sys
import os

def load_data():
    script_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))  
    folder = os.path.join(script_dir, "data", "raw")  
    print(folder)
    years = ['2015-16', '2016-17', '2017-18', '2018-19', '2019-20', '2020-21', '2021-22']
    raw_data = [pd.read_csv(f"{folder}/{year}.csv") for year in years]
    return pd.concat(raw_data, ignore_index=True) # concatenate data in the same dataframe
