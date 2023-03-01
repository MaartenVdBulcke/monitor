from pandas import DataFrame, Timedelta
import plotly.express as px
import streamlit as st


class Monitor:

    @staticmethod
    def to_local_time(df: DataFrame) -> DataFrame:
        df.timestamp_utc += Timedelta(hours=1)
        return df

    @staticmethod
    def render(df: DataFrame) -> None:
        df = Monitor.to_local_time(df)
        fig = px.line(df, x='timestamp_utc', y='temperature', title='Temperature kids')
        st.plotly_chart(fig, use_container_width=True)
