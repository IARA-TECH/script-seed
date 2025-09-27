import random
import re
from datetime import timedelta, datetime
import unicodedata

import bcrypt
from faker import Faker
from termcolor import colored

from sql_statements import SqlStatements

fake = Faker("pt_BR")
fake.email()
sql_statements = SqlStatements()

def print_success_message(message: str, results: any = None) -> None:
    print(colored(message, "green"))
    if results:
        print(colored(f"Results: {results}", "cyan"))

def hash_password(password) -> str:
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed.decode("utf-8")

def format_name(name:str) ->str:
    titles = ["Sr. ", "Sra. ","Dr. ", "Dra. ", "Srta. "]
    for title in titles:
        name = name.replace(title, '')
    return name
    
def create_email(name:str, domain:str) -> str:
    nkfd = unicodedata.normalize("NFKD", name)
    name = "".join(c for c in nkfd if not unicodedata.combining(c))
    name = name.title().replace(' ','')
    return f"{name}@{domain}"

# Creating access types
access_types = {
    "Administrador": sql_statements.create_access_type(
        "Administrador",
        "Pode criar cargos, realizar pagamentos e visualizar informações sensíveis sobre a fábrica",
    ),
    "Supervisor": sql_statements.create_access_type(
        "Supervisor",
        "Pode revisar e aprovar solicitações de alterações nos relatórios",
    ),
    "Solicitante": sql_statements.create_access_type(
        "Solicitante", "Pode solicitar alterações nos relatórios."
    ),
    "Visualizador": sql_statements.create_access_type(
        "Visualizador", "Pode visualizar relatórios e informações do sistema."
    ),
}
print_success_message("Access types created", access_types)

# Creating genders
genders = {
    "Feminino": sql_statements.create_gender("Feminino"),
    "Masculino": sql_statements.create_gender("Masculino"),
    "Outro": sql_statements.create_gender("Outro"),
}
print_success_message("Genders created", genders)

# Creating payment methods
payment_methods = {
    "Crédito": sql_statements.create_payment_method("Crédito"),
    "Débito": sql_statements.create_payment_method("Débito"),
    "Pix": sql_statements.create_payment_method("Pix"),
}
print_success_message("Payment methods created", payment_methods)

# Creating the subscription
subscription_id = sql_statements.create_subscription("Mar Profundo", fake.text(200), 1610.00, 1)

for _ in range(3):
    factory_domain = fake.unique.domain_name()
    # Creating factory
    factory_id = sql_statements.create_factory(
        fake.unique.company(),
        re.sub(r"\D", "", (fake.unique.cnpj())),
        factory_domain,
        fake.text(200),
    )
    print_success_message("Factory created", factory_id)

    # Creating address
    address_id = sql_statements.create_address(
        fake.state(),
        fake.city(),
        fake.neighborhood(),
        re.sub(r"\D", "", fake.unique.postcode()),
        fake.street_name(),
        fake.building_number(),
        fake.text(50),
        factory_id,
    )
    print_success_message(f"Address for factory {factory_id} created", address_id)

    for i in range(random.randint(3, 4)):
        if i == 0:
            access_types_ids = [
                access_types["Administrador"],
                access_types["Visualizador"],
            ]
        elif i == 1:
            access_types_ids = [
                access_types["Supervisor"],
                access_types["Visualizador"],
            ]
        elif i == 2:
            access_types_ids = [
                access_types["Solicitante"],
                access_types["Visualizador"],
            ]
        else:
            access_types_ids = [access_types["Visualizador"]]

        for _ in range(random.randint(4, 6)):
            gender_choice = random.randint(1, 5)
            if gender_choice in {1, 2}:
                user_name = format_name(fake.name_female())
                user_gender_id = genders["Feminino"]
            elif gender_choice in {3, 4}:
                user_name = format_name(fake.name_male())
                user_gender_id = genders["Masculino"]
            else:
                user_name = format_name(fake.name_nonbinary())
                user_gender_id = genders["Outro"]

            user_email = create_email(user_name, factory_domain)
            user_password = hash_password(fake.password())

            # Creating user accounts
            user_id = sql_statements.create_user_account(
                user_name,
                user_email,
                user_password,
                fake.date_of_birth(minimum_age=20, maximum_age=60),
                user_gender_id,
                factory_id
            )
            print_success_message("User created", user_id)

            # Creating user account access type
            for access_type_id in access_types_ids:
                sql_statements.create_user_account_access_type(user_id, access_type_id)
                print_success_message(f'Relation between user account with id {user_id} and access type with id {access_type_id} created', {"user_account_uuid":user_id, "access_type_id":access_type_id})

            if i == 0:
                user_id_who_paid = user_id
            # Creating user account role

        if user_id_who_paid:
            paid_at = datetime.now()
            starts_at = paid_at
            expires_on = starts_at + timedelta(days=30)

            payment_method_id = random.choice(list(payment_methods.values()))

            payment_id = sql_statements.create_payment(
                paid_at,
                1610.00,
                starts_at,
                expires_on,
                True,
                False,
                subscription_id,
                user_id_who_paid,
                payment_method_id,
            )
            print_success_message(f"Payment for factory {factory_id} created", payment_id)

sql_statements.close_connection()