from api.base_api_requests import BaseApiRequests
from custom_moduls.console_design.console_decorator import log_api_status

import requests


# class ScenarioApiRequests(BaseApiRequests):
#
#     def __extract_input_params(self,
#                                scenario_id: int = None,
#                                params: dict = None,
#                                url_additional_path: str = None,
#                                json: dict = None) -> dict:
#
#         scenario_id = '' if scenario_id is None else '/' + str(scenario_id)
#         url_additional_path = '' if url_additional_path is None else '/' + str(url_additional_path)
#
#         headers = {'Authorization': f'Bearer {self._access_token}'}
#         url = f'{self._base_url}/{self._optimizer_type}-scenarios{scenario_id}{url_additional_path}'
#         request_parameters = {'url': url, 'headers': headers, 'params': params, 'json': json, 'verify': False}
#
#         return request_parameters
#
#     @log_api_status(2)
#     def create_scenario(self, json_body: dict) -> requests.Response:
#
#         request_parameters = self.__extract_input_params(json=json_body)
#
#         response = self.request.post(request_parameters)
#
#         return response
#
#     @log_api_status(2)
#     def get_list_of_scenarios(self, params: dict = None) -> requests.Response:
#
#         request_parameters = self.__extract_input_params(params=params)
#
#         response = self.request.get(request_parameters)
#
#         return response
#
#     @log_api_status(2, additional_info='scenario_id')
#     def get_scenario(self, scenario_id: int) -> requests.Response:
#
#         request_parameters = self.__extract_input_params(scenario_id)
#
#         response = self.request.get(request_parameters)
#
#         return response
#
#     @log_api_status(2, additional_info='scenario_id')
#     def delete_scenario(self, scenario_id: int) -> requests.Response:
#
#         request_parameters = self.__extract_input_params(scenario_id)
#
#         response = self.request.delete(request_parameters)
#
#         return response
#
#     @log_api_status(2, additional_info='pfr_url')
#     def save_scenario_pfr(self, scenario_id: int, pfr_url: str, json_body: dict) -> requests.Response:
#
#         request_parameters = self.__extract_input_params(scenario_id, url_additional_path=pfr_url, json=json_body)
#
#         if self._optimizer_type == 'cfr':
#             response = self.request.patch(request_parameters)
#         else:
#             response = self.request.post(request_parameters)
#
#         return response
#
#     @log_api_status(2, additional_info='scenario_id')
#     def calculation(self, scenario_id: int) -> requests.Response:
#
#         json_body = {}
#         addition_url = 'calculation'
#
#         request_parameters = self.__extract_input_params(scenario_id, url_additional_path=addition_url, json=json_body)
#
#         response = self.request.post(request_parameters)
#
#         return response
#
#     @log_api_status(2, additional_info='scenario_id')
#     def revoke(self, scenario_id: int) -> requests.Response:
#
#         json_body = {}
#         addition_url = 'revoke'
#
#         request_parameters = self.__extract_input_params(scenario_id, url_additional_path=addition_url, json=json_body)
#
#         response = self.request.post(request_parameters)
#
#         return response


class ScenarioApiRequests(BaseApiRequests):
    def __init__(self, environment: str, auth_tokens: dict = None, optimizer_type: str = None):
        super().__init__(environment, auth_tokens, optimizer_type)

        self.scenario = self.__Scenario(self)
        self.input = self.__Input(self)
        self.output = self.__Output(self)

    class __Scenario:
        def __init__(self, base_api):
            self._base_api = base_api
            self.__dict__.update(base_api.__dict__)

        @log_api_status(2)
        def create_scenario(self, json_body: dict) -> requests.Response:

            request_parameters = self._create_params.for_scenario(json=json_body)

            response = self._request.post(request_parameters)

            return response

        @log_api_status(2)
        def get_list_of_scenarios(self, params: dict = None) -> requests.Response:

            request_parameters = self._create_params.for_scenario(params=params)

            response = self._request.get(request_parameters)

            return response

        @log_api_status(2, ['scenario_id'])
        def get_scenario(self, scenario_id: int) -> requests.Response:

            request_parameters = self._create_params.for_scenario(scenario_id)

            response = self._request.get(request_parameters)

            return response

        @log_api_status(2, ['scenario_id'])
        def delete_scenario(self, scenario_id: int) -> requests.Response:

            request_parameters = self._create_params.for_scenario(scenario_id)

            response = self._request.delete(request_parameters)

            return response

        @log_api_status(2, ['pfr_url'])
        def save_scenario_pfr(self, scenario_id: int, pfr_url: str, json_body: dict) -> requests.Response:

            request_parameters = self._create_params.for_scenario(scenario_id,
                                                                 url_additional_path=pfr_url,
                                                                 json=json_body)

            if self._optimizer_type == 'cfr':
                response = self._request.patch(request_parameters)
            else:
                response = self._request.post(request_parameters)

            return response

        @log_api_status(2, ['scenario_id'])
        def calculation(self, scenario_id: int) -> requests.Response:

            json_body = {}
            addition_url = 'calculation'

            request_parameters = self._create_params.for_scenario(scenario_id,
                                                                 url_additional_path=addition_url,
                                                                 json=json_body)

            response = self._request.post(request_parameters)

            return response

        @log_api_status(2, ['scenario_id'])
        def revoke(self, scenario_id: int) -> requests.Response:

            json_body = {}
            addition_url = 'revoke'

            request_parameters = self._create_params.for_scenario(scenario_id,
                                                                 url_additional_path=addition_url,
                                                                 json=json_body)

            response = self._request.post(request_parameters)

            return response

    class __Input:
        def __init__(self, base_api):
            self._base_api = base_api
            self.__dict__.update(base_api.__dict__)

        @log_api_status(2)
        def get_preview_data(self, scenario_id: int, input_data: dict) -> requests.Response:

            request_parameters = self._create_params.for_input(scenario_id, input_data, request_url_param='/data')
            response = self._request.get(request_parameters)

            return response

        @log_api_status(2)
        def get_input_log(self, scenario_id: int, input_data: dict) -> requests.Response:

            request_parameters = self._create_params.for_input(scenario_id, input_data, request_url_param='/log')
            response = self._request.get(request_parameters)

            return response

        @log_api_status(2)
        def get_input_data(self, scenario_id: int, input_data: dict) -> requests.Response:

            request_parameters = self._create_params.for_input(scenario_id, input_data, request_url_param='/download')
            response = self._request.get(request_parameters)

            return response

        @log_api_status(2)
        def get_input_info(self, scenario_id: int, input_data: dict) -> requests.Response:

            request_parameters = self._create_params.for_input(scenario_id, input_data, request_url_param='/info')
            response = self._request.get(request_parameters)

            return response

        @log_api_status(2, ['params'])
        def upload_input_data(self, scenario_id: int, input_data: dict,
                              file_path: str = None, params: dict = None) -> requests.Response:  # upload_input_file

            request_parameters = self._create_params.for_input(scenario_id, input_data, params=params)

            if file_path is not None:

                try:
                    files = {'files': {'file': open(f'{file_path}', 'rb')}}
                except FileNotFoundError as exc:
                    return exc

                if files is not None:
                    request_parameters.update(files)

            response = self._request.post(request_parameters)

            return response

        @log_api_status(2)
        def delete_input_file(self, scenario_id: int, input_data: dict) -> requests.Response:

            request_parameters = self._create_params.for_input(scenario_id, input_data)
            response = self._request.delete(request_parameters)

            return response

    class __Output:
        def __init__(self, base_api):
            self._base_api = base_api
            self.__dict__.update(base_api.__dict__)

        @log_api_status(2, ['scenario_id'])
        def get_kpi_data(self, scenario_id: int) -> requests.Response:

            request_parameters = self._create_params.for_output_kpi(scenario_id)
            response = self._request.get(request_parameters)

            return response

        @log_api_status(2, ['scenario_id', 'output_table_type'])
        def get_preview_output_table(self, scenario_id: int, output_table_type: str, query_params: dict = None) -> requests.Response:

            if query_params is None:
                query_params = {}

            query_params.update({'limit': 50})

            request_parameters = self._create_params.for_output_tables(scenario_id, output_table_type, query_params)
            response = self._request.get(request_parameters)

            return response
