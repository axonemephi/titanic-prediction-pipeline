# This script's job is to wake up, find the clean data prepared by our ETL script, 
# use our saved model to make predictions, and store those predictions.

import pandas as pd
import sqlite3
import joblib

DATABASE_NAME = 'predictions.db'
MODEL_FILE = 'survival_model.joblib'
PASSENGER_ID_COLUMN = 'PassengerId'

def make_predctions():
    """
    loads the pretrained model, from joblib
    reads new clean data from the database
    makes predctions, and saves them back to database
    """
    print("starting predction process....")


    # load the pretrained model.
    try:
        model = joblib.load(MODEL_FILE)
        print("Model loaded successfully")
    except FileNotFoundError:
        print(f"Error: model file not found at {MODEL_FILE}. please run the training script first")
        return
    
    conn = sqlite3.connect(DATABASE_NAME)

    # extract new data
    # read all the data from clean_passengers table
    try:
        df = pd.read_sql_query("SELECT * FROM clean_passengers", conn)
    except pd.io.sql.DatabaseError:
        print(f"no new data to predict. the 'clean_passengers' table does not exist or is empty")
        conn.close()
        return
    

    if df.empty:
        print("no new data to predict")
        conn.close()
        return
    
    print(f"found {len(df)} new records to make predctions on...")

    passenger_ids = df[PASSENGER_ID_COLUMN]

    features_for_model = ['Pclass', 'Sex', 'Age', 'SibSp', 'Parch', 'Fare', 'Embarked']
    X_predict = df[features_for_model]

    # predict
    predictions = model.predict(X_predict)

    # Load the predctions
    # create a new dataframe with PassengerId and the predictions
    output_df = pd.DataFrame({
        PASSENGER_ID_COLUMN: passenger_ids,
        'Survived Predctions': predictions
    })

    # save the predctions to new table called 'survival predctions'
    output_df.to_sql('survival_predictions', conn, if_exists='append', index=False)
    print(f"saved {len(output_df)} predcions to the 'survival predctions' table.")

    # CLEANUP
    # To prevent making the same predictions again, we clear the 'clean_passengers'
    cursor = conn.cursor()
    cursor.execute("DELETE FROM clean_passengers")
    conn.commit()
    print("cleaned the clean_passengers table")

    conn.close()
    print("predctions process finished successfully.")

if __name__ == '__main__':
    make_predctions()