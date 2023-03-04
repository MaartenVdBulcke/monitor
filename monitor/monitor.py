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

        cls.show_latest_measurement(df)

        fig_day = cls.define_plot_day(df)
        st.plotly_chart(fig_day, use_container_width=True)

    @classmethod
    def show_latest_measurement(cls, df: DataFrame):
        latest_measurement_time = df.timestamp.iloc[-1]
        latest_measurement_temp = df.temperature.iloc[-1]
        st.markdown(
            f'<h2 style=text-align:center;color:darkTurquoise;>'
            f'{round(latest_measurement_temp, 1)}° Celsius'
            f'</h2>',
            unsafe_allow_html=True
        )
        if (m := latest_measurement_time.minute) < 10:
            m = f'0{m}'

            st.markdown(
                f'<h5 style=text-align:center;color:darkTurquoise;>'
                f'last measured at {latest_measurement_time.hour}h{m}'
                f'</h5>',
                unsafe_allow_html=True
            )

    @classmethod
    def define_plot_day(cls, df: DataFrame):
        bar = px.bar(
            df, x='timestamp', y='temperature', title=' ', # title='Temperature kids',
            range_x=[df.timestamp.iloc[-1] - Timedelta(hours=5), df.timestamp.iloc[-1] + Timedelta(hours=0.25)]
        )
        bar.update_traces(marker_color='red')
        bar.update_layout(
            # title_x='center',
            title_font_size=30,
            xaxis=dict(tickformat='%H:%M <br>%A')
        )
        return bar
