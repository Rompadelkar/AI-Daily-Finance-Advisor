import streamlit as st
import pandas as pd
import datetime
import plotly.express as px
from dotenv import load_dotenv
from analyzer import analyze_expenses, ai_finance_advice, categorize_expense, predict_weekly_spending

load_dotenv()

st.set_page_config(page_title="AI Daily Finance Advisor", layout="wide")

st.title("💰 AI Daily Finance Advisor")

file = "expenses.csv"

try:
    df = pd.read_csv(file)
except:
    df = pd.DataFrame(columns=["date","category","amount","description"])

df["date"] = pd.to_datetime(df["date"], errors="coerce")

# SIDEBAR INPUT
st.sidebar.header("Add Expense")

date = st.sidebar.date_input("Date", datetime.date.today())

description = st.sidebar.text_input("Description")

auto_category = st.sidebar.checkbox("Auto Categorize (AI)")

if auto_category and description != "":
    category = categorize_expense(description)
else:
    category = st.sidebar.selectbox(
        "Category",
        ["Food","Transport","Shopping","Subscription","Other"]
    )

amount = st.sidebar.number_input("Amount ₹", min_value=0.0)

if st.sidebar.button("Add Expense"):

    new_row = pd.DataFrame({
        "date":[date],
        "category":[category],
        "amount":[amount],
        "description":[description]
    })

    df = pd.concat([df,new_row], ignore_index=True)

    df["date"] = pd.to_datetime(df["date"], errors="coerce")

    df.to_csv(file,index=False)

    st.sidebar.success("Expense Added")

# RESET
st.sidebar.markdown("---")
if st.sidebar.button("Reset All Data"):

    df = pd.DataFrame({
        "date": pd.to_datetime([]),
        "category": [],
        "amount": [],
        "description": []
    })

    df.to_csv(file,index=False)

    st.sidebar.success("Data Reset")

# TODAY ANALYSIS
today = datetime.date.today()

today_df = df[df["date"].dt.date == today]

st.subheader("Today's Spending")

if len(today_df) > 0:

    total_today, category_total, highest_category, highest_amount = analyze_expenses(today_df)

    col1,col2,col3 = st.columns(3)

    col1.metric("Total Today", f"₹{total_today}")
    col2.metric("Top Category", highest_category)
    col3.metric("Highest Expense", f"₹{highest_amount}")

    pie_df = category_total.reset_index()
    pie_df.columns = ["category","amount"]

    fig = px.pie(pie_df, names="category", values="amount", hole=0.5)

    st.plotly_chart(fig, use_container_width=True)

# TREND
st.subheader("Daily Spending Trend")

daily = df.groupby(df["date"].dt.date)["amount"].sum().reset_index()

daily.columns = ["date","amount"]

fig2 = px.line(daily, x="date", y="amount", markers=True)

st.plotly_chart(fig2, use_container_width=True)

# MONTHLY
st.subheader("Monthly Summary")

month_df = df[df["date"].dt.month == today.month]

monthly_total = month_df["amount"].sum()

st.metric("Monthly Spending", f"₹{monthly_total}")

# BUDGET ALERT
budget = st.number_input("Set Monthly Budget ₹", value=5000)

if monthly_total > budget:

    st.error("⚠ You exceeded your monthly budget!")

# AI ADVICE
st.subheader("AI Financial Advice")

summary = df.groupby("category")["amount"].sum().to_string()

if st.button("Generate Advice"):

    advice = ai_finance_advice(summary)

    st.success(advice)

# WEEKLY PREDICTION
st.subheader("Predicted Spending Next Week")

if len(df) > 5:

    prediction = predict_weekly_spending(df)

    st.info(f"Estimated spending next week: ₹{round(prediction,2)}")

# TABLE
st.subheader("Transactions")

st.dataframe(df)

# DOWNLOAD
st.download_button(
    "Download Data",
    df.to_csv(index=False),
    "expenses.csv"
)
