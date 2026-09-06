import streamlit as st
from supabase import create_client, Client

# we defines the isntance of supabase client here so that we can use it in other files by importing it from this file
supabase: Client = create_client(
    st.secrets["SUPABASE_URL"], 
    st.secrets["SUPABASE_KEY"]
)