import os

from api.input_api_requests import InputApiRequests
from optimizer_data.data.default_data import FileDirectory
from optimizer_data.data.input_data import InputData
from pages.site_data.credentials import Credentials


class ApiOperations:
    def __init__(self, environment: str, scenario_id: int = None, auth_creds: tuple = None) -> None:

        self._environment = environment
        self._scenario_id = scenario_id
        self._input_api = InputApiRequests(environment, auth_creds)

    def upload_input_files(self, inputs_data: dict, files_directory: str, files_type: str = 'xlsx') -> dict:

        response_data = {}

        for input_name, input_data in inputs_data.items():

            file_name = f'{input_name}.{files_type}'
            file_path = f'{files_directory}/{file_name}'

            response = self._input_api.upload_input_file(self._scenario_id, input_data, file_path)

            response_data[input_name] = response

        return response_data

    def delete_input_files(self, inputs_data: dict) -> dict:

        response_about_deletion = {}

        for input_name, input_data in inputs_data.items():

            response = self._input_api.delete_input_file(self._scenario_id, input_data)

            response_about_deletion[input_name] = response

        return response_about_deletion

    def get_input_logs(self, inputs_data: dict) -> dict:

        input_logs = {}

        for input_name, input_data in inputs_data.items():

            response = self._input_api.get_input_log(self._scenario_id, input_data)

            if response.status_code < 300:

                input_logs[input_name] = response.text

        return input_logs

    def get_preview_data(self, inputs_data: dict) -> dict:

        preview_data = {}

        for input_name, input_data in inputs_data.items():

            response = self._input_api.get_preview_data(self._scenario_id, input_data)

            if 200 <= response.status_code < 300:

                preview_data[input_name] = response.json()

        return preview_data

    def get_input_files_data(self, inputs_data: dict, files_directory: str) -> None:

        save_directory = f'{files_directory}/{self._scenario_id}_files'

        if not os.path.exists(save_directory):
            os.makedirs(save_directory)

        for input_name, input_data in inputs_data.items():

            file_path = f'{save_directory}/{input_name}.xlsx'

            response = self._input_api.get_input_data(self._scenario_id, input_data)

            with open(file_path, 'wb') as file:
                file.write(response.content)

    def get_input_info(self, inputs_data: dict) -> dict:

        input_info = {}

        for input_name, input_data in inputs_data.items():

            response = self._input_api.get_input_info(self._scenario_id, input_data)

            if response.status_code < 300:

                input_info[input_name] = response.json()

        return input_info


# if __name__ == "__main__":
#     optimizer_type = 'tetris'
#     environment = 'LOCAL_STAGE'
#     scenario_id = 473
#     inputs_data = InputData(optimizer_type).get_from_json()
#     creds = Credentials.auth(env=environment).values()
#     # files_directory = FileDirectory(optimizer_type)
#
#     operation = ApiOperations(environment, scenario_id, creds)
#
#     operation.get_preview_data(inputs_data)



