from db_manager import DBManager


def run_interface():
    db = DBManager()

    while True:
        print("\nВыберите действие:")
        print("1 - Показать компании и количество вакансий")
        print("2 - Показать все вакансии")
        print("3 - Показать среднюю зарплату")
        print("4 - Показать вакансии с зарплатой выше средней")
        print("5 - Поиск вакансий по ключевому слову")
        print("0 - Выход")

        choice = input("Ваш выбор: ")

        if choice == "1":
            data = db.get_companies_and_vacancies_count()
            for name, count in data:
                print(f"{name}: {count} вакансий")

        elif choice == "2":
            data = db.get_all_vacancies()
            for company, title, salary, url in data:
                print(f"{company} | {title} | {salary or 'ЗП не указана'} | {url}")

        elif choice == "3":
            avg = db.get_avg_salary()
            print(f"Средняя зарплата: {int(avg)} руб.")

        elif choice == "4":
            data = db.get_vacancies_with_higher_salary()
            for title, salary in data:
                print(f"{title} — {salary} руб.")

        elif choice == "5":
            keyword = input("Введите ключевое слово для поиска: ")
            data = db.get_vacancies_with_keyword(keyword)
            if data:
                for title, url in data:
                    print(f"{title}: {url}")
            else:
                print("Ничего не найдено.")

        elif choice == "0":
            db.close()
            print("До свидания!")
            break

        else:
            print("Неверный выбор, попробуйте снова.")
