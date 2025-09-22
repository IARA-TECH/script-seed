import os
import random
import sys

import bcrypt
import psycopg2
from dotenv import load_dotenv
from faker import Faker
from termcolor import colored

load_dotenv()

fake = Faker("pt_BR")

conn = psycopg2.connect(host=os.getenv('DB_HOST'), database=os.getenv('DB_DATABASE'), user=os.getenv('DB_USER'), password=os.getenv('DB_PASSWORD'), port=os.getenv("DB_PORT"))

def execute_query(query: str, ok_message: str, error_message: str, vars: list = ()) -> list:
    try:
        cur = conn.cursor()
        cur.execute(query, vars)
        result = cur.fetchall()
        cur.close()
        print(colored(ok_message, 'green'))
        return result
    
    except Exception as e:
        print(colored(error_message,'red'))
        print(e)
        cur.close()
        conn.rollback()
        conn.close()
        sys.exit(1)
