# Script Seed

Desenvolvimento de um **script automatizado em Python** para **popular bancos de dados SQL e MongoDB** com dados iniciais (seed), facilitando a configuração e replicação de ambientes de desenvolvimento, teste e produção.  

O projeto foi criado com foco em **agilidade, padronização e automação**, podendo ser integrado a pipelines de **CI/CD** para execução contínua.

---

## 📚 Sumário

* [💡 Sobre o Projeto](#-sobre-o-projeto)
* [⚙️ Tecnologias Utilizadas](#️-tecnologias-utilizadas)
* [🧩 Como Executar](#-como-executar)
* [🧰 Estrutura do Projeto](#-estrutura-do-projeto)
* [👩‍💻 Autor](#-autor)

---

## 💡 Sobre o Projeto

O **Script Seed** é uma aplicação em **Python** que automatiza o processo de inserção de dados em bancos **SQL** e **MongoDB**, garantindo que aplicações tenham dados consistentes e prontos para uso logo após a inicialização.

Este projeto foi desenvolvido para:

* Criar e inserir dados iniciais de forma **rápida e reprodutível**.
* Fornecer uma camada de abstração para **MongoDB** e **SQL**, através dos arquivos `mongo_statements.py` e `sql_statements.py`.
* Permitir a **configuração via variáveis de ambiente** (arquivo `.env`).
* Integrar-se facilmente a **pipelines automatizadas**, como o **GitHub Actions**.

---

## ⚙️ Tecnologias Utilizadas

| Categoria                         | Tecnologias / Ferramentas                                      |
| --------------------------------- | --------------------------------------------------------------- |
| **Linguagem**                     | Python 3.9+                                                    |
| **Banco de Dados**                | MongoDB, MySQL / PostgreSQL                                    |
| **Automação / CI/CD**             | GitHub Actions (`.github/workflows/cicd.yml`)                  |
| **Gerenciamento de Dependências** | `pip`, `requirements.txt`                                      |
| **Ambiente**                      | Variáveis de ambiente via `.env` e `.env.example`              |
| **Bibliotecas Principais**        | `pymongo`, `psycopg2`, `python-dotenv`, `mysql-connector-python` |

---

## 🧩 Como Executar

### 🧱 Executando Localmente

```bash
# Clone o repositório
git clone https://github.com/SEU_USUARIO/script-seed-main.git

# Acesse o diretório
cd script-seed-main

# Crie o ambiente virtual
python -m venv venv

# Ative o ambiente
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

# Instale as dependências
pip install -r requirements.txt
````
---

### ▶️ Executando o Script

Para executar o seed de dados:

```bash
python seed.py
```

O script identificará automaticamente o tipo de banco configurado (`SQL` ou `Mongo`) e executará as instruções correspondentes dos arquivos:

* `sql_statements.py` → para bancos relacionais
* `mongo_statements.py` → para bancos não relacionais

---

## 🧰 Estrutura do Projeto

```
script-seed-main/
├── .env.example          # Exemplo de variáveis de ambiente
├── .gitignore            # Arquivos ignorados pelo Git
├── LICENSE               # Licença do projeto
├── README.md             # Documentação do projeto
├── requirements.txt      # Dependências Python
├── seed.py               # Script principal de execução
├── mongo_statements.py   # Scripts de inserção para MongoDB
├── sql_statements.py     # Scripts de inserção para SQL
└── .github/
    └── workflows/
        └── cicd.yml      # Pipeline de CI/CD automatizado
```

---

## 👩‍💻 Autor

**IARA Tech**

Projeto Interdisciplinar desenvolvido por alunos do 1º e 2º ano de ensino médio do Instituto J&F, com o propósito de facilitar o registro e consulta de ábacos industriais.

📍 São Paulo, Brasil
📧 [iaratech.oficial@gmail.com](mailto:iaratech.oficial@gmail.com)
🌐 GitHub: [https://github.com/IARA-TECH](https://github.com/IARA-TECH)
