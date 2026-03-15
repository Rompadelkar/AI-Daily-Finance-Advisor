import pandas as pd

df = pd.read_csv("Daily Household Transactions.csv")

df = df[df["Income/Expense"] == "Expense"]

df = df.rename(columns={
    "Date":"date",
    "Category":"category",
    "Amount":"amount",
    "Note":"description",
    "Mode":"payment_method",
    "Currency":"currency"
})

df = df[["date","category","amount","description"]]

df.to_csv("expenses.csv", index=False)

print("Dataset ready for app")