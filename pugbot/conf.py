import os
import logging


# Main Python settings
DEBUG = os.getenv("DEBUG", "False").lower() == "true"
TEST_MODE = os.getenv("TEST_MODE", "False").lower() == "true"
DEFAULT_LOG_LEVEL = getattr(
    logging, os.getenv("DEFAULT_LOG_LEVEL", "INFO").upper()
)
DEFAULT_LOG_FORMATTER = os.getenv(
    "DEFAULT_LOG_FORMATTER",
    "[%(name)s] [%(asctime)s] [%(levelname)s] %(message)s"
)


# PostgreSQL connection
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")


# Discord Bot
TOKEN = os.getenv("TOKEN")
PREFIX = os.getenv("PREFIX", ".")  # Prefix for the commands

# Testing config
TEST_CHANNEL_ID = os.getenv("TEST_CHANNEL_ID")