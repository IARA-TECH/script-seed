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

def execute_query(query: str, ok_message: str, error_message: str, vars: tuple = ()) -> list:
    try:
        cur = conn.cursor()
        cur.execute(query, vars)
        result = cur.fetchall()
        cur.close()
        print(colored(ok_message, 'green'))
        return result
    
    except Exception as e:
        print(colored(error_message,'red'))
        print(colored(e, 'red'))
        cur.close()
        conn.rollback()
        conn.close()
        sys.exit(1)

# Creating access types
query = """
    INSERT INTO Access_Type (name, description)
    VALUES
    (
    'Administrador',
    'Pode criar cargos, realizar pagamentos e visualizar informações sensíveis sobre a fábrica'
    ),
    (
    'Supervisor',
    'Pode revisar e aprovar solicitações de alterações nos relatórios'
    ),
    (
    'Solicitante',
    'Pode solicitar alterações nos relatórios.'
    ),
    (
    'Visualizador',
    'Pode visualizar relatórios e informações do sistema.'
    )
    RETURNING name, pk_id
"""
access_types = execute_query(query=query, ok_message='Access types created', error_message='Error while creating access types')
access_types = {access_type[0]:access_type[1] for access_type in access_types}

# Creating genders
query = """
    INSERT INTO Gender (name)
    VALUES
    (
    'Feminino'
    ),
    (
    'Masculino'
    ),
    (
    'Outro'
    )
    RETURNING name, pk_id
"""
genders = execute_query(query=query, ok_message="Genders created", error_message="Error while creating genders")
genders = {gender[0]: gender[1] for gender in genders}

# Creating payment methods
query = """
    INSERT INTO Payment_Method (name)
    VALUES 
    (
    'Crédito'
    ),
    (
    'Débito'
    ),
    (
    'Pix'
    )
    RETURNING name, pk_id
"""
payment_methods = execute_query(query=query, ok_message="Payment methods created", error_message="Error while creating payment methods")
payment_methods = {payment_method[0]: payment_method[1] for payment_method in payment_methods}

# Creating the subscription
query = """
    INSERT INTO Subscription (name, description, price, monthly_duration)
    VALUES
    (
    'Mar Profundo',
    %s,
    1610,
    1
    ) 
    RETURNING pk_id
"""
vars = (fake.text(200),)
subscription = (execute_query(query=query, vars=vars, ok_message="Subscription created", error_message="Error while creating subscription"))[0]