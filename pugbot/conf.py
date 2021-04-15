import os
import logging


# Set debug mode on or off
DEBUG = os.getenv("DEBUG", "False").lower() == "true"
DEFAULT_LOG_LEVEL = getattr(logging, os.getenv("DEFAULT_LOG_LEVEL", "INFO").upper())
DEFAULT_LOG_FORMATTER = os.getenv("DEFAULT_LOG_FORMATTER", "[%(name)s] [%(asctime)s] [%(levelname)s] %(message)s")
TEST_MODE = os.getenv("TEST_MODE", "False").lower() == "true"


# Mongo connection
MONGO_HOST = os.getenv("MONGO_HOST")
MONGO_PORT = os.getenv("MONGO_PORT")
MONGO_USERNAME = os.getenv("MONGO_USERNAME")
MONGO_PASSWORD = os.getenv("MONGO_PASSWORD")


# Discord Bot
TOKEN = os.getenv("TOKEN")
PREFIX = os.getenv("PREFIX", "pugbot.")  # Prefix for the commands

# Testing config
TEST_CHANNEL_ID = os.getenv("TEST_CHANNEL_ID")