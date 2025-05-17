import polars as pl
from sqlalchemy import create_engine, inspect, text, MetaData

from src.config import logger


class DataStorage:
    def __init__(self, url):
        self.engine = create_engine(url, client_encoding="utf8")
        self.inspector = inspect(self.engine)

    def get_table_names(self):
        try:
            with self.engine.connect():
                return self.inspector.get_table_names()
        except Exception as e:
            logger.error(f"Error retrieving table names: {e}")
            return None

    def get_table_info(self, table_name):
        try:
            with self.engine.connect():
                return self.inspector.get_columns(table_name)
        except Exception as e:
            logger.error(f"Error retrieving table info: {e}")
            return None

    def get_table(self, table_name: str):
        """
        Load data from the warehouse.
        """
        try:
            with self.engine.connect() as connection:
                QUERY = f"SELECT * FROM {table_name}"
                result = connection.execute(text(QUERY))
                return pl.DataFrame(result.fetchall())
        except Exception as e:
            logger.error(f"Error retrieving table data: {e}")

    def insert_table(self, table: pl.DataFrame, table_name: str):
        """
        Insert data into the staging database.
        """
        try:
            with self.engine.connect() as connection:
                table.write_database(
                    table_name=table_name.lower(),
                    connection=connection,
                    if_table_exists="replace",
                )

        except Exception as e:
            logger.error(f"Error inserting table data: {e}")
            raise e

    def drop_table(self, table_name: str):
        """
        Delete a table from the staging database.
        """
        try:
            with self.engine.connect() as connection:
                connection.execute(text(f"DROP TABLE IF EXISTS {table_name}"))
        except Exception as e:
            logger.error(f"Error deleting table: {e}")
            raise e

    def drop_all_tables(self):
        """
        Delete all tables from the staging database.
        """
        try:
            meta = MetaData()
            meta.reflect(bind=self.engine)
            meta.drop_all(bind=self.engine)
            logger.success("All tables deleted successfully.")
        except Exception as e:
            logger.error(f"Error deleting all tables: {e}")
            raise e
