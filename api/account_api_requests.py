from api.base_api_requests import BaseApiRequests
from custom_moduls.console_design.console_decorator import log_api_status

import requests


class AccountApiRequests(BaseApiRequests):

    def __extract_input_params(self, route: str, params: dict = None, json: dict = None) -> dict:

        headers = {'Authorization': f'Bearer {self._access_token}'}
        url = f'{self._base_url}/account/{route}'
        request_parameters = {'url': url, 'headers': headers, 'params': params, 'json': json, 'verify': False}

        return request_parameters

    @log_api_status(2)
    def get_personal_info(self) -> requests.Response:
        response = self.request.get(self.__extract_input_params('personal-info'))

        return response

    @log_api_status(2, additional_info='json_body')
    def change_personal_info(self, json_body: dict) -> requests.Response:
        response = self.request.patch(self.__extract_input_params('personal-info', json=json_body))

        return response
