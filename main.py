from api_hh import HHAPI
from create_db import create_database, create_tables
from user_interface import run_interface
from vacancies_handler import insert_companies, insert_vacancies


def main():
    # Создание базы данных
    create_database("kursovaya_gdm")  # Имя должно совпадать с DB_NAME в .env

    # Создание таблиц
    create_tables()

    # Получение данных от API
    hh = HHAPI()
    employer_ids = [
        "3529",
        "1740",
        "78638",
        "4181",
        "80",
        "3776",
        "907345",
        "2748",
        "3776",
        "4934",
    ]
    employers = hh.get_employers(employer_ids)

    # Загрузка компаний в БД
    insert_companies(employers)

    # Загрузка вакансий в БД
    for emp in employers:
        print(f"Загружаем вакансии для {emp['name']}...")
        vacancies = hh.get_vacancies(emp["id"])
        insert_vacancies(vacancies, emp["id"])

    # Запуск пользовательского интерфейса
    run_interface()


if __name__ == "__main__":
    main()
