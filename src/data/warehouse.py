from sqlalchemy import text

from src.data import DataStorage


class Warehouse(DataStorage):
    def __init__(self, url):
        super().__init__(url)

    def load_data(_self, table_name):
        """
        Load data from the warehouse.
        """
        with _self.engine.connect() as connection:
            QUERY = f"SELECT * FROM {table_name}"
            result = connection.execute(text(QUERY))
            return result.fetchall()
