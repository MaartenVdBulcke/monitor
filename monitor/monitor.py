from sqlalchemy.engine import Engine
from pandas import read_sql, DataFrame
import plotly.express as px
import streamlit as st


class Monitor:

    @staticmethod
    @st.cache_data(ttl=600)
    def read_database(engine: Engine) -> DataFrame:
        with engine.connect() as connection:
            return read_sql('measurements', connection)

    @staticmethod
    def render(df: DataFrame) -> None:
        fig = px.line(df, x='timestamp_utc', y='temperature', title='Temperature kids')
        st.plotly_chart(fig, use_container_width=True)
