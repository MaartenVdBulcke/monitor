import streamlit as st

from db import MariaEngine
from monitor import Monitor

st.set_page_config(page_title='Loof monitor', page_icon='🛸')

engine = MariaEngine.get_engine()
Monitor.update(engine)

st.button('REFRESH')
