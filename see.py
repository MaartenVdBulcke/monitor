import streamlit as st
from sqlalchemy.exc import OperationalError as SqlAlchemyError
from pymysql.err import OperationalError as PyMySqlError
from datetime import datetime

from db import MariaEngine, FirebaseRealtime
from monitor import Monitor

st.set_page_config(page_title='Loof monitor', page_icon='🛸')

FirebaseRealtime.initialize_firebase_realtime()

try:
    engine = MariaEngine()
    measurements = engine.read()
    Monitor.render(measurements)

    if (timestamp := datetime.now()) and timestamp.hour == 0 and 0 <= timestamp.minute <= 10:
        FirebaseRealtime.backup(measurements)

except (SqlAlchemyError, PyMySqlError):
    st.write('Data from firebase backup.')
    measurements = FirebaseRealtime.read()
    if measurements is not None:
        Monitor.render(measurements)

st.button('REFRESH')
