import os
import pandas as pd
import numpy as np
import pickle
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder

# ✅ Load Dataset
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
csv_file_path = os.path.join(BASE_DIR, "transactions_train.csv")
df = pd.read_csv(csv_file_path)

# ✅ Drop Unnecessary Columns (IDs and Dates are not useful for ML)
df = df.drop(columns=["transaction_date", "transaction_id_anonymous", "payee_id_anonymous"], errors='ignore')

# ✅ Encode Categorical Data
le = LabelEncoder()
for col in df.columns:
    if df[col].dtype == "object":  # Convert non-numeric columns
        df[col] = le.fit_transform(df[col])

# ✅ Ensure All Data is Numeric
print(df.dtypes)

# ✅ Select Features & Labels
X = df.drop(columns=["is_fraud"])  # Features (Exclude target)
y = df["is_fraud"]  # Target variable

# ✅ Split Data into Train & Test Sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# ✅ Train Model (Random Forest)
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# ✅ Save Model as `fraud_model.pkl`
with open("fraud_model.pkl", "wb") as model_file:
    pickle.dump(model, model_file)

print("✅ Model trained & saved as fraud_model.pkl")
