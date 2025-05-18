import os
import pathlib

from dotenv import load_dotenv
from loguru import logger

PROJECT_ROOT = pathlib.Path(__file__).parent.parent.resolve()
DATA_DIR = PROJECT_ROOT / "data"

RAW_DATA_DIR = DATA_DIR / "raw"
EXTERNAL_DATA_DIR = DATA_DIR / "external"
INTERIM_DATA_DIR = DATA_DIR / "interim"
PROCESSED_DATA_DIR = DATA_DIR / "processed"

if not (PROJECT_ROOT / ".env").exists():
    raise FileNotFoundError(f"Please create a .env file in the root directory ({PROJECT_ROOT})")

load_dotenv(PROJECT_ROOT / ".env")
STAGING_DATABASE_URL = os.getenv("STAGING_DATABASE_URL")
WAREHOUSE_DATABASE_URL = os.getenv("WAREHOUSE_DATABASE_URL")


def check_env_variable(var, var_name: str):
    """Check if an environment variable is set."""
    if var is None:
        raise EnvironmentError(f"Environment variable {var_name} is not set.")


check_env_variable(STAGING_DATABASE_URL, "STAGING_DATABASE_URL")
check_env_variable(WAREHOUSE_DATABASE_URL, "WAREHOUSE_DATABASE_URL")


logger.info(f"PROJECT_ROOT: {PROJECT_ROOT}")
logger.info(f"DATA_DIR: {DATA_DIR}")
