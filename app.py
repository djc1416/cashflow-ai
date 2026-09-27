import pandas as pd
import streamlit as st

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

    except Exception as error:
        st.error(str(error))

else:
    st.info(texts["no_file"])