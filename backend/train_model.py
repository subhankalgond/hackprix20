import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import pickle

df = pd.read_csv('cleaned_dataset.csv')

X = df.drop(columns=["Disease"])
y = df['Disease']

symptom_list = X.columns.tolist()

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = RandomForestClassifier()
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
print("Accuracy:", accuracy_score(y_test, y_pred))

with open("model.pkl", "wb") as f:
    pickle.dump(model, f)

with open("symptom_list.pkl", "wb") as f:
    pickle.dump(symptom_list, f)

print("✅ Model trained and saved as model.pkl and symptom_list.pkl")