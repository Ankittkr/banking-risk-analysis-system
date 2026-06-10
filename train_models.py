import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.linear_model import LinearRegression
from sklearn.metrics import accuracy_score
from sklearn.metrics import mean_absolute_error

df = pd.read_csv("dataset/german_credit_data.csv")

feature_cols = [
    'laufkont',
    'laufzeit',
    'moral',
    'verw',
    'sparkont',
    'beszeit',
    'rate',
    'famges',
    'buerge',
    'wohnzeit',
    'verm',
    'alter',
    'weitkred',
    'wohn',
    'bishkred',
    'beruf',
    'pers',
    'telef',
    'gastarb'
]

# ---------------------------
# Logistic Regression
# ---------------------------

X_risk = df[feature_cols]
y_risk = df["kredit"]

X_train, X_test, y_train, y_test = train_test_split(
    X_risk,
    y_risk,
    test_size=0.2,
    random_state=42
)

risk_model = LogisticRegression(max_iter=2000)

risk_model.fit(X_train, y_train)

pred = risk_model.predict(X_test)

acc = accuracy_score(y_test, pred)

print(f"Risk Model Accuracy: {acc:.4f}")

joblib.dump(risk_model, "models/risk_model.pkl")

# ---------------------------
# Linear Regression
# ---------------------------

X_loan = df[feature_cols]
y_loan = df["hoehe"]

X_train, X_test, y_train, y_test = train_test_split(
    X_loan,
    y_loan,
    test_size=0.2,
    random_state=42
)

loan_model = LinearRegression()

loan_model.fit(X_train, y_train)

pred = loan_model.predict(X_test)

mae = mean_absolute_error(y_test, pred)

print(f"Loan Model MAE: {mae:.2f}")

joblib.dump(
    loan_model,
    "models/loan_model.pkl"
)

print("Models Saved Successfully")