import streamlit as st

from chatspend.models import Expense
from chatspend.utils import sb_table, sb_user, get_current_month_range


class ExpenseService:

    @property
    def table(self):
        return sb_table(Expense).select("id, category_id(name), price, date, notes", count="exact")

    def all(self):
        return self.table.execute()
    
    def find_by_category_id(self):
        qs = self.table

        if 'expense_filter_category' in st.session_state:
            filter_category = st.session_state['expense_filter_category'].split('|')[0]

            if filter_category != "0":
                qs.eq("category_id", filter_category)

        filter_this_month = st.session_state.get("expense_filter_this_month", True) 

        if filter_this_month:
            first_day_of_month, last_day_of_month = get_current_month_range()
            qs.gte("date", first_day_of_month)
            qs.lte("date", last_day_of_month)


        return qs.execute()   

    def create(self, data=None):
        user = sb_user()

        if data is None:
            data = st.session_state

        new_data = {    
            "category_id": data["expense_category"].split('|')[0], # "1|Food" => 1 
            "date": str(data["expense_date"]),
            "price": data["expense_price"],
            "notes": data["expense_notes"],
            "created_by": user["id"],
            "updated_by": user["id"],   
        }

        return sb_table(Expense).insert(new_data).execute()


    def delete_by_ids(self, ids):
        return sb_table(Expense).delete().in_("id", ids).execute()
