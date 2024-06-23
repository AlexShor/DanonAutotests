from api.base_api_requests import BaseApiRequests
from custom_moduls.console_design.console_decorator import log_api_status

import requests


class ScenarioApiRequests(BaseApiRequests):

    def __extract_input_params(self, scenario_id: int = None, params: dict = None, json: dict = None) -> dict:

        if scenario_id is None:
            scenario_id = ''
        else:
            scenario_id = '/' + str(scenario_id)

        headers = {'Authorization': f'Bearer {self._access_token}'}

        url = f'{self._base_url}/{self._optimizer_type}-scenarios{scenario_id}'

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

    # @log_api_status(2)
    # def create_scenario(self, scenario_id: int, input_data: dict) -> requests.Response:
    #
    #     request_url_param = '/download'
    #
    #     response = self._requests_get(scenario_id, input_data, request_url_param)
    #
    #     return response
    #
    # @log_api_status(2)
    # def update_scenario(self, scenario_id: int, input_data: dict) -> requests.Response:
    #
    #     request_url_param = '/info'
    #
    #     response = self._requests_get(scenario_id, input_data, request_url_param)
    #
    #     return response
    #
    # @log_api_status(2)
    # def delete_scenario(self, scenario_id: int, input_data: dict) -> requests.Response:
    #
    #     response = self._requests_delete(scenario_id, input_data)
    #
    #     return response


# if __name__ == "__main__":
#     env = 'LOCAL_STAGE'
#     scen_api = ScenarioApiRequests(env, optimizer_type='promo')
#     resp = scen_api.get_scenario(1709)
#
#     print(resp)
