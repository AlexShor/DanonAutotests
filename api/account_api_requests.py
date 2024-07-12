from api.base_api_requests import BaseApiRequests
from custom_moduls.console_design.console_decorator import log_api_status

import requests


class AccountApiRequests(BaseApiRequests):

    @log_api_status(2)
    def get_personal_info(self) -> requests.Response:
        response = self._request.get(self._create_params.for_account('personal-info'))

        return response

    @log_api_status(2, ['json_body'])
    def change_personal_info(self, json_body: dict) -> requests.Response:
        response = self._request.patch(self._create_params.for_account('personal-info', json=json_body))

        return response
