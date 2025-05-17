from src.data import DataStorage


class Staging(DataStorage):
    def __init__(self, url):
        super().__init__(url)

    def preprocess_table(self, table: str):
        """
        Preprocess the table before inserting it into the staging database.
        """
        # Implement any preprocessing logic here
        pass
