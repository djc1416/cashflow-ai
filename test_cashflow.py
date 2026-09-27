import pandas as pd

from cashflow import calculate_cash_flow

data = {
    "Date": [
        "2026-09-01",
        "2026-09-02",
        "2026-09-03",
    ],    
    "Description": [
        "Salary",
        "Supermarket",
        "Internet",
    ],
    "Category": [
        "Income",
        "Food",
        "Bills",
    ],
    "Type": [
        "Income",
        "Expense",
        "Expense",
    ],
    "Amount": [
        800000,
        45000,
        25000,
    ],
}

df = pd.DataFrame(data)

income, expenses, net_cash_flow = calculate_cash_flow(df)

print("Income:", income)
print("Expenses:", expenses)
print("Net Cash Flow:", net_cash_flow)