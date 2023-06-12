import configparser

config = configparser.ConfigParser()
config.read("university/settings.ini")

POSTGRES_USER = "postgres"

POSTGRES_PASSWORD = config.get("university", "post_pass")

POSTGRES_HOSTNAME = "localhost"

DATABASE_PORT = "5432"

POSTGRES_DB = config.get("university", "post_db")

API_VERSION = "/api/v1"