import pandas as pd
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import train_test_split
import joblib
import time
import os
import json
import re

MODEL_PATH = "sp500_reasoning_model.pkl"
DATA_PATH = "stock_data.csv"
QUESTION_LOG = "question_log.json"

def extract_years(text):
    return [int(y) for y in re.findall(r'(20\d{2}|19\d{2})', text)]

def enhance_training_data(df, log_path):
    if not os.path.exists(log_path):
        return df.copy()

    with open(log_path, "r") as f:
        try:
            logs = json.load(f)
        except json.JSONDecodeError:
            return df.copy()

    interest_years = []
    for entry in logs:
        q = entry.get("user_input", "")
        intent = entry.get("intent", "")
        if intent in ["recommend_stock", "most_profit", "worst_day", "average_sp500", "compare_averages"]:
            yrs = extract_years(q)
            interest_years.extend(yrs)

    interest_years = list(set(interest_years))
    if not interest_years:
        return df.copy()

    print(f"📌 Reinforcing training with interest in years: {interest_years}")
    extra_rows = df[df['year'].isin(interest_years)]

    # Duplicate these rows to simulate more importance
    enhanced_df = pd.concat([df, extra_rows, extra_rows]).drop_duplicates().reset_index(drop=True)
    return enhanced_df

def train_model(df):
    df['dt'] = pd.to_datetime(df['dt'])
    df['year'] = df['dt'].dt.year
    df['profit'] = df['sp500'] - df['prev_day']

    features = ['vix', 'sp500_volume', 'djia', 'djia_volume', 'hsi',
                'ads', 'us3m', 'joblessness', 'epu', 'GPRD', 'prev_day']
    target = 'sp500'

    X = df[features]
    y = df[target]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
    model = DecisionTreeRegressor(max_depth=3)
    model.fit(X_train, y_train)

    joblib.dump(model, MODEL_PATH)
    print("✅ Model trained and saved.")

# Watch for updates
print("🔁 Watching for new user interest to retrain model...")

last_log_size = 0
while True:
    try:
        df = pd.read_csv(DATA_PATH)

        if os.path.exists(QUESTION_LOG):
            current_log_size = os.path.getsize(QUESTION_LOG)
            if current_log_size != last_log_size:
                df_enhanced = enhance_training_data(df, QUESTION_LOG)
                train_model(df_enhanced)
                last_log_size = current_log_size
        time.sleep(6)

    except Exception as e:
        print("❌ Error:", e)
        time.sleep(6)
