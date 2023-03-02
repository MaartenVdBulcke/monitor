from pandas import DataFrame, Timedelta
import plotly.express as px
import streamlit as st


class Monitor:

    @staticmethod
    def to_local_time(df: DataFrame) -> DataFrame:
        df['timestamp'] = df.timestamp_utc + Timedelta(hours=1)
        return df

    @classmethod
    def render(cls, df: DataFrame) -> None:

        df = Monitor.to_local_time(df)

        fig_day = cls.define_plot_day(df)
        st.plotly_chart(fig_day, use_container_width=True)

        fig = cls.define_plot(df)
        st.plotly_chart(fig, use_container_width=True)

    @staticmethod
    def define_plot(df: DataFrame):
        bar = px.bar(df, x='timestamp', y='temperature', title='Temperature kids')
        bar.update_traces(marker_color='green')
        bar.update_layout(
            title_x=0.38,
            title_font_size=30,
            xaxis=dict(tickformat='%H:%M <br>%A')
        )
        return bar

    @classmethod
    def define_plot_day(cls, df: DataFrame):
        bar = px.bar(
            df, x='timestamp', y='temperature', title='Temperature kids now',
            range_x=[df.timestamp.iloc[-1] - Timedelta(hours=5), df.timestamp.iloc[-1] + Timedelta(hours=0.25)]
        )
        bar.update_traces(marker_color='red')
        bar.update_layout(
            title_x=0.38,
            title_font_size=30,
            xaxis=dict(tickformat='%H:%M <br>%A')
        )
        return bar
