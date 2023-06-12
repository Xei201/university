import configparser

config = configparser.ConfigParser()
config.read("university/settings.ini")

POSTGRES_USER = config.get("university", "POSTGRES_USER")

POSTGRES_PASSWORD = config.get("university", "POSTGRES_PASSWORD")

POSTGRES_HOSTNAME = config.get("university", "POSTGRES_HOSTNAME")

DATABASE_PORT = config.get("university", "DATABASE_PORT")

POSTGRES_DB = config.get("university", "POSTGRES_DB")

API_VERSION = "/api/v1"