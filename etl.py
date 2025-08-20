# this is the core engine of our pipeline: the ETL script that will automatically process new files.
# It will find raw data, clean it, and load it into our central database, 
# making it ready for the machine learning model.

import os
import glob
import pandas as pd
import sqlite3

RAW_DATA_DIR = 'raw_data'
PROCESSED_DATA_DIR = 'processed_data'
DATABASE_NAME = 'predictions.db'

def process_data():
    """
    finds new CSV files in the raw data directory, process them and loads them 
    into the SQLite database
    """
    print("starting ETL process")

    # find all the csv file in the raw data dir
    raw_files = glob.glob(os.path.join(RAW_DATA_DIR, '*.csv'))

    if not raw_files:
        print("no new files to process")

    # connect to db. it will be created if does not exist
    conn = sqlite3.connect(DATABASE_NAME)

    for file_path in raw_files:
        print(f"Processing file: {file_path}")

        # 1. Extract
        df = pd.read_csv(file_path)

        # 2. Transform
        df['Age'] = df['Age'].fillna(df['Age'].median())
        df['Embarked'] = df['Embarked'].fillna(df['Embarked'].mode()[0])

        df['Sex'] = df['Sex'].map({'male': 0, 'female': 1})
        df['Embarked'] = df['Embarked'].map({'S': 0, 'C': 1, 'Q': 2})
        df['Fare'].fillna(df['Fare'].median(), inplace=True)
        df['SibSp'].fillna(0, inplace=True)
        df['Parch'].fillna(0, inplace=True)
        
        # 3. Load
        df.to_sql('clean_passengers', conn, if_exists='append', index=False)
        print(f"loaded {len(df)} records into the database")

        # move the processed file into the porcessed data directory
        file_name = os.path.basename(file_path)
        os.rename(file_path, os.path.join(PROCESSED_DATA_DIR, file_name))
        print(f"moved {file_name} to processed data archive.")
    
    conn.close()
    print("ETL process finished successfully")

if __name__ == '__main__':
    process_data()