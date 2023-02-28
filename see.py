from sqlalchemy import create_engine
from pandas import read_sql
import plotly.express as px
import streamlit as st
import pymysql

db_type = st.secrets['db_type']
user = st.secrets['username']
password = st.secrets['password']
database = st.secrets['db_name']
host = st.secrets['host']
port = st.secrets['port']

engine = create_engine(f'{db_type}://{user}:{password}@{host}:{port}/{database}')

with engine.connect() as connection:
    measurements = read_sql('measurements', connection)

fig = px.line(
    measurements,
    x='timestamp_utc',
    y='temperature',
    title='Temperature kids'
)

st.plotly_chart(fig, use_container_width=True)
