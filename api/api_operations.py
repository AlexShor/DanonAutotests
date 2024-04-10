# from dotenv import load_dotenv

from pages.site_data.credentials import Credentials as Creds
from api.base_api_requests import BaseApiRequests
from api.input_api_requests import InputApiRequests
from optimizer_data.data.input_type_name_matches import InputTypeNameMatch
from optimizer_data.data.default_data import FileDirectory

import requests
# import urllib3

# load_dotenv()
# urllib3.disable_warnings()


class ApiOperations:
    def __init__(self, environment: str, scenario_id: int = None, auth_creds: tuple = None):
        self._environment = environment
        self._scenario_id = scenario_id
        self._input_api = InputApiRequests(environment)

        if auth_creds:
            self._input_api.authorization(*auth_creds)

    def upload_input_files(self, inputs_data: dict, files_directory: str, files_type: str = 'xlsx'):

        for input_name, input_data in inputs_data.items():

            file_name = f'{input_data.get("system_file_name")}.{files_type}'
            file_path = f'{files_directory}/{file_name}'

            response = self._input_api.upload_input_file(self._scenario_id, input_data, file_path)

            print(response)

    def get_input_logs(self, inputs_data: dict):

        for input_name, input_data in inputs_data.items():

            response = self._input_api.get_input_log(self._scenario_id, input_data)
            print(type(response))
            print(response)


if __name__ == "__main__":
    pass
    # environment = 'LOCAL_STAGE'
    # scenario_id = 469
    # inputs_data = InputTypeNameMatch.Tetris.TYPES
    # creds = Creds.auth(env=environment).values()
    # files_directory = FileDirectory('tetris')
    #
    # operation = ApiOperations(environment, scenario_id, creds)
    #
    # operation.upload_input_files(inputs_data, files_directory.invalid_input_files)

    #print(data.text)

