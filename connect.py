import os
from urllib.parse import quote_plus

from sqlalchemy import create_engine, text
from get_data import load_customer_data


def quote_value(value: str) -> str:
    return quote_plus(value)


def create_database_if_needed(username: str, password: str, host: str, port: str, database: str):
    admin_url = (
        f"mysql+pymysql://{quote_value(username)}:{quote_value(password)}@{host}:{port}/"
    )
    engine = create_engine(admin_url)
    with engine.connect() as conn:
        conn = conn.execution_options(isolation_level='AUTOCOMMIT')
        conn.execute(
            text(
                f"CREATE DATABASE IF NOT EXISTS `{database}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"
            )
        )
    print(f"Database '{database}' is ready.")


def upload_to_mysql(df, username: str, password: str, host: str, port: str, database: str):
    db_url = (
        f"mysql+pymysql://{quote_value(username)}:{quote_value(password)}@{host}:{port}/{database}"
    )
    engine = create_engine(db_url)
    df.to_sql(name='customers', con=engine, if_exists='replace', index=False)
    print(f"Data uploaded successfully to MySQL database '{database}'.")


def main():
    username = os.getenv('MYSQL_USER', 'root')
    password = os.getenv('MYSQL_PASSWORD', 'Shiwam@808460')
    host = os.getenv('MYSQL_HOST', '127.0.0.1')
    port = os.getenv('MYSQL_PORT', '3306')
    database = os.getenv('MYSQL_DATABASE', 'customer_behavior')

    df = load_customer_data()

    create_database_if_needed(username, password, host, port, database)
    upload_to_mysql(df, username, password, host, port, database)


if __name__ == '__main__':
    main()