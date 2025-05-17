from pprint import pprint

import polars as pl
from tqdm import tqdm
from typer import Typer

from src.config import EXTERNAL_DATA_DIR, STAGING_DATABASE_URL, logger
from src.data import Staging

cli = Typer()


@cli.command()
def move_to_staging():
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
    STAGING = Staging(STAGING_DATABASE_URL)
    STAGING.delete_all_tables()
    logger.success("All tables dropped successfully.")


@cli.command()
def move_to_data_warehouse():
    pass


@cli.command()
def start_streamlit():
    pass


if __name__ == "__main__":
    cli()
