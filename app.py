
import pandas as pd
import plotly.express as px
import streamlit as st

from cashflow import (
    calculate_cash_flow,
    calculate_expenses_by_category,
    calculate_expense_ratio,
    calculate_monthly_cash_flow,
)
from translations import TRANSLATIONS


st.set_page_config(
    page_title="CashFlow AI",
)


language = st.selectbox(
    "Idioma / Language",
    options=["es", "en"],
    format_func=lambda x: (
        "Español" if x == "es" else "English"
    ),
)


texts = TRANSLATIONS[language]


st.title(texts["page_title"])
st.write(texts["welcome"])

st.header(texts["upload_file"])

uploaded_file = st.file_uploader(
    texts["supported_formats"],
    type=["csv", "xlsx"],
)


if uploaded_file is not None:
    try:
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        st.success(texts["file_loaded"])

        st.subheader(texts["data_preview"])
        st.dataframe(df)

        required_columns = [
            "Date",
            "Description",
            "Category",
            "Type",
            "Amount",
        ]

        missing_columns = [
            column
            for column in required_columns
            if column not in df.columns
        ]

        st.write(texts["columns_required"])

        if missing_columns:
            st.error(
                f"{texts['missing_columns']} "
                f"{', '.join(missing_columns)}"
            )

        else:
            st.success(texts["valid_data"])

            transaction_filter = st.selectbox(
                texts["transaction_type"],
                options=["all", "income", "expense"],
                format_func=lambda x: {
                    "all": texts["all"],
                    "income": texts["income_filter"],
                    "expense": texts["expense_filter"],
                }[x],
            )

            filtered_df = df.copy()

            if transaction_filter == "income":
                filtered_df = filtered_df[
                    filtered_df["Type"] == "Income"
                ]

            elif transaction_filter == "expense":
                filtered_df = filtered_df[
                    filtered_df["Type"] == "Expense"
                ]

            income, expenses, net_cash_flow = (
                calculate_cash_flow(df)
            )

            expense_ratio = calculate_expense_ratio(
                income,
                expenses,
            )

            st.subheader(texts["cash_flow"])

            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.metric(
                    texts["income"],
                    f"{income:,.0f}",
                )

            with col2:
                st.metric(
                    texts["expenses"],
                    f"{expenses:,.0f}",
                )

            with col3:
                st.metric(
                    texts["net_cash_flow"],
                    f"{net_cash_flow:,.0f}",
                )

            with col4:
                expense_ratio_display = (
                    f"{expense_ratio:.1f} %"
                    if expense_ratio is not None
                    else texts["no_expense_ratio"]
                )

                st.metric(
                    texts["expense_ratio"],
                    expense_ratio_display,
                )    


            expenses_by_category = (
                calculate_expenses_by_category(filtered_df)
            )

            st.subheader(texts["expenses_by_category"])

            if not expenses_by_category.empty:
                category_options = [
                    "all"
                ] + expenses_by_category.index.tolist()

                selected_category = st.selectbox(
                    texts["category"],
                    options=category_options,
                    format_func=lambda x: (
                       texts["all"] if x == "all" else x
                ),
            )

                if selected_category != "all":
                    expenses_by_category = expenses_by_category.loc[
                        [selected_category]
                    ]   

                if expenses_by_category.empty:
                    st.info(texts["no_expenses_for_filter"])

                else:
                    st.dataframe(expenses_by_category)

                    fig = px.bar(
                        x=expenses_by_category.values,
                        y=expenses_by_category.index,
                        orientation="h",
                        labels={
                            "x": texts["amount"],
                            "y": texts["category"],
                        },
                        text_auto=",.0f",
                    )

                    fig.update_layout(
                        height=(
                            200
                            if len(expenses_by_category) == 1
                            else max(
                                300,
                            min(550, 100 + len(expenses_by_category) * 45),
                            )
                        ),
                        margin=dict(
                            l=20, r=70, t=20, b=35),
                        showlegend=False,
                        yaxis=dict(
                            autorange="reversed",
                            title=None,
                        ),
                        xaxis=dict(
                            title=None,
                            showgrid=True,
                            zeroline=False,
                            range=[
                                0,
                                float(expenses_by_category.max()) * 1.25,
                            ],
                        ),
                    )

                    fig.update_traces(
                        marker_line_width=0,
                        textposition="outside",
                        cliponaxis=False,
                    )

                    st.plotly_chart(
                        fig,
                        use_container_width=True,
                    ) 

                monthly_summary = calculate_monthly_cash_flow(df)

                st.subheader(
                    texts["monthly_cash_flow"]
                )

                if monthly_summary.empty:
                    st.info(texts["no_monthly_cash_flow"])

                else:
                    monthly_fig = px.line(
                        monthly_summary.reset_index(),
                        x="Month",
                        y=[
                            "Income",
                            "Expense",
                            "Net Cash Flow",
                        ],
                        markers=True,
                        labels={
                            "Month": texts["month"],
                            "value": texts["amount"],
                            "variable": texts["series"],
                        },
                    )

                    monthly_fig.update_layout(
                        xaxis=dict(
                            type="category",
                            title=texts["month"],
                        ),
                        yaxis=dict(
                            title=texts["amount"],
                            tickformat=",.0f",
                            rangemode="tozero",
                        ),
                        legend=dict(
                            orientation="h",
                            yanchor="bottom",
                            y=1.02,
                            xanchor="left",
                            x=0,
                        ),
                        margin=dict(
                            l=20, r=20, t=50, b=35),
                        hovermode="x unified",
                    )

                    monthly_fig.update_traces(
                        line=dict(width=3),
                        marker=dict(size=8)
                    )
                        
  
                    st.plotly_chart(
                    monthly_fig,
                    use_container_width=True,
                    )

                    

    except Exception as error:
        st.error(str(error))

else:
    st.info(texts["no_file"])
