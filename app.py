import numpy as np
import pandas as pd
import streamlit as st
from st_pages import Page, show_pages
from streamlit_supabase_auth import login_form, logout_button

from chatspend.services import IncomeService, ExpenseService, MonthlyInsightsService
from chatspend.utils import sb_user


def main():
    st.title("Personal Finance App")

    login_form(providers=["github",])
    user = sb_user()

    if user["authenticated"] == False:
        show_pages([
            Page("app.py", "Home", "🏠"),            
        ])
        return
    else:
        show_pages([
            Page("app.py", "Home", "🏠"),
            Page("chatspend/pages/incomes.py", "Incomes", "💰"),
            Page("chatspend/pages/expenses.py", "Expenses", "💸"),
            Page("chatspend/pages/categories.py", "Categories", "📊"),
            Page("chatspend/pages/about.py", "About", "📖")
        ])

    with st.sidebar:
        if user["authenticated"]:
            st.write(f"Welcome {user['email']}")
            logout_button()

    income_service = IncomeService()
    expense_service = ExpenseService()
    monthly_insights_service = MonthlyInsightsService()

    incomes = income_service.all()
    incomes_df = pd.DataFrame(incomes.data)

    expenses = expense_service.all()
    expenses_df = pd.DataFrame(expenses.data)

    sum_incomes = 0
    sum_expenses = 0

    if 'price' in incomes_df.columns:
        sum_incomes = incomes_df['price'].sum()

    if 'price' in expenses_df.columns:
        sum_expenses = expenses_df['price'].sum()

    summary_col1, summary_col2, summary_col3 = st.columns(3)

    with summary_col1:
        st.metric(label="Total Income", value=sum_incomes)

    with summary_col2:
        st.metric(label="Total Expenses", value=sum_expenses)

    with summary_col3:
        available_balance = sum_incomes - sum_expenses
        st.metric(label="Available Balance", value=available_balance) 

    chart_data = monthly_insights_service.all()
    chart_data_df = pd.DataFrame(np.zeros((12, 3)), columns=["income", "expense", "subscription"])
    for chart_data_item in chart_data.data:
        chart_data_df.loc[chart_data_item["month"]-1, chart_data_item["type"]] = chart_data_item["price"]

    st.bar_chart(chart_data_df)
    
if __name__ == "__main__":
    main()
