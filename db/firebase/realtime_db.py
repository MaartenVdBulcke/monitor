from typing import Optional
import streamlit as st
import firebase_admin
from firebase_admin import credentials, db
from pandas import DataFrame, to_datetime


class FirebaseRealtime:

    @staticmethod
    def initialise_firebase():
        try:
            cred = credentials.Certificate(dict(st.secrets["textkey"]))
            st.session_state['firebase'] = firebase_admin.initialize_app(cred,
                                                                         {'databaseURL': st.secrets['firebase_url']})
            st.session_state['ref'] = db.reference('/measurements')
        except ValueError:
            pass

    @staticmethod
    def read_db(ref) -> Optional[DataFrame]:
        backup_records = ref.get()
        if backup_records is None:
            return None
        df = DataFrame.from_records(ref.get())
        df.timestamp_utc = to_datetime(df.timestamp_utc)
        return df

    @staticmethod
    def backup(ref, df: DataFrame):
        """Replaces all the data stored in MySql to the Firebase realtime database.
        This procedure is performed every day around midnight."""
        df.timestamp_utc = df.timestamp_utc.astype('str')
        ref.set(df.to_dict('records'))
