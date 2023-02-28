import streamlit as st


def get_connection_string() -> str:

    db_type = st.secrets['db_type']
    username = st.secrets['username']
    password = st.secrets['password']
    host = st.secrets['host']
    port = st.secrets['port']
    db_name = st.secrets['db_name']

    return f'{db_type}://{username}:{password}@{host}:{port}/{db_name}'
