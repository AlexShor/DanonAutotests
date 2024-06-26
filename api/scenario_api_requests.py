from api.base_api_requests import BaseApiRequests
from custom_moduls.console_design.console_decorator import log_api_status

import requests


class ScenarioApiRequests(BaseApiRequests):

    def __extract_input_params(self,
                               scenario_id: int = None,
                               params: dict = None,
                               pfr_url: str = None,
                               json: dict = None) -> dict:

        scenario_id = '' if scenario_id is None else '/' + str(scenario_id)
        pfr_url = '' if pfr_url is None else '/' + str(pfr_url)

        headers = {'Authorization': f'Bearer {self._access_token}'}
        url = f'{self._base_url}/{self._optimizer_type}-scenarios{scenario_id}{pfr_url}'
        request_parameters = {'url': url, 'headers': headers, 'params': params, 'json': json, 'verify': False}

        return request_parameters

    @log_api_status(2)
    def create_scenario(self, json_body: dict) -> requests.Response:

        request_parameters = self.__extract_input_params(json=json_body)

        response = self.request.post(request_parameters)

        return response

    @log_api_status(2)
    def get_list_of_scenarios(self, params: dict = None) -> requests.Response:

        request_parameters = self.__extract_input_params(params=params)

        response = self.request.get(request_parameters)

        return response

    @log_api_status(2, additional_info='scenario_id')
    def get_scenario(self, scenario_id: int) -> requests.Response:

        request_parameters = self.__extract_input_params(scenario_id)

        response = self.request.get(request_parameters)

        return response

    @log_api_status(2, additional_info='scenario_id')
    def delete_scenario(self, scenario_id: int) -> requests.Response:

        request_parameters = self.__extract_input_params(scenario_id)

        response = self.request.delete(request_parameters)

        return response

    @log_api_status(2, additional_info='pfr_url')
    def save_scenario_pfr(self, scenario_id: int, pfr_url: str, json_body: dict) -> requests.Response:

        request_parameters = self.__extract_input_params(scenario_id, pfr_url=pfr_url, json=json_body)

        if self._optimizer_type == 'cfr':
            response = self.request.patch(request_parameters)
        else:
            response = self.request.post(request_parameters)

        return response
