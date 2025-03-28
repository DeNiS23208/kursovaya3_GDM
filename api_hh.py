from typing import List, Dict, Union
import requests


class HHAPI:
    BASE_URL = "https://api.hh.ru"

    def get_vacancies(self, employer_id: str) -> List[Dict]:
        """
        Получает вакансии конкретного работодателя

        :param employer_id: ID работодателя
        :return: Список словарей с вакансиями
        """
        vacancies = []
        page = 0
        while True:
            url = f"{self.BASE_URL}/vacancies"
            params: dict[str, Union[str, int]] = {
                "employer_id": employer_id,
                "page": page,
                "per_page": 100,
            }
            response = requests.get(url, params=params)
            if response.status_code != 200:
                print(f"Ошибка при получении вакансий для работодателя {employer_id}")
                break

            data = response.json()
            vacancies.extend(data.get("items", []))

            if page >= data.get("pages", 0) - 1:
                break
            page += 1

        return vacancies
