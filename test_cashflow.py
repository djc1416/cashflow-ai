
import pandas as pd

from cashflow import calculate_cash_flow


def create_test_dataframe():
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

    return pd.DataFrame(data)


def test_calculate_cash_flow():
    df = create_test_dataframe()

    income, expenses, net_cash_flow = calculate_cash_flow(df)

    assert income == 800000
    assert expenses == 70000
    assert net_cash_flow == 730000
