import streamlit as st
import firebase_admin
from firebase_admin import credentials, db
import json


@st.cache_resource
def initialize_firebase_realtime():
    cred = credentials.Certificate(dict(st.secrets["textkey"]))
    firebase_admin.initialize_app(cred)

# ref = db.reference("/")
