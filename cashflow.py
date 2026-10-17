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


def calculate_expense_ratio(income, expenses):
    if income <= 0:
        return None

    return (expenses / income) * 100


def calculate_monthly_cash_flow(df):

    monthly_df = df.copy()

    monthly_df["Date"] = pd.to_datetime(
        monthly_df["Date"],
        errors="coerce",
    )

    monthly_df = monthly_df.dropna(subset=["Date"])

    monthly_df["Month"] = (
          monthly_df["Date"].dt.to_period("M").astype(str)
    )

    monthly_summary = (
        monthly_df.pivot_table(
            index="Month",
            columns="Type",
            values="Amount",
            aggfunc="sum",
            fill_value=0      
        )
    )

    for transaction_type in ["Income", "Expense"]:
        if transaction_type not in monthly_summary.columns:
            monthly_summary[transaction_type] = 0

    monthly_summary["Net Cash Flow"] = (
        monthly_summary["Income"] - monthly_summary["Expense"]
    )

    return monthly_summary.sort_index()                