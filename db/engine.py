from sqlalchemy import create_engine
from sqlalchemy.engine import Engine

from .connection_string import get_connection_string


class MariaEngine:

    @staticmethod
    def get_engine() -> Engine:
        return create_engine(get_connection_string())

