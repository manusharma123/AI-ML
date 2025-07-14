import pandas as pd
import joblib
import json
import os
import re
from transformers import pipeline

# Load data & model
df = pd.read_csv("stock_data.csv")
df['dt'] = pd.to_datetime(df['dt'])
df['year'] = df['dt'].dt.year
df['profit'] = df['sp500'] - df['prev_day']
model = joblib.load("sp500_reasoning_model.pkl")

QUESTION_LOG = "question_log.json"

# Zero-shot classifier
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

INTENTS = [
    "average_sp500",
    "compare_averages",
    "compare_years_avg",
    "most_profit",
    "worst_day",
    "recommend_stock",
    "most_volatile_year",
    "years_above_avg",
    "best_year_gain",
    "unknown"
]

def classify_intent(text):
    result = classifier(text, candidate_labels=INTENTS)
    return result["labels"][0]

def extract_years(text):
    return [int(y) for y in re.findall(r'(20\d{2}|19\d{2})', text)]

def handle_query(intent, text, df):
    years = extract_years(text)

    if intent == "most_profit":
        year = years[0] if years else None
        if year and year in df['year'].values:
            sub = df[df['year'] == year]
            row = sub.loc[sub['profit'].idxmax()]
            return f"📈 On {row['dt'].date()}, S&P 500 had the biggest gain of {row['profit']:.2f} in {year}."
        row = df.loc[df['profit'].idxmax()]
        return f"📈 Strongest daily gain: {row['profit']:.2f} on {row['dt'].date()}."

    elif intent == "best_year_gain":
        yearly = df.groupby('year')['profit'].max()
        year = yearly.idxmax()
        return f"📈 Best year for single-day gain: {year} with {yearly[year]:.2f} gain."

    elif intent == "worst_day":
        year = years[0] if years else None
        if year:
            sub = df[df['year'] == year]
            row = sub.loc[sub['profit'].idxmin()]
            return f"📉 Worst drop in {year}: {row['profit']:.2f} on {row['dt'].date()}."
        row = df.loc[df['profit'].idxmin()]
        return f"📉 Worst drop ever: {row['profit']:.2f} on {row['dt'].date()}."

    elif intent == "average_sp500":
        year = years[0] if years else None
        if year and year in df['year'].values:
            avg = df[df['year'] == year]['sp500'].mean()
            return f"📊 Average S&P 500 in {year} was {avg:.2f}."
        return f"📉 No data for year {year}."

    elif intent in ["compare_averages", "compare_years_avg"]:
        if len(years) >= 2:
            y1, y2 = years[:2]
            avg1 = df[df['year'] == y1]['sp500'].mean()
            avg2 = df[df['year'] == y2]['sp500'].mean()
            return f"📊 Avg S&P 500:\n  {y1}: {avg1:.2f}\n  {y2}: {avg2:.2f}\n  Difference: {abs(avg1 - avg2):.2f}."
        return "📉 To compare averages, please ask about two years like 'Compare 2015 and 2020'."

    elif intent == "years_above_avg":
        threshold = 4000
        results = df.groupby('year')['sp500'].mean().reset_index()
        years_above = results[results['sp500'] > threshold]['year'].tolist()
        return f"📆 Years where average S&P 500 > {threshold}: {', '.join(map(str, years_above))}"

    elif intent == "most_volatile_year":
        df['daily_vol'] = df['sp500'] - df['prev_day']
        volatility = df.groupby('year')['daily_vol'].std()
        year = volatility.idxmax()
        return f"📊 Most volatile year: {year} (std dev: {volatility.max():.2f})."

    elif intent == "recommend_stock":
        year = years[0] if years else None
        sub = df[df['year'] == year].copy() if year else df.copy()
        sub['sp500_ret'] = (sub['sp500'] - sub['prev_day']) / sub['prev_day']
        sub['djia_ret'] = sub['djia'].pct_change()
        sub['hsi_ret'] = sub['hsi'].pct_change()

        avg_returns = {
            'S&P 500': sub['sp500_ret'].mean(),
            'DJIA': sub['djia_ret'].mean(),
            'HSI': sub['hsi_ret'].mean()
        }

        best = max(avg_returns, key=avg_returns.get)
        return (
            f"📈 Based on daily returns{f' in {year}' if year else ''}, '{best}' performed best.\n"
            f"Returns:\n  S&P 500: {avg_returns['S&P 500']:.4f}\n  DJIA: {avg_returns['DJIA']:.4f}\n  HSI: {avg_returns['HSI']:.4f}\n"
            f"✅ Suggested Index: {best}"
        )

    return "🤔 I couldn’t confidently understand your question. Try asking about average, gain, drop, or volatility."

def log_question(user_input, intent, response):
    log = {
        "user_input": user_input,
        "intent": intent,
        "response": response
    }

    logs = []
    if os.path.exists(QUESTION_LOG):
        with open(QUESTION_LOG, "r") as f:
            try:
                logs = json.load(f)
            except json.JSONDecodeError:
                logs = []

    logs.append(log)

    with open(QUESTION_LOG, "w") as f:
        json.dump(logs, f, indent=2)

# Chat Loop
print("🧠 Stock Reasoning Chatbot (Zero-Shot, Fixed — type 'exit' to quit')")
while True:
    query = input("\nYou: ")
    if query.lower() in ["exit", "quit", "bye"]:
        print("Bot: 👋 Goodbye!")
        break
    intent = classify_intent(query)
    response = handle_query(intent, query, df)
    print("Bot:", response)
    log_question(query, intent, response)
