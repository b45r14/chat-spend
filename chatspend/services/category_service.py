import streamlit as st

from chatspend.models import Category
from chatspend.utils import sb_table, sb_user


class CategoryService:

    def all(self):
        qs = sb_table(Category).select("id, name, type", count="exact").execute()

        return qs
    
    def find_by_type(self, name):
        return sb_table(Category).select("id, name, type").eq("type", name).execute()

    def create(self, data=None):
        user = sb_user()

        if data is None:
            data = st.session_state

        new_data = {        
            "name": data["category_name"],
            "type": data["category_type"],
            "created_by": user["id"],
            "updated_by": user["id"],
        }

        return sb_table(Category).insert(new_data).execute()


    def delete_by_ids(self, ids):
        return sb_table(Category).delete().in_("id", ids).execute()
