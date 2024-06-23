from api.base_api_requests import BaseApiRequests
from custom_moduls.console_design.console_decorator import log_api_status

import requests


class InputApiRequests(BaseApiRequests):

    def __extract_input_params(self, scenario_id: int, input_data: dict, request_url_param: str = '') -> dict:

        url_input_path = input_data.get('url_path')
        params_input_type = input_data.get('parameter')
        optimizer_type = self._optimizer_type

        url_input_path = (f'/{url_input_path}', '')[url_input_path is None]
        inputs_in_url = ('/inputs', '')[optimizer_type == 'promo']

        params = ({'input_type': params_input_type}, None)[params_input_type is None]
        headers = {'Authorization': f'Bearer {self._access_token}'}

        url = (f'{self._base_url}/{optimizer_type}-scenarios/{scenario_id}'
               f'{url_input_path}{inputs_in_url}{request_url_param}')

        request_parameters = {'url': url, 'headers': headers, 'params': params, 'verify': False}

        return request_parameters

    def _requests_get(self, scenario_id: int, input_data: dict, request_url_param: str) -> requests.Response:

        request_parameters = self.__extract_input_params(scenario_id, input_data, request_url_param)

        response = self.request.get(request_parameters)

        return response

    def _requests_post(self, scenario_id: int, input_data: dict, request_url_param: str = '',
                       files: dict = None) -> requests.Response:

        request_parameters = self.__extract_input_params(scenario_id, input_data, request_url_param)

        if files is not None:
            request_parameters.update(files)

        response = self.request.post(request_parameters)

        return response

    def _requests_delete(self, scenario_id: int, input_data: dict, request_url_param: str = '') -> requests.Response:

        request_parameters = self.__extract_input_params(scenario_id, input_data, request_url_param)

        response = self.request.delete(request_parameters)

        return response

    @log_api_status(2)
    def get_preview_data(self, scenario_id: int, input_data: dict) -> requests.Response:

        request_url_param = '/data'

        response = self._requests_get(scenario_id, input_data, request_url_param)

        return response

    @log_api_status(2)
    def get_input_log(self, scenario_id: int, input_data: dict) -> requests.Response:

        request_url_param = '/log'

        response = self._requests_get(scenario_id, input_data, request_url_param)

        return response

    @log_api_status(2)
    def get_input_data(self, scenario_id: int, input_data: dict) -> requests.Response:

        request_url_param = '/download'

        response = self._requests_get(scenario_id, input_data, request_url_param)

        return response

    @log_api_status(2)
    def get_input_info(self, scenario_id: int, input_data: dict) -> requests.Response:

        request_url_param = '/info'

        response = self._requests_get(scenario_id, input_data, request_url_param)

        return response

    @log_api_status(2)
    def upload_input_file(self, scenario_id: int, input_data: dict, file_path: str) -> requests.Response:

        files = {'files': {'file': open(f'{file_path}', 'rb')}}

        response = self._requests_post(scenario_id, input_data, files=files)

        return response

    @log_api_status(2)
    def delete_input_file(self, scenario_id: int, input_data: dict) -> requests.Response:

        response = self._requests_delete(scenario_id, input_data)

        return response


# if __name__ == "__main__":
#     environment = 'LOCAL_STAGE'
#     scenario_id = 406
#     inputs_data = InputData('cfr').get_from_json()
#
#     session = InputApiRequests(environment).authorization(*Credentials.auth(env=environment).values())
#
#
#     data = session.get_input_info(scenario_id, inputs_data['dlc'])
#
#     print(data.json())
#
#     # with open(f'optimizer_data_tests.xlsx', 'wb') as file:
#     #     file.write(data.content)
