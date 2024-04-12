from pages.site_data.urls import BaseUrls
from dotenv import load_dotenv

import requests
import urllib3

load_dotenv()
urllib3.disable_warnings()


class BaseApiRequests:
    def __init__(self, environment: str = 'DEV') -> None:

        self._environment = environment
        self._base_url = f'{BaseUrls.BASE_URLS_BACK.get(environment)}/api'
        self._login = None
        self._password = None
        self._access_token = None
        self._refresh_token = None

    @staticmethod
    def __check_status_code(response: requests):
        status_code = response.status_code

        if status_code >= 500:
            return status_code, None
        elif status_code >= 400:
            return status_code, response.text
        elif status_code >= 300:
            return status_code, response
        elif status_code >= 200:
            return status_code, response
        elif status_code >= 100:
            return status_code, response
        else:
            return None

    def authorization(self, login: str, password: str):
        print('authorization')
        url = f'{self._base_url}/auth/login'
        form_data = {"email": login, "password": password}

        response = requests.post(url=url, verify=False, data=form_data)

        response.encoding = 'UTF-8'

        self._access_token = response.json().get('access')
        self._refresh_token = response.json().get('refresh')

        return self


if __name__ == "__main__":
    environment = 'LOCAL_STAGE'
    scenario_id = 466
