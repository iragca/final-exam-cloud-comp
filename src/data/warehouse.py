from functools import wraps
from src.data import DataStorage
from src.config import logger


class Warehouse(DataStorage):
    def __init__(self, url):
        super().__init__(url)

    def preprocess_and_load(self):
        """
        Decorator to preprocess and load data into the warehouse.
        """

        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                # Preprocess step
                data = func(*args, **kwargs)

                # Load into warehouse
                table_name = kwargs.get("table_name", "default_table").lower()
                with self.engine.connect() as connection:
                    data.write_database(
                        table_name=table_name,
                        connection=connection,
                        if_table_exists="replace",
                    )
                logger.info(f"'{table_name}' loaded into warehouse.")
                return data  # optionally return processed data

            return wrapper

        return decorator
