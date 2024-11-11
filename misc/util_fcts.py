from dotenv import load_dotenv
import os
import sqlalchemy
import json
import logging

def get_env():
    load_dotenv()
    DB_HOST = os.getenv("DB_HOST")
    DB_NAME = os.getenv("DB_NAME")
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_PORT = os.getenv("DB_PORT")
    return (DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME)


def connect2DB():
    params = get_env()
    engine = sqlalchemy.create_engine(f"postgresql://{params[0]}:{params[1]}@{params[2]}:{params[3]}/{params[4]}")
    return engine

def get_config():
    with open("config.json", "r") as file:
        config = json.load(file)
    
    return config

def get_logging():
    logging.basicConfig(filename='query_errors.log', level=logging.ERROR,
                        format='%(asctime)s - %(levelname)s - %(message)s')
    logger = logging.getLogger(__name__)
    return logger