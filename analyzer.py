import google.generativeai as genai
import os
from sklearn.linear_model import LinearRegression
import numpy as np

def analyze_expenses(df):

    total_today = df["amount"].sum()

    category_total = df.groupby("category")["amount"].sum()

    highest_category = category_total.idxmax()

    highest_amount = category_total.max()

    return total_today, category_total, highest_category, highest_amount


def ai_finance_advice(summary):

    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

    model = genai.GenerativeModel("models/gemini-2.5-flash")

    prompt = f"""
    Analyze this spending data and give financial advice.

    {summary}

    Tell:
    - where the user spends the most
    - how they can reduce spending
    - one smart saving habit
    """

    response = model.generate_content(prompt)

    return response.text


def categorize_expense(description):

    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

    model = genai.GenerativeModel("gemini-2.5-flash")

    prompt = f"""
    Categorize this expense into one of these categories:
    Food, Transport, Shopping, Subscription, Other.

    Expense: {description}

    Return only the category name.
    """

    response = model.generate_content(prompt)

    return response.text.strip()


def predict_weekly_spending(df):

    df = df.copy()

    df["date"] = df["date"].astype("int64") // 10**9

    X = np.arange(len(df)).reshape(-1,1)

    y = df["amount"].values

    model = LinearRegression()

    model.fit(X,y)

    next_days = np.arange(len(df), len(df)+7).reshape(-1,1)

    prediction = model.predict(next_days)

    return prediction.sum()