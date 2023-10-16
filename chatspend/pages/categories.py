from datetime import datetime
import pandas as pd
import streamlit as st

from chatspend.services import CategoryService


category_service = CategoryService()

with st.sidebar:
    st.text_input("Category Name", placeholder="Enter category name", key="category_name")

    selectbox_options = ['income', 'expense', 'subscription']
    
    st.selectbox(
        "Category Type",
        options=selectbox_options,
        format_func=lambda x: x.capitalize(),
        key="category_type",
    )

    if st.button("Add Category", type="primary"):
        category_service.create()

categories = category_service.all()
df = pd.DataFrame(categories.data)

col1, col2 = st.columns(2)

with col1:
   st.metric(label="Total Categories", value=categories.count)

df_with_selections = df.copy()
df_with_selections["Select"] = False

edited_df = st.data_editor(df_with_selections,
            column_config = {
                "id": None,
                "name": "Name",
                "type": "Type",
                "Select": st.column_config.CheckboxColumn(required=True),
            },
            hide_index=True,
            use_container_width=True,
            disabled=df.columns)

df_selected_rows = edited_df[edited_df.Select]

if st.button('Delete selected rows'):
    category_service.delete_by_ids(df_selected_rows['id'].tolist())
    st.rerun()


