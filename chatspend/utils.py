from datetime import datetime
import streamlit as st
from st_supabase_connection import SupabaseConnection


def get_supabase_client():
    supabase_client = None

    if 'supabase_client' not in st.session_state:
        st.session_state['supabase_client'] = supabase_client
    else:
        supabase_client = st.session_state["supabase_client"]

    if supabase_client is None:
        supabase_client = st.experimental_connection(
            name="supabase_connection", type=SupabaseConnection, ttl="10m"
        )

        st.session_state["supabase_client"] = supabase_client

    return supabase_client.client

sb_client = get_supabase_client()

def sb_table(model):
    if not isinstance(model, str) and hasattr(model, '__tablename__'):
        table_name = model.__tablename__
    else:
        table_name = model

    return sb_client.table(table_name)

def sb_user():   
    if "sb_user" not in st.session_state:
        st.session_state["sb_user"] = {
            "authenticated": False
        }

    sb_user = st.session_state["sb_user"]

    if sb_user["authenticated"] is False:

        if "login" in st.session_state:
            session = st.session_state['login']    

            if session and "access_token" in session:
                sb_client.auth.set_session(session["access_token"], session["refresh_token"])

            if session and "user" in session:
                sb_user.update(session['user'])
                sb_user["authenticated"] = True
                
    return sb_user

def get_current_month_range():
    now = datetime.now()
    first_day_of_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    last_day_of_month = now.replace(hour=23, minute=59, second=59, microsecond=0)
    
    return first_day_of_month, last_day_of_month