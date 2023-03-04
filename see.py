from traceback import format_exc

import streamlit as st
from sqlalchemy.exc import OperationalError as SqlAlchemyError
from pymysql.err import OperationalError as PyMySqlError
from datetime import datetime
import firebase_admin
from firebase_admin import credentials, db

from db import MariaEngine, FirebaseRealtime
from monitor import Monitor


st.set_page_config(page_title='Loof monitor', page_icon='🛸')

FirebaseRealtime.initialise_firebase()

_, col1, col2, col3 = st.columns((4, 2, 2, 4))
col1.button('REFRESH', use_container_width=True)

if col2.button('BACKUP', use_container_width=True):
    try:
        engine = MariaEngine()
        measurements = engine.read()
        try:
            cred = credentials.Certificate(dict(st.secrets["textkey"]))
            st.session_state['firebase'] = firebase_admin.initialize_app(
                cred, {'databaseURL': st.secrets['firebase_url']})
        except ValueError as e:
            st.session_state['ref'] = db.reference('/measurements')
            FirebaseRealtime.backup(st.session_state['ref'], measurements)
            col3.write('BACKUP SUCCEEDED')

    except (SqlAlchemyError, PyMySqlError):
        col2.write('BACKUP FAILED')

try:
    engine = MariaEngine()
    measurements = engine.read()
    Monitor.render(measurements)

    if (timestamp := datetime.now()) and timestamp.hour == 0 and 0 <= timestamp.minute <= 10:
        st.session_state['ref'] = db.reference('/measurements')
        FirebaseRealtime.backup(st.session_state['ref'], measurements)

except (SqlAlchemyError, PyMySqlError):
    st.write('Data from firebase backup.')
    st.session_state['ref'] = db.reference('/measurements')
    measurements = FirebaseRealtime.read_db(st.session_state['ref'])
    if measurements is None:
        st.write('No backup records available.')
    else:
        Monitor.render(measurements)
