from typing import Optional
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from pandas import DataFrame, read_sql

from .connection_string import get_connection_string


class MariaEngine:

    def __init__(self):
        self.engine: Optional[Engine] = self.get_engine()

    def read(self) -> DataFrame:
        with self.engine.connect() as connection:
            return read_sql('measurements', connection)

    @staticmethod
    def get_engine() -> Engine:
        return create_engine(get_connection_string())
