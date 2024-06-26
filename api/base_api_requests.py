import functools

from custom_moduls.console_design.console_decorator import log_api_status
from pages.site_data.urls import BaseUrls
from dotenv import load_dotenv

import requests
import urllib3

load_dotenv()
urllib3.disable_warnings()


class BaseApiRequests:
    def __init__(self,
                 environment: str,
                 auth_tokens: dict = None,
                 optimizer_type: str = None,
                 auth_creds: tuple = None) -> None:

        self._environment = environment
        self._optimizer_type = optimizer_type
        self._base_url = f'{BaseUrls.BASE_URLS_BACK.get(environment)}/api'

        if auth_tokens:
            self._access_token = auth_tokens.get('access')
            self._refresh_token = auth_tokens.get('refresh')

        #self._auth_tokens = auth_tokens

        self.request = self.Request(self)

        if auth_creds:
            self._login, self._password = auth_creds
            #self.get_tokens()

    class Request:
        def __init__(self, cls):
            """ cls - instance ...ApiRequests """

            self._cls = cls

        @staticmethod
        def __check_status_code(func):
            @functools.wraps(func)
            def wrapper(self, *args, **kwargs):

                response = func(self, *args, **kwargs)
                response.encoding = 'UTF-8'

                status_code = response.status_code

                if status_code == 401:

                    access_token = self._cls.get_tokens()[0]
                    args[0]['headers'] = {'Authorization': f'Bearer {access_token}'}

                    response = wrapper(self, *args, **kwargs)

                return response

            return wrapper

        @__check_status_code
        def get(self, request_parameters: dict):
            return requests.get(**request_parameters)

        @__check_status_code
        def post(self, request_parameters: dict):
            return requests.post(**request_parameters)

        @__check_status_code
        def patch(self, request_parameters: dict):
            return requests.patch(**request_parameters)

        @__check_status_code
        def delete(self, request_parameters: dict):
            return requests.delete(**request_parameters)

    @log_api_status(1)
    def get_tokens(self):

        url = f'{self._base_url}/auth/login'
        form_data = {"email": self._login, "password": self._password}

        request_parameters = {'url': url, 'data': form_data, 'verify': False}

        response = self.request.post(request_parameters)

        self._access_token = response.json().get('access')
        self._refresh_token = response.json().get('refresh')

        #self._auth_tokens = response.json()

        return response
