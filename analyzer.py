import google.generativeai as genai
import os

def analyze_expenses(df):

    if df.empty:
        return 0, {}, "None", 0

    total_today = df["amount"].sum()

    category_total = df.groupby("category")["amount"].sum()

    highest_category = category_total.idxmax()

    highest_amount = category_total.max()

    return total_today, category_total, highest_category, highest_amount


def ai_finance_advice(summary):

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        return "AI advice unavailable (API key missing)."

    genai.configure(api_key=api_key)

    try:

        model = genai.GenerativeModel("models/gemini-2.5-flash")

        prompt = f"""
        Analyze the following spending summary:

        {summary}

        Tell:
        - where the user spends the most
        - how they can reduce spending
        - one smart saving habit
        """

        response = model.generate_content(prompt)

        return response.text

    except Exception:
        return "AI advice temporarily unavailable."