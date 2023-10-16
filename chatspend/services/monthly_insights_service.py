import streamlit as st

from chatspend.models import MonthlyInsights
from chatspend.utils import sb_table, sb_user, get_current_month_range


class MonthlyInsightsService:

    def all(self):
        user = sb_user()
        return sb_table(MonthlyInsights).select("type, month, price").eq("created_by", user["id"]).execute()
