import streamlit as st
from sqlalchemy.exc import OperationalError as SqlAlchemyError
from pymysql.err import OperationalError as PyMySqlError
from datetime import datetime
from firebase_admin import credentials, db as fire_db
import firebase_admin

from db import MariaEngine, FirebaseRealtime
from monitor import Monitor


st.set_page_config(page_title='Loof monitor', page_icon='🛸')

cred = credentials.Certificate(dict(st.secrets["textkey"]))
if 'firebase' not in st.session_state:
    st.session_state['firebase'] = firebase_admin.initialize_app(cred, {'databaseURL': st.secrets['firebase_url']})
    st.session_state['ref'] = fire_db.reference('/measurements')

try:
    engine = MariaEngine()
    measurements = engine.read()
    Monitor.render(measurements)

    if (timestamp := datetime.now()) and timestamp.hour == 0 and 0 <= timestamp.minute <= 10:
        FirebaseRealtime.backup(st.session_state['ref'], measurements)

except (SqlAlchemyError, PyMySqlError):
    st.write('Data from firebase backup.')
    measurements = FirebaseRealtime.read_db(st.session_state['ref'])
    if measurements is not None:
        Monitor.render(measurements)

st.button('REFRESH')
