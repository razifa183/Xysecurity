import pandas as pd
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.ensemble import IsolationForest
import joblib

# File paths
TRAIN_FILE = "KDDTrain+.txt"
COLUMN_FILE = "Field Names.csv"

# Load column names
def load_column_names():
    cols = pd.read_csv(COLUMN_FILE, header=None)[0].tolist()
    cols.append("target")
    cols.append("difficulty_level")
    return cols

# Preprocessing functions
def normalize_text_columns(df):
    for col in ['protocol_type', 'service', 'flag', 'target']:
        df[col] = df[col].astype(str).str.lower()
    return df

def encode_categorical_columns(df):
    encoders = {}
    for col in ['protocol_type', 'service', 'flag']:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col])
        encoders[col] = le
    return df, encoders

def simplify_target(df):
    df['target'] = df['target'].apply(lambda x: 0 if x == 'normal' else 1)
    return df

# ...
def preprocess(df):
    df.drop(columns=['difficulty_level'], inplace=True, errors='ignore')
    df = normalize_text_columns(df)
    df, encoders = encode_categorical_columns(df)
    df = simplify_target(df)

    features_to_use = ['protocol_type', 'service', 'flag', 'duration', 'src_bytes', 'dst_bytes']
    X = df[features_to_use]
    y = df['target']

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    return X_scaled, y, encoders, scaler


# Main
if __name__ == "__main__":
    print("📁 Loading column names...")
    column_names = load_column_names()

    print("📄 Reading dataset...")
    df = pd.read_csv(TRAIN_FILE, header=None, names=column_names)

    print("🧼 Preprocessing...")
    X_scaled, y, encoders, scaler = preprocess(df)

    print("🔍 Filtering normal traffic for training...")
    X_normal = X_scaled[y == 0]

    print("🧠 Training Isolation Forest...")
    model = IsolationForest(contamination=0.01, random_state=42)
    model.fit(X_normal)

    print("💾 Saving model and encoders...")
    joblib.dump(model, "isolation_model.pkl")
    joblib.dump(scaler, "scaler.pkl")
    joblib.dump(encoders, "encoders.pkl")

    print("✅ Training complete!")
