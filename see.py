import streamlit as st
from sqlalchemy.exc import OperationalError as SqlAlchemyError
from pymysql.err import OperationalError as PyMySqlError

from db import MariaEngine
from firebase import initialize_firebase_realtime
from monitor import Monitor

st.set_page_config(page_title='Loof monitor', page_icon='🛸')

initialize_firebase_realtime()

try:
    engine = MariaEngine.get_engine()
    Monitor.update(engine)
except (SqlAlchemyError, PyMySqlError):
    st.write('Connection to database failed.\nSoon you will be seeing a backup here.')
    # TODO: create a local sqlite3 db:
        # 1. as backup for data
        # 2. as backup for rendering

st.button('REFRESH')
