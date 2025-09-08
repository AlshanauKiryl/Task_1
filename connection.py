import os
import psycopg2 as postgre
from dotenv import load_dotenv
import logging
load_dotenv()
logging.basicConfig(level=logging.INFO, filename="py_log.log",filemode="w")

def connection():
    '''функция подключения к Бд'''
    conn = postgre.connect(os.getenv('DB_URL'))
    logging.info('Connection to DB established')
    return conn