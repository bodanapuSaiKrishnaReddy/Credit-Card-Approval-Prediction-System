import pandas as pd
import numpy as np
import pickle
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    classification_report,
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix
)

# 1. Load Datasets
print("Loading data...")
app_df = pd.read_csv('archive/application_record.csv')
credit_df = pd.read_csv('archive/credit_record.csv')

# 2. Feature Engineering on Credit Record (Target Generation)
# Status definitions: 0: 1-29 days past due, 1: 30-59 days, 2: 60-89 days...
# We define "Bad" (1) as anyone with debts past due for 30+ days (Status 1-5)
credit_df['target'] = credit_df['STATUS'].isin(['1', '2', '3', '4', '5']).astype(int)

# Group by ID to see if an applicant was ever classified as a high-risk ("Bad") customer
target_df = credit_df.groupby('ID')['target'].max().reset_index()

# Merge back with Application Records
df = pd.merge(app_df, target_df, on='ID', how='inner')

# 3. Data Cleaning & Pre-processing
df.drop(['ID'], axis=1, inplace=True)
# Impute missing OCCUPATION_TYPE with a new "Unknown" category instead of dropping the row
df['OCCUPATION_TYPE'] = df['OCCUPATION_TYPE'].fillna('Unknown')
df.dropna(inplace=True)  # Drops rows where other required fields might be missing

# WARNING: Using gender-related features ('CODE_GENDER') as predictor variables is
# legally restricted for real credit decisions under fair-lending laws (e.g., ECOA / Reg B in the US).
# TODO: Ask the user whether to drop this feature before deploying to production.

# Encode Categorical Variables
categorical_cols = df.select_dtypes(include=['object']).columns
label_encoders = {}

for col in categorical_cols:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    label_encoders[col] = le

# Separate Features and Target
X = df.drop(['target'], axis=1)
y = df['target']

# 4. Train-Test Split (Split raw features before scaling)
X_train_raw, X_test_raw, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# Feature Scaling (Fit only on training data to avoid data leakage)
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train_raw)
X_test = scaler.transform(X_test_raw)

# 5. Model Building (Random Forest Classifier)
print("Training Random Forest Model...")
model = RandomForestClassifier(n_estimators=100, min_samples_split=10, random_state=42)
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
y_prob = model.predict_proba(X_test)[:, 1]

print("=== Evaluation Metrics ===")
print(f"Accuracy:        {accuracy_score(y_test, y_pred):.4f}")
print(f"Precision:       {precision_score(y_test, y_pred):.4f}")
print(f"Recall:          {recall_score(y_test, y_pred):.4f}")
print(f"F1-Score:        {f1_score(y_test, y_pred):.4f}")
print(f"ROC-AUC Score:   {roc_auc_score(y_test, y_prob):.4f}")
print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))
print("\nClassification Report (Split by Class):")
print(classification_report(y_test, y_pred))

# 6. Save Artifacts for Flask Application
with open('model.pkl', 'wb') as m_file:
    pickle.dump(model, m_file)

with open('scaler.pkl', 'wb') as s_file:
    pickle.dump(scaler, s_file)

with open('encoders.pkl', 'wb') as e_file:
    pickle.dump(label_encoders, e_file)

print("All pipeline artifacts saved successfully!")