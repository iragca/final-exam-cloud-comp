import subprocess
from pprint import pprint

import polars as pl
from tqdm import tqdm
from typer import Typer

from src.config import (
    EXTERNAL_DATA_DIR,
    STAGING_DATABASE_URL,
    WAREHOUSE_DATABASE_URL,
    logger,
)
from src.data import Staging, Warehouse
from src.utils import int_to_datetime, remove_dash

cli = Typer()


@cli.command()
def move_to_staging():
    """
    Moves data from external CRM and ERP source directories into the staging database.
    This function reads CSV files from predefined CRM and ERP source directories,
    loads them into DataFrames, and inserts them into corresponding tables in the
    staging database. Progress is displayed using tqdm for both CRM and ERP tables.
    Logs a success message upon completion.
    Raises:
        FileNotFoundError: If any of the source CSV files are missing.
        Exception: If there is an error during data loading or insertion.
    """
    SOURCE_CRM = EXTERNAL_DATA_DIR / "source_crm"
    SOURCE_ERP = EXTERNAL_DATA_DIR / "source_erp"
    STAGING = Staging(STAGING_DATABASE_URL)

    SOURCE_CRM_TABLES = [
        "cust_info",
        "prd_info",
        "sales_details",
    ]

    SOURCE_ERP_TABLES = [
        "CUST_AZ12",
        "LOC_A101",
        "PX_CAT_G1V2",
    ]

    for table in tqdm(SOURCE_CRM_TABLES, desc="Loading CRM tables"):
        df = pl.read_csv(SOURCE_CRM / f"{table}.csv")
        STAGING.insert_table(df, table)

    for table in tqdm(SOURCE_ERP_TABLES, desc="Loading ERP tables"):
        df = pl.read_csv(SOURCE_ERP / f"{table}.csv")
        STAGING.insert_table(df, table)

    logger.success("Data moved to staging successfully.")


@cli.command()
def read_staging():
    """
    Reads all table names from the staging database, retrieves their schema information, and prints the details.
    This function:
    - Connects to the staging database using the `Staging` class and `STAGING_DATABASE_URL`.
    - Retrieves a list of all table names in the staging database.
    - For each table, fetches and prints its schema or metadata information using `get_table_info`.
    - Outputs the table names, their count, and detailed information for each table.
    Returns:
        None
    """
    STAGING = Staging(STAGING_DATABASE_URL)
    tables = STAGING.get_table_names()
    print("TABLES: ", tables, len(tables))

    for table in tables:
        table_info = STAGING.get_table_info(table)
        print(f"{table}: ")
        print("=" * 20)
        pprint(table_info)


@cli.command()
def drop_staging():
    """
    Drops all tables from the staging database.

    This function initializes a connection to the staging database using the
    configured `STAGING_DATABASE_URL`, drops all tables within the staging
    environment, and logs a success message upon completion.
    """
    STAGING = Staging(STAGING_DATABASE_URL)
    STAGING.drop_all_tables()
    logger.success("All tables in staging dropped successfully.")


@cli.command()
def move_to_data_warehouse():
    """
    Extracts data from staging tables, preprocesses it, and loads it into the data warehouse.
    This function performs the following steps:
    1. Connects to the staging and warehouse databases.
    2. Retrieves tables from the staging database, including customer info, product info, sales details, and others.
    3. Defines preprocessing functions for each table, which:
        - Remove duplicate and null records.
        - Cast columns to appropriate data types (e.g., categorical, date).
        - Convert integer date representations to date objects where necessary.
    4. Loads the cleaned and transformed data into the corresponding warehouse tables.
    5. Logs a success message upon completion.
    Assumes that the following are defined elsewhere:
    - `Staging` and `Warehouse` classes for database connections.
    - `STAGING_DATABASE_URL` and `WAREHOUSE_DATABASE_URL` for connection strings.
    - `pl` (Polars) for DataFrame operations.
    - `int_to_datetime` for converting integer dates.
    - `logger` for logging.
    """
    STAGING = Staging(STAGING_DATABASE_URL)
    WAREHOUSE = Warehouse(WAREHOUSE_DATABASE_URL)

    cust_info = STAGING.get_table("cust_info")
    prd_info = STAGING.get_table("prd_info")
    sales_details = STAGING.get_table("sales_details")
    cust_az12 = STAGING.get_table("cust_az12")
    loc_a101 = STAGING.get_table("loc_a101")
    px_cat_g1v2 = STAGING.get_table("px_cat_g1v2")

    @WAREHOUSE.preprocess_and_load()
    def process_cust_info(cust_info: pl.DataFrame, table_name: str = "cust_info"):
        return (
            cust_info.unique()
            .drop_nulls()
            .with_columns(
                [
                    pl.col("cst_gndr").cast(pl.Categorical),
                    pl.col("cst_marital_status").cast(pl.Categorical),
                    pl.col("cst_create_date").cast(pl.Date),
                ]
            )
        )

    @WAREHOUSE.preprocess_and_load()
    def process_prd_info(prd_info: pl.DataFrame, table_name: str = "prd_info"):
        return (
            prd_info.unique()
            .drop_nulls()
            .with_columns(
                [
                    pl.col("prd_line").cast(pl.Categorical),
                    pl.col("prd_start_dt").cast(pl.Date),
                    pl.col("prd_end_dt").cast(pl.Date),
                ]
            )
        )

    @WAREHOUSE.preprocess_and_load()
    def process_sales_details(sales_details: pl.DataFrame, table_name: str = "sales_details"):
        return (
            sales_details.unique()
            .drop_nulls()
            .with_columns(
                [
                    pl.col("sls_order_dt").map_elements(
                        lambda x: int_to_datetime(x), return_dtype=pl.Date
                    ),
                    pl.col("sls_ship_dt").map_elements(
                        lambda x: int_to_datetime(x), return_dtype=pl.Date
                    ),
                    pl.col("sls_due_dt").map_elements(
                        lambda x: int_to_datetime(x), return_dtype=pl.Date
                    ),
                ]
            )
        ).drop_nulls()

    @WAREHOUSE.preprocess_and_load()
    def process_cust_az12(cust_az12: pl.DataFrame, table_name: str = "cust_az12"):
        return (
            cust_az12.unique()
            .drop_nulls()
            .with_columns([pl.col("GEN").cast(pl.Categorical), pl.col("BDATE").cast(pl.Date)])
        )

    @WAREHOUSE.preprocess_and_load()
    def process_loc_a101(loc_a101: pl.DataFrame, table_name: str = "loc_a101"):
        return (
            loc_a101.unique()
            .drop_nulls()
            .with_columns(
                [
                    pl.col("CID").map_elements(lambda x: remove_dash(x), return_dtype=pl.Utf8).alias("CID"),
                ]
            )
        )

    @WAREHOUSE.preprocess_and_load()
    def process_px_cat_g1v2(px_cat_g1v2: pl.DataFrame, table_name: str = "px_cat_g1v2"):
        return px_cat_g1v2.unique().drop_nulls()

    process_cust_info(cust_info, table_name="cust_info")
    process_prd_info(prd_info, table_name="prd_info")
    process_sales_details(sales_details, table_name="sales_details")
    process_cust_az12(cust_az12, table_name="cust_az12")
    process_loc_a101(loc_a101, table_name="loc_a101")
    process_px_cat_g1v2(px_cat_g1v2, table_name="px_cat_g1v2")
    logger.success("Data preprocessed and loaded to warehouse successfully.")


@cli.command()
def read_warehouse():
    """
    Reads and prints information about all tables in the warehouse.
    This function connects to the warehouse using the global `WAREHOUSE_DATABASE_URL`,
    retrieves the list of table names, and for each table, prints its name and detailed
    information using pretty-print formatting.
    Returns:
        None
    """
    WAREHOUSE = Warehouse(WAREHOUSE_DATABASE_URL)
    tables = WAREHOUSE.get_table_names()
    print("TABLES: ", tables, len(tables))

    for table in tables:
        table_info = WAREHOUSE.get_table_info(table)
        print(f"{table}: ")
        print("=" * 20)
        pprint(table_info)


@cli.command()
def drop_warehouse():
    """
    Drops all tables from the warehouse database.

    This function initializes a Warehouse instance using the configured database URL,
    removes all tables from the warehouse, and logs a success message upon completion.
    """
    WAREHOUSE = Warehouse(WAREHOUSE_DATABASE_URL)
    WAREHOUSE.drop_all_tables()
    logger.success("All tables in warehouse dropped successfully.")


@cli.command()
def start_streamlit(port: int = 8501, host: str = "0.0.0.0"):
    """
    Start the Streamlit dashboard on a specified host and port.

    This CLI command builds a command-line instruction to run `streamlit run dashboard.py`
    with optional host and port arguments, then executes it using `subprocess.run`.

    Args:
        port (int): Port to serve the Streamlit app on (default: 8501).
        host (str): Host IP address to bind the server to (default: "0.0.0.0").
    """
    process = ["streamlit", "run", "dashboard.py"]

    if port:
        process += ["--server.port", str(port)]

    if host:
        process += ["--server.address", host]

    subprocess.run(process)


if __name__ == "__main__":
    cli()
