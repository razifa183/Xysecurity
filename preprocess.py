import pandas as pd
from sklearn.preprocessing import LabelEncoder, StandardScaler

# File paths
TRAIN_FILE = "KDDTrain+.txt"
COLUMN_FILE = "Field Names.csv"

# Step 1: Load column names from Field Names CSV + target + difficulty_level
def load_column_names():
    cols = pd.read_csv(COLUMN_FILE, header=None)[0].tolist()
    cols.append("target")            # 42nd column
    cols.append("difficulty_level")  # 43rd column in the dataset
    return cols

def load_dataset(filepath,columns):
    return pd.read_csv(filepath,names=columns)

# Step 2: Normalize categorical string values to lowercase
def normalize_text_columns(df):
    cat_cols = ['protocol_type', 'service', 'flag', 'target']
    for col in cat_cols:
        df[col] = df[col].astype(str).str.lower()
    return df

# Step 3: Encode categorical columns using LabelEncoder
def encode_categorical_columns(df):
    cat_cols = ['protocol_type', 'service', 'flag']
    label_encoders = {}
    for col in cat_cols:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col])
        label_encoders[col] = le
    return df, label_encoders

# Step 4: Convert target column to binary: normal = 0, attack = 1
def simplify_target(df):
    df['target'] = df['target'].apply(lambda x: 0 if x == 'normal' else 1)
    return df

# Step 5: Complete preprocessing pipeline
def preprocess(df):
    # Drop unused column
    if 'difficulty_level' in df.columns:
        df.drop(columns=['difficulty_level'], inplace=True)

    df = normalize_text_columns(df)
    df, encoders = encode_categorical_columns(df)
    df = simplify_target(df)

    # ✅ Only keep features available from live packet
    df = df[['duration', 'protocol_type', 'src_bytes', 'flag', 'target']]

    # Sanity check
    for col in df.columns:
        if df[col].dtype == 'object':
            print(f"⚠️ Column '{col}' still has string values! Sample: {df[col].unique()}")
            raise ValueError(f"Column '{col}' must be numeric before scaling.")

    X = df.drop(columns=["target"])
    y = df["target"]

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    return X_scaled, y, encoders, scaler


# Main function
if __name__ == "__main__":
    print("🔹 Loading column names...")
    column_names = load_column_names()

    print("📁 Reading raw dataset...")
    df = pd.read_csv(TRAIN_FILE, header=None)

    print("🧩 Assigning column names...")
    df.columns = column_names

    print("🔧 Preprocessing...")
    X, y, encoders, scaler = preprocess(df)

    print("✅ DONE. Processed data shape:", X.shape)
    print("📊 Target class distribution:\n", y.value_counts())
