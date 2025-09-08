import os
import psycopg2 as postgre
from dotenv import load_dotenv
load_dotenv()

def connection():
    '''функция подключения к Бд'''
    conn = postgre.connect(os.getenv('DB_URL'))
    return conn