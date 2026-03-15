import streamlit as st
import pandas as pd
import datetime
import plotly.express as px

from database import *
from analyzer import analyze_expenses, ai_finance_advice

st.set_page_config(page_title="AI Finance Advisor", layout="wide")

st.title("💰 AI Personal Finance Advisor")

# SESSION STATE LOGIN
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = None

menu = ["Login","Signup"]
choice = st.sidebar.selectbox("Menu",menu)

# SIGNUP
if choice == "Signup":

    st.subheader("Create Account")

    new_user = st.text_input("Username")
    new_password = st.text_input("Password",type="password")

    if st.button("Create Account"):

        success = create_user(new_user,new_password)

        if success:
            st.success("Account created. Please login.")
        else:
            st.error("Username already exists.")


# LOGIN
if choice == "Login" and not st.session_state.logged_in:

    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password",type="password")

    if st.sidebar.button("Login"):

        user = login_user(username,password)

        if user:

            st.session_state.logged_in = True
            st.session_state.username = username

            st.rerun()

        else:
            st.error("Invalid login")


# DASHBOARD AFTER LOGIN
if st.session_state.logged_in:

    username = st.session_state.username

    st.success(f"Welcome {username}")

    if st.sidebar.button("Logout"):

        st.session_state.logged_in = False
        st.session_state.username = None
        st.rerun()

    # ADD EXPENSE
    st.sidebar.header("Add Expense")

    date = st.sidebar.date_input("Date",datetime.date.today())

    category = st.sidebar.selectbox(
        "Category",
        ["Food","Transport","Shopping","Subscription","Other"]
    )

    amount = st.sidebar.number_input("Amount ₹",min_value=0.0)

    description = st.sidebar.text_input("Description")

    if st.sidebar.button("Add Expense"):

        add_expense(username,date,category,amount,description)

        st.sidebar.success("Expense Added")

    if st.sidebar.button("Reset All Data"):

        reset_user_data(username)

        st.sidebar.success("All expenses deleted")

    # LOAD DATA
    data = get_expenses(username)

    df = pd.DataFrame(
        data,
        columns=["date","category","amount","description"]
    )

    if not df.empty:
        df["date"] = pd.to_datetime(df["date"], errors="coerce")

    today = datetime.date.today()

    st.subheader("Today's Spending")

    if not df.empty:

        today_df = df[df["date"].dt.date == today]

        if not today_df.empty:

            total_today, category_total, highest_category, highest_amount = analyze_expenses(today_df)

            col1,col2,col3 = st.columns(3)

            col1.metric("Total Today",f"₹{total_today}")
            col2.metric("Top Category",highest_category)
            col3.metric("Highest Expense",f"₹{highest_amount}")

            pie_df = category_total.reset_index()
            pie_df.columns=["category","amount"]

            fig = px.pie(pie_df,names="category",values="amount")

            st.plotly_chart(fig,use_container_width=True)

    st.subheader("Daily Spending Trend")

    if not df.empty:

        daily = df.groupby(df["date"].dt.date)["amount"].sum().reset_index()

        fig2 = px.line(daily,x="date",y="amount",markers=True)

        st.plotly_chart(fig2,use_container_width=True)

    st.subheader("Monthly Summary")

    if not df.empty:

        month_df = df[df["date"].dt.month == today.month]

        monthly_total = month_df["amount"].sum()

        st.metric("Monthly Spending",f"₹{monthly_total}")

    st.subheader("AI Financial Advice")

    if not df.empty:

        summary = df.groupby("category")["amount"].sum().to_string()

        if st.button("Generate Advice"):

            advice = ai_finance_advice(summary)

            st.success(advice)

    st.subheader("All Transactions")

    st.dataframe(df)