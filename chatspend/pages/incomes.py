from datetime import datetime
import requests
import pandas as pd
import streamlit as st

from chatspend.services import CategoryService, IncomeService


category_service = CategoryService()
income_service = IncomeService()
categories = category_service.find_by_type("income")

with st.sidebar:

    st.selectbox(
        "Choose category",
        options=[f"{c['id']}|{c['name']}" for c in categories.data],
        format_func=lambda x: x.split('|')[1],
        help="This is used to select the category.",
        key="income_category",
    )

    st.date_input("Date",
                      format="YYYY-MM-DD", 
                      key="income_date")
    
    st.number_input("Amount", placeholder="Enter amount", key="income_price")

    st.text_input("Notes", placeholder="Notes", key="income_notes")

    if st.button("Add Income", type="primary"):
        income_service.create()
        st.rerun()

incomes = income_service.find_by_category_id()
df = pd.DataFrame(incomes.data)

if 'category_id' in df.columns:
    df['category_id'] = df['category_id'].apply(lambda x:x.get('name'))

if 'price' in df.columns:
    sum_incomes = df['price'].sum()
else:
    sum_incomes = 0

col1, col2 = st.columns(2)

with col1:
   st.metric(label="Total Incomes", value=incomes.count)

with col2:
   st.metric(label="Total Amount", value=sum_incomes)

df_filter_col1, df_filter_col2, df_filter_col3 = st.columns(3)

with df_filter_col2:
    filter_this_month = st.session_state.get("income_filter_this_month", True) 
    st.toggle("This Month", value=filter_this_month, key="income_filter_this_month")

with df_filter_col3:
    selectbox_options = [f"{c['id']}|{c['name']}" for c in categories.data]
    selectbox_options.insert(0, "0|All")

    st.selectbox(
        "Filter category",
        options=selectbox_options,
        format_func=lambda x: x.split('|')[1],
        help="This is used to select the category.",
        key="income_filter_category",
    )

df_with_selections = df.copy()
df_with_selections["Select"] = False

edited_df = st.data_editor(df_with_selections,
            column_config = {
                "id": None,
                "category_id": "Category",
                "price": st.column_config.NumberColumn("Price", format="$ %d"),
                "date": st.column_config.DateColumn("Date", format="DD-MM-YYYY"),
                "notes": "Notes",
                "Select": st.column_config.CheckboxColumn(required=True),
            },
            hide_index=True,
            use_container_width=True,
            disabled=df.columns)

selected_rows = edited_df[edited_df.Select]

if st.button('Delete selected rows'):
    income_service.delete_by_ids(selected_rows['id'].tolist())
    st.rerun()


