import pandas as pd
from sklearn.linear_model import LogisticRegression
import joblib

# --- 1. Data Loading ---
# Load the raw dataset
print("Loading data...")
df = pd.read_csv('titanic.csv')

print("Cleaning and preparing data...")

df['Age'] = df['Age'].fillna(df['Age'].median())
df['Embarked'] = df['Embarked'].fillna(df['Embarked'].mode()[0])

# Convert categorical columns to numerical format
df['Sex'] = df['Sex'].map({'male': 0, 'female': 1})
df['Embarked'] = df['Embarked'].map({'S': 0, 'C': 1, 'Q': 2})



features = ['Pclass', 'Sex', 'Age', 'SibSp', 'Parch', 'Fare', 'Embarked']
target = 'Survived'

X = df[features]
y = df[target]

print("Training the model...")
model = LogisticRegression(max_iter=1000)
model.fit(X, y)

# --- 5. Saving the Model ---
print("Saving the trained model...")
# Use joblib to "flash-freeze" our trained model and save it to a file
joblib.dump(model, 'survival_model.joblib')

print("\nModel trained and saved successfully as 'survival_model.joblib'")
print(df.head())