import psycopg2
from typing import List, Tuple
from db_config import DB_PARAMS


class DBManager:
    def __init__(self):
        self.conn = psycopg2.connect(**DB_PARAMS)
        self.cursor = self.conn.cursor()

    def get_companies_and_vacancies_count(self) -> List[Tuple[str, int]]:
        """Возвращает список компаний и количество вакансий в каждой"""
        self.cursor.execute(
            """
            SELECT c.name, COUNT(v.vacancy_id)
            FROM companies c
            LEFT JOIN vacancies v ON c.company_id = v.company_id
            GROUP BY c.name;
        """
        )
        return self.cursor.fetchall()

    def get_all_vacancies(self) -> List[Tuple[str, str, int, str]]:
        """Возвращает список всех вакансий с названием компании,
        названием вакансии, зарплатой и ссылкой"""
        self.cursor.execute(
            """
            SELECT c.name, v.title, v.salary_from, v.url
            FROM vacancies v
            JOIN companies c ON v.company_id = c.company_id;
        """
        )
        return self.cursor.fetchall()

    def get_avg_salary(self) -> float:
        """Возвращает среднюю зарплату по всем вакансиям"""
        self.cursor.execute(
            """
            SELECT AVG(salary_from) FROM vacancies
            WHERE salary_from IS NOT NULL;
        """
        )
        result = self.cursor.fetchone()
        return result[0] if result else 0

    def get_vacancies_with_higher_salary(self) -> List[Tuple[str, int]]:
        """Возвращает вакансии с зарплатой выше средней"""
        avg_salary = self.get_avg_salary()
        self.cursor.execute(
            """
            SELECT title, salary_from FROM vacancies
            WHERE salary_from > %s;
        """,
            (avg_salary,),
        )
        return self.cursor.fetchall()

    def get_vacancies_with_keyword(self, keyword: str) -> List[Tuple[str, str]]:
        """Возвращает вакансии, в названии которых есть ключевое слово"""
        self.cursor.execute(
            """
            SELECT title, url FROM vacancies
            WHERE title ILIKE %s;
        """,
            (f"%{keyword}%",),
        )
        return self.cursor.fetchall()

    def close(self):
        self.cursor.close()
        self.conn.close()
