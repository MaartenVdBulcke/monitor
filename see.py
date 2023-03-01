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
        try:
            cred = credentials.Certificate(dict(st.secrets["textkey"]))
            st.session_state['firebase'] = firebase_admin.initialize_app(cred,
                                                                         {'databaseURL': st.secrets['firebase_url']})
            st.session_state['ref'] = db.reference('/measurements')
        except KeyError as e:
            st.write('BACKUP FAILED', type(e).__name__, format_exc())
        except ValueError as e:
            FirebaseRealtime.backup(st.session_state['ref'], measurements)
            st.write('BACKUP SUCCEEDED')

    except (SqlAlchemyError, PyMySqlError):
        st.write('BACKUP FAILED')
