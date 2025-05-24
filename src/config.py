import os
import pathlib

from dotenv import load_dotenv
from loguru import logger
from src.utils import check_env_variable


PROJECT_ROOT = pathlib.Path(__file__).parent.parent.resolve()
DATA_DIR = PROJECT_ROOT / "data"

RAW_DATA_DIR = DATA_DIR / "raw"
EXTERNAL_DATA_DIR = DATA_DIR / "external"
INTERIM_DATA_DIR = DATA_DIR / "interim"
PROCESSED_DATA_DIR = DATA_DIR / "processed"

if not (PROJECT_ROOT / ".env").exists():
    logger.warning(FileNotFoundError(f"No .env file found in the root directory ({PROJECT_ROOT})"))

load_dotenv(PROJECT_ROOT / ".env")
STAGING_DATABASE_URL = os.getenv("STAGING_DATABASE_URL")
WAREHOUSE_DATABASE_URL = os.getenv("WAREHOUSE_DATABASE_URL")

try:
    check_env_variable(STAGING_DATABASE_URL, "STAGING_DATABASE_URL", important=False)
    check_env_variable(WAREHOUSE_DATABASE_URL, "WAREHOUSE_DATABASE_URL", important=True)
except EnvironmentError as e:
    logger.error(e)
    raise


logger.info(f"PROJECT_ROOT: {PROJECT_ROOT}")
logger.info(f"DATA_DIR: {DATA_DIR}")
