import psycopg2
from db_config import DB_PARAMS


def create_tables():
    connection = psycopg2.connect(**DB_PARAMS)
    connection.autocommit = True
    cursor = connection.cursor()

    # Создание таблицы компаний
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS companies (
            company_id SERIAL PRIMARY KEY,
            hh_id INTEGER UNIQUE, -- <== Добавлено UNIQUE!
            name TEXT NOT NULL,
            description TEXT,
            site_url TEXT
        );
        """
    )

    # Создание таблицы вакансий
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS vacancies (
        vacancy_id SERIAL PRIMARY KEY,
        title TEXT NOT NULL,
        salary_from INTEGER,
        salary_to INTEGER,
        currency TEXT,
        url TEXT,
        company_id INTEGER REFERENCES companies(company_id) ON DELETE CASCADE
    );
    """
    )

    cursor.close()
    connection.close()
    print("База данных и таблицы успешно созданы.")


if __name__ == "__main__":
    create_tables()
