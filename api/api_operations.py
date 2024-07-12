import functools
import os
import time

import requests

from api.base_api_requests import BaseApiRequests
# from api.input_api_requests import InputApiRequests
from api.scenario_api_requests import ScenarioApiRequests
from api.account_api_requests import AccountApiRequests
from optimizer_data.operations_file_data import OperationsFileData


class ApiOperations:
    def __init__(self,
                 environment: str,
                 optimizer_type: str,
                 scenario_id: int = None,
                 auth_creds: tuple = None) -> None:

        self._environment = environment
        self._optimizer_type = optimizer_type
        self._scenario_id = scenario_id

        auth_tokens = BaseApiRequests(environment, auth_creds=auth_creds).get_tokens().json()
        self._auth_tokens = auth_tokens

        self._account_api = None
        self._scenario_api = None
        self._input_api = None
        self._output_api = None

        self.personal_info = None
        self.scenario_data = None

    class __integrate_api_request:
        @staticmethod
        def _get(type_api):

            def _decorator(func):
                @functools.wraps(func)
                def _wrapper(*args, **kwargs):

                    self = args[0]
                    environment = self._environment
                    auth_tokens = self._auth_tokens
                    optimizer_type = self._optimizer_type

                    match type_api:

                        case 'account_api':
                            if self._account_api is None:
                                self._account_api = AccountApiRequests(environment, auth_tokens, optimizer_type)

                        case 'scenario_api':
                            if self._scenario_api is None:
                                self._scenario_api = ScenarioApiRequests(environment, auth_tokens,
                                                                         optimizer_type).scenario

                        case 'input_api':
                            if self._input_api is None:
                                self._input_api = ScenarioApiRequests(environment, auth_tokens, optimizer_type).input

                        case 'output_api':
                            if self._output_api is None:
                                self._output_api = ScenarioApiRequests(environment, auth_tokens, optimizer_type).output

                    result = func(*args, **kwargs)

                    return result

                return _wrapper

            return _decorator

        account_api = _get('account_api')
        scenario_api = _get('scenario_api')
        input_api = _get('input_api')
        output_api = _get('output_api')

    def _check_scenario_type(self) -> str:

        scenario_data = self.get_scenario()

        scenario_type = scenario_data.get(f'{self._optimizer_type.lower()}_type')

        if scenario_type:
            scenario_type = scenario_type.get('code')

        return scenario_type

    @__integrate_api_request.input_api
    def wait_file_info(self, input_data: dict, waited_file_info: dict):
        """
        waited_file_info = {'key': value, 'key': value, ...}
        """

        checking = True

        while checking:
            time.sleep(1)

            response = self._input_api.get_input_info(self._scenario_id, input_data)

            if response.status_code < 300:

                for key, value in waited_file_info.items():
                    if response.json().get(key) == value:
                        checking = False

            elif response.status_code >= 400:
                checking = False

            time.sleep(4)

    @__integrate_api_request.input_api
    def upload_input_files(self,
                           inputs_data: dict,
                           files_directory: str = None,
                           files_type: str = None,
                           wait_file_validation: bool = True,
                           use_download_file_name: bool = False) -> dict:

        scenario_type = self._check_scenario_type()

        response_data = {}

        def api_request_upload_input_data(input_data, file_name, file_path):

            def make_not_download():
                return self._input_api.upload_input_data(self._scenario_id, input_data,
                                                         params={'optional_upload': True})

            if input_data.get('not_download') or isinstance(file_path, Exception):
                response = make_not_download()
            else:
                response = self._input_api.upload_input_data(self._scenario_id, input_data, file_path)

                if wait_file_validation and response.status_code < 300:
                    self.wait_file_info(input_data, {
                        'uploading_status': True,
                        'data_uploading_status': 'Data successfully uploaded'
                    })

            response_data[file_name] = response

        for input_name, input_data in inputs_data.items():

            optimization_type = input_data.get('optimization_type')

            if use_download_file_name:
                input_name = input_data.get('download_file_name')

            if optimization_type is None or scenario_type in optimization_type:

                if files_directory is None:
                    file_path = input_data.get('full_path')

                elif files_type is None:
                    file_path = OperationsFileData.determine_file_type(files_directory, input_name)

                else:
                    file_path = f'{files_directory}/{input_name}.{files_type}'

                if isinstance(file_path, list):

                    for f_path in file_path:
                        f_name = f_path.split('/')[-1].split('.')[0].lower()
                        input_data['system_file_name'] = f_name

                        api_request_upload_input_data(input_data, f_name, f_path)

                else:

                    api_request_upload_input_data(input_data, input_name, file_path)

        return response_data

    @__integrate_api_request.input_api
    def delete_input_files(self, inputs_data: dict) -> dict:

        scenario_type = self._check_scenario_type()

        response_about_deletion = {}

        for input_name, input_data in inputs_data.items():

            optimization_type = input_data.get('optimization_type')

            if optimization_type is None or scenario_type in optimization_type:
                response = self._input_api.delete_input_file(self._scenario_id, input_data)

                response_about_deletion[input_name] = response

        return response_about_deletion

    @__integrate_api_request.input_api
    def get_input_logs(self, inputs_data: dict) -> dict:

        scenario_type = self._check_scenario_type()

        input_logs = {}

        for input_name, input_data in inputs_data.items():

            optimization_type = input_data.get('optimization_type')

            if optimization_type is None or scenario_type in optimization_type:

                response = self._input_api.get_input_log(self._scenario_id, input_data)

                if response.status_code < 300:
                    input_logs[input_name] = response.text

        return input_logs

    @__integrate_api_request.input_api
    def get_preview_data(self, inputs_data: dict) -> dict:

        scenario_type = self._check_scenario_type()

        preview_data = {}

        for input_name, input_data in inputs_data.items():

            optimization_type = input_data.get('optimization_type')

            if optimization_type is None or scenario_type in optimization_type:

                response = self._input_api.get_preview_data(self._scenario_id, input_data)

                if 200 <= response.status_code < 300:
                    preview_data[input_name] = response.json()

        return preview_data

    @__integrate_api_request.input_api
    def get_input_files_data(self, inputs_data: dict, files_directory: str) -> None:

        scenario_type = self._check_scenario_type()

        save_directory = f'{files_directory}/{self._scenario_id}_files'

        if not os.path.exists(save_directory):
            os.makedirs(save_directory)

        for input_name, input_data in inputs_data.items():

            optimization_type = input_data.get('optimization_type')

            if optimization_type is None or scenario_type in optimization_type:
                file_path = f'{save_directory}/{input_name}.xlsx'

                response = self._input_api.get_input_data(self._scenario_id, input_data)

                with open(file_path, 'wb') as file:
                    file.write(response.content)

    @__integrate_api_request.input_api
    def get_input_info(self, inputs_data: dict) -> dict:

        scenario_type = self._check_scenario_type()

        input_info = {}

        for input_name, input_data in inputs_data.items():

            optimization_type = input_data.get('optimization_type')

            if optimization_type is None or scenario_type in optimization_type:

                response = self._input_api.get_input_info(self._scenario_id, input_data)

                if response.status_code < 300:
                    input_info[input_name] = response.json()

        return input_info

    def wait_scenario_info(self, waited_scenario_info: list, timeout: int = 1800) -> None:  # timeout = 1800 - 30 min
        '''
        waited_scenario_info = [key, [value, value, ...]]
        '''

        start_time = time.time()

        while True:
            time.sleep(1)

            response = self.get_scenario()

            if response.get(waited_scenario_info[0]) in waited_scenario_info[1]:
                break

            if time.time() - start_time >= timeout:
                raise TimeoutError(f'Timeout "{timeout} sec" [{waited_scenario_info}]')

            time.sleep(4)

    @__integrate_api_request.scenario_api
    def create_scenario(self, json_body: dict) -> dict:

        response = self._scenario_api.create_scenario(json_body)

        scenario_data = response.json()
        self.scenario_data = scenario_data
        self._scenario_id = scenario_data['id']

        return scenario_data

    @__integrate_api_request.scenario_api
    def get_list_of_scenarios(self, params: dict = None) -> dict:

        response = self._scenario_api.get_list_of_scenarios(params)

        return response.json()

    @__integrate_api_request.scenario_api
    def get_scenario(self) -> dict:

        response = self._scenario_api.get_scenario(self._scenario_id)

        scenario_data = response.json()
        self.scenario_data = scenario_data

        return scenario_data

    @__integrate_api_request.scenario_api
    def delete_scenario(self) -> requests.Response:

        response = self._scenario_api.delete_scenario(self._scenario_id)

        return response

    @__integrate_api_request.scenario_api
    def save_scenario_pfr(self, parameters: dict, use_additional_params: bool = False):

        results = {}

        for param_type, param_data in parameters.items():

            if param_type == 'additional_params' and not use_additional_params:
                break

            for pfr_url, json_body in param_data.items():
                response = self._scenario_api.save_scenario_pfr(self._scenario_id, pfr_url, json_body)

                results.setdefault(param_type, {}).update({pfr_url: response})

        return results

    @__integrate_api_request.scenario_api
    def calculation(self, wait_calculation_result: bool = True):

        response = self._scenario_api.calculation(self._scenario_id)

        if wait_calculation_result:
            self.wait_scenario_info(['calculation_status', ['success', 'error']])

        return response

    @__integrate_api_request.account_api
    def get_personal_info(self) -> dict:

        response = self._account_api.get_personal_info()

        personal_info = response.json()
        self.personal_info = personal_info

        return personal_info

    @__integrate_api_request.account_api
    def change_personal_info(self, json_body: dict) -> dict:

        response = self._account_api.change_personal_info(json_body)

        personal_info = response.json()
        self.personal_info = personal_info

        return personal_info

    @__integrate_api_request.output_api
    def get_kpi_data(self) -> requests.Response:

        response = self._output_api.get_kpi_data(self._scenario_id)

        return response.json()

    @__integrate_api_request.output_api
    def get_preview_output_table(self, output_table_type: str, query_params: dict = None) -> requests.Response:

        if query_params is None:
            query_params = {}

        query_params.update({'limit': 50})

        response = self._output_api.get_preview_output_table(self._scenario_id, output_table_type, query_params)

        return response.json()
