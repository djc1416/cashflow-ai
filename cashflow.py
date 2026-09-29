import pandas as pd

def calculate_cash_flow(df):
    """
    Calculate total income, total expenses, and net cash flow.
    """

    income = df.loc[
        df["Type"] == "Income",
        "Amount",
    ].sum()

    expenses = df.loc[
        df["Type"] == "Expense",
        "Amount",
    ].sum()

    net_cash_flow = income - expenses

    return income, expenses, net_cash_flow

def calculate_expenses_by_category(df):

    expenses_by_category = (
        df.loc[df["Type"] == "Expense"]
        .groupby("Category")["Amount"]
        .sum()
        .sort_values(ascending=False)
    )

    return expenses_by_category    
   