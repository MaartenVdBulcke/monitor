import streamlit as st
from sqlalchemy.exc import OperationalError as SqlAlchemyError
from pymysql.err import OperationalError as PyMySqlError
from datetime import datetime

from db import MariaEngine, FirebaseRealtime
from monitor import Monitor


st.set_page_config(page_title='Loof monitor', page_icon='🛸')

FirebaseRealtime.initialise_firebase()

try:
    engine = MariaEngine()
    measurements = engine.read()
    Monitor.render(measurements)

    if (timestamp := datetime.now()) and timestamp.hour == 0 and 0 <= timestamp.minute <= 10:
        FirebaseRealtime.backup(st.session_state['ref'], measurements)

except (SqlAlchemyError, PyMySqlError):
    st.write('Data from firebase backup.')
    measurements = FirebaseRealtime.read_db(st.session_state['ref'])
    if measurements is None:
        st.write('No backup records available.')
    else:
        Monitor.render(measurements)

st.button('REFRESH')

if st.button('BACKUP'):
    try:
        engine = MariaEngine()
        measurements = engine.read()
        FirebaseRealtime.backup(st.session_state['ref'], measurements)
        st.write('BACKUP SUCCEEDED')
    except (SqlAlchemyError, PyMySqlError):
        st.write('BACKUP FAILED')
