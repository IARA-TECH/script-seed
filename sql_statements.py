import os
from enum import Enum

import psycopg2
from dotenv import load_dotenv
from termcolor import colored


load_dotenv()

class FetchEnum(Enum):
    FETCH_ALL = "all"
    FETCH_ONE = "one"
    NO_FETCH = "none"

class SqlStatements:
    def __init__(self):
        self.__conn = psycopg2.connect(
            host=os.getenv('POSTGRES_DB_HOST'), 
            database=os.getenv('POSTGRES_DB_DATABASE'), 
            user=os.getenv('POSTGRES_DB_USER'), 
            password=os.getenv('POSTGRES_DB_PASSWORD'), 
            port=os.getenv("POSTGRES_DB_PORT")
        )

    def open_connection(self) -> any:
        if self.__conn.closed == 0:
            self.__conn = psycopg2.connect(
                host=os.getenv('POSTGRES_DB_HOST'), 
                database=os.getenv('POSTGRES_DB_DATABASE'), 
                user=os.getenv('POSTGRES_DB_USER'), 
                password=os.getenv('POSTGRES_DB_PASSWORD'), 
                port=os.getenv("POSTGRES_DB_PORT")
            )
            return self.__conn
        else:
            raise RuntimeError("A connection is already opened, close it before opening a new one")
            

    def __execute_statement(self, query: str, error_message: str = None, vars: tuple = (), fetch: FetchEnum = FetchEnum.NO_FETCH) -> list:
        if self.__conn.closed == 1:
            raise RuntimeError("The connection is not opened")
        try:
            cur = self.__conn.cursor()
            cur.execute(query, vars)

            if fetch == FetchEnum.FETCH_ALL:
                returning = cur.fetchall()
            elif fetch == FetchEnum.FETCH_ONE:
                returning = cur.fetchone()
            else:
                returning = []

            cur.close()
            return returning
        
        except Exception as e:
            if error_message:
                print(colored(error_message, 'red'))
            cur.close()
            self.__conn.rollback()
            self.__conn.close()
            raise RuntimeError(e)

    def create_access_type(self, name:str, description:str) -> int:
        query = """
            INSERT INTO Access_Type (name, description)
            VALUES
            (%s, %s) RETURNING pk_id
        """
        vars = (name, description)
        access_type = self.__execute_statement(query=query, error_message="Error while creating access type", vars=vars, fetch=FetchEnum.FETCH_ONE)
        return access_type[0]

    def create_gender(self, name) -> int:
        query = """
            INSERT INTO Gender (name)
            VALUES
            (%s) RETURNING pk_id
        """
        vars = (name,)
        gender = self.__execute_statement(query=query, error_message="Error while creating gender", vars=vars, fetch=FetchEnum.FETCH_ONE)
        return gender[0]

    def create_payment_method(self, name) -> int:
        query = """
            INSERT INTO Payment_Method (name)
            VALUES
            (%s) RETURNING pk_id
        """
        vars = (name,)
        payment_method = self.__execute_statement(query=query, error_message="Error while creating payment method", vars=vars, fetch=FetchEnum.FETCH_ONE)
        return payment_method[0]
    
    def create_subscription(self, name:str, description:str, price:float, monthly_duration:int) -> int:
        query = """
            INSERT INTO Subscription (name, description, price, monthly_duration)
            VALUES (%s, %s, %s, %s)
            RETURNING pk_id
        """
        vars = (name, description, price, monthly_duration)
        subscription = self.__execute_statement(query=query, error_message="Error while creating subscription", vars=vars, fetch=FetchEnum.FETCH_ONE)
        return subscription[0]
        
    def create_factory(self, name: str, cnpj:str, domain:str, description:str) -> int:
        query = """
            INSERT INTO Factory (name, cnpj, domain, description)
            VALUES
            (
            %s,
            %s,
            %s,
            %s
            )
            RETURNING pk_id
        """
        vars = (name, cnpj, domain, description)
        factory = self.__execute_statement(query=query, error_message="Error while creating factory", vars=vars, fetch=FetchEnum.FETCH_ONE)
        return factory[0]

    def create_address(self, state:str, city:str, neighborhood: str, cep:str, street:str, building_number:int, complement:str, factory_id:int) -> int:
        query = """
            INSERT INTO Address (state, city, neighborhood, cep, street, building_number, complement, factory_id)
            VALUES
            (
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s
            ) RETURNING pk_id
        """
        vars = (state, city, neighborhood, cep, street, building_number, complement, factory_id)
        address = self.__execute_statement(query=query, error_message="Error while creating address", vars=vars, fetch=FetchEnum.FETCH_ONE)
        return address[0]

    def create_user_account_access_type(self, user_account_uuid: int, access_type_id:int) -> None:
        query = """
            INSERT INTO User_Account_Access_Type (user_account_uuid, access_type_id)
            VALUES 
            (
            %s,
            %s
            ) 
        """
        vars = (user_account_uuid, access_type_id)
        self.__execute_statement(query=query, error_message="Error while creating role access type", vars=vars, fetch=FetchEnum.NO_FETCH)
    
    def create_user_account(self, name:str, email:str, password:str, date_of_birth:str, gender_id:int, factory_id):
        query = """
            INSERT INTO User_Account (name, email, password, date_of_birth, gender_id, factory_id)
            VALUES
            (
            %s,
            %s,
            %s,
            %s,
            %s,
            %s
            )
            RETURNING pk_uuid
        """
        vars = (name, email, password, date_of_birth, gender_id, factory_id)
        user_account = self.__execute_statement(query=query, error_message="Error while creating user account", vars=vars, fetch=FetchEnum.FETCH_ONE)
        return user_account[0]

    def create_payment(self, paid_at:str, total:float, starts_at:str, expires_on:str, is_active:bool, is_expired:bool, subscription_id:int, user_account_uuid:str, payment_method:int) -> int:
        query = """
            INSERT INTO Payment (paid_at, total, starts_at, expires_on, is_active, is_expired, subscription_id, user_account_uuid, payment_method_id)
            VALUES
            (
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s
            ) RETURNING pk_id
        """
        vars = (paid_at, total, starts_at, expires_on, is_active, is_expired, subscription_id, user_account_uuid, payment_method)
        payment = self.__execute_statement(query=query, error_message="Error while creating payment", vars=vars, fetch=FetchEnum.FETCH_ONE)
        return payment[0]
    
    def close_connection(self) -> None:
        if self.__conn.closed == 1:
            raise RuntimeError("The connection is already closed.")
        self.__conn.commit()
        self.__conn.close()