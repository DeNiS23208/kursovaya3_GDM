import psycopg2
from typing import List, Dict
from db_config import DB_PARAMS


def insert_companies(companies: List[Dict]):
    connection = psycopg2.connect(**DB_PARAMS)
    cursor = connection.cursor()

    for company in companies:
        cursor.execute(
            """
            INSERT INTO companies (hh_id, name, description, site_url)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (hh_id) DO NOTHING;
        """,
            (
                company.get("id"),
                company.get("name"),
                company.get("description"),
                company.get("site_url"),
            ),
        )

    connection.commit()
    cursor.close()
    connection.close()
    print(f"В таблицу companies добавлено {len(companies)} компаний.")


def insert_vacancies(vacancies: List[Dict], company_id: int):
    connection = psycopg2.connect(**DB_PARAMS)
    cursor = connection.cursor()

    for vacancy in vacancies:
        salary = vacancy.get("salary")
        salary_from = salary["from"] if salary else None
        salary_to = salary["to"] if salary else None
        currency = salary["currency"] if salary else None

        cursor.execute(
            """
            INSERT INTO vacancies (title, salary_from, salary_to, currency, url, company_id)
            VALUES (%s, %s, %s, %s, %s,
                (SELECT company_id FROM companies WHERE hh_id = %s)
            );
        """,
            (
                vacancy.get("name"),
                salary_from,
                salary_to,
                currency,
                vacancy.get("alternate_url"),
                company_id,
            ),
        )

    connection.commit()
    cursor.close()
    connection.close()
    print(
        f"В таблицу vacancies добавлено {len(vacancies)} вакансий для компании {company_id}."
    )
