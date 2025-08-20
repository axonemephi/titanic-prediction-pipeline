import pandas as pd
import sqlite3

DATABASE_NAME = 'predictions.db'

conn = sqlite3.connect(DATABASE_NAME)

df = pd.read_sql_query("SELECT * FROM survival_predictions", conn)

conn.close()

if df.empty:
    print("No predctions found")
else:
    print("----------Predctions Table--------")
    print(df.to_string())