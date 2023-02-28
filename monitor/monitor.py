from sqlalchemy.engine import Engine
from pandas import read_sql, DataFrame, Timedelta
import plotly.express as px
import streamlit as st


class Monitor:

    @staticmethod
    def update(engine: Engine) -> None:
        measurements = Monitor.read_database(engine)
        measurements = Monitor.to_local_time(measurements)
        Monitor.render(measurements)

    @staticmethod
    def read_database(engine: Engine) -> DataFrame:
        with engine.connect() as connection:
            return read_sql('measurements', connection)

    @staticmethod
    def to_local_time(df: DataFrame) -> DataFrame:
        df.timestamp_utc += Timedelta(hours=1)
        return df

    @staticmethod
    def render(df: DataFrame) -> None:

        fig = px.line(df, x='timestamp_utc', y='temperature', title='Temperature kids')
        st.plotly_chart(fig, use_container_width=True)
