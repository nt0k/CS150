from Lab5.ingestion import pull_and_clean_data
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import pandas as pd

def classify(df):
    X = df[[
        "Birthday_count",
        "Annual_income",
        "Employed_days",
        "Family_Members",
        "CHILDREN",
        "Property_Owner",
        "Phone",
        "Car_Owner",
        "Work_Phone",
        "GENDER",
        "Type_Income"
    ]]  # Selecting only the specified features

    y = df["label"]  # Target variable (0 or 1)

    # Split into train and test sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Accuracy: {accuracy:.2f}")

df = pull_and_clean_data()
classify(df)