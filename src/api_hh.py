from typing import Dict, List, Union

import requests


class HHAPI:
    BASE_URL = "https://api.hh.ru"

    def get_employers(self, employer_ids: List[str]) -> List[Dict]:
        """
        Получает данные о работодателях по их ID
        """
        employers = []
        for emp_id in employer_ids:
            url = f"{self.BASE_URL}/employers/{emp_id}"
            response = requests.get(url)
            if response.status_code == 200:
                employers.append(response.json())
            else:
                print(f"Ошибка при получении данных о работодателе {emp_id}")
        return employers

    def get_vacancies(self, employer_id: str) -> List[Dict]:
        """
        Получает список вакансий конкретного работодателя
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
