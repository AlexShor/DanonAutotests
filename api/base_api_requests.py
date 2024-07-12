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

        self._request = self.__Request(self)
        self._create_params = self.__Create_params(self)

        if auth_creds:
            self._login, self._password = auth_creds

    class __Request:
        def __init__(self, cls):
            """ cls - instance ...ApiRequests """

            self._cls = cls

        @staticmethod
        def __check_status_code(func):
            @functools.wraps(func)
            def wrapper(self, *args, lvl_rec=1, **kwargs):

                response = func(self, *args, **kwargs)
                response.encoding = 'UTF-8'

                status_code = response.status_code

                match status_code:

                    case 401:
                        print('lvl_rec', lvl_rec)
                        print('response', response)

                        access_token = self._cls.refresh_tokens().json().get('access')
                        print('access_token', access_token)
                        args[0]['headers'] = {'Authorization': f'Bearer {access_token}'}
                        print('args', args)
                        lvl_rec += 1
                        response = wrapper(self, *args, lvl_rec, **kwargs)
                        print('response', response)

                    case 502:
                        raise requests.exceptions.ConnectionError()

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

    class __Create_params:
        def __init__(self, base_api):
            self._base_api = base_api
            self.__dict__.update(base_api.__dict__)

        def __collect_params(self, url: str, params: dict = None, json: dict = None,
                             form_data: dict = None, have_access_token: bool = True):

            headers = {'Authorization': f'Bearer {self._access_token}'} if have_access_token else None
            request_parameters = {'url': url,
                                  'headers': headers,
                                  'params': params,
                                  'json': json,
                                  'data': form_data,
                                  'verify': False}

            return request_parameters

        def for_scenario(self, scenario_id: int = None, params: dict = None,
                         url_additional_path: str = None, json: dict = None) -> dict:

            scenario_id = '' if scenario_id is None else '/' + str(scenario_id)
            url_additional_path = '' if url_additional_path is None else '/' + str(url_additional_path)

            url = f'{self._base_url}/{self._optimizer_type}-scenarios{scenario_id}{url_additional_path}'
            return self.__collect_params(url, params, json)

        def for_input(self, scenario_id: int, input_data: dict, request_url_param: str = '', params: dict = None) -> dict:

            query_params = {}
            if params is not None:
                query_params.update(params)

            params_input_type = input_data.get('parameter')
            if params_input_type is not None:
                query_params.update({'input_type': params_input_type})

            url_input_path = input_data.get('url_path')
            optimizer_type = self._optimizer_type

            url_input_path = (f'/{url_input_path}', '')[url_input_path is None]
            inputs_in_url = ('/inputs', '')[optimizer_type == 'promo']

            url = (f'{self._base_url}/{optimizer_type}-scenarios/{scenario_id}'
                   f'{url_input_path}{inputs_in_url}{request_url_param}')
            return self.__collect_params(url, query_params)

        def for_output_kpi(self, scenario_id: int) -> dict:

            url_path = ('/results/kpi', '/promo-result-kpi')[self._optimizer_type == 'promo']

            url = f'{self._base_url}/{self._optimizer_type}-scenarios/{scenario_id}{url_path}'
            return self.__collect_params(url)

        def for_output_tables(self, scenario_id: int, output_table_type: str, query_params: dict = None) -> dict:

            optimizer_type = self._optimizer_type

            if optimizer_type == 'promo':
                url_path = output_table_type
            else:
                url_path = 'outputs'
                query_params.update({'output_type': output_table_type})

            url = f'{self._base_url}/{optimizer_type}-scenarios/{scenario_id}/results/{url_path}'
            return self.__collect_params(url, query_params)

        def for_account(self, route: str, params: dict = None, json: dict = None) -> dict:

            url = f'{self._base_url}/account/{route}'
            return self.__collect_params(url, params, json)

        def for_tokens(self, url_param: str, form_data: dict = None):

            url = f'{self._base_url}/auth/{url_param}'
            return self.__collect_params(url, form_data=form_data, have_access_token=False)

    @log_api_status(1)
    def get_tokens(self):

        form_data = {"email": self._login, "password": self._password}

        response = self._request.post(self._create_params.for_tokens('login', form_data))

        # if response.status_code < 300:
        self._access_token = response.json().get('access')
        self._refresh_token = response.json().get('refresh')

        return response

    @log_api_status(1)
    def refresh_tokens(self):

        form_data = {"refresh": self._refresh_token}
        response = self._request.post(self._create_params.for_tokens('refresh', form_data))

        self._access_token = response.json().get('access')
        self._refresh_token = response.json().get('refresh')

        return response
