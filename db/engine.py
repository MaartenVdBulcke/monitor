import streamlit as st
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine

from .connection_string import get_connection_string


class MariaEngine:

    @staticmethod
    @st.cache_resource
    def get_engine() -> Engine:
        return create_engine(get_connection_string())
