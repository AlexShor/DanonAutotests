from api.input_api_requests import InputApiRequests


class ApiOperations:
    def __init__(self, environment: str, scenario_id: int = None, auth_creds: tuple = None) -> None:

        self._environment = environment
        self._scenario_id = scenario_id
        self._input_api = InputApiRequests(environment)

        if auth_creds:
            self._input_api.authorization(*auth_creds)

    def upload_input_files(self, inputs_data: dict, files_directory: str, files_type: str = 'xlsx') -> None:

        for input_name, input_data in inputs_data.items():

            if input_data['active']:

                file_name = f'{input_name}.{files_type}'
                file_path = f'{files_directory}/{file_name}'

                response = self._input_api.upload_input_file(self._scenario_id, input_data, file_path)

                print(input_name, response.status_code)

    def delete_input_files(self, inputs_data: dict) -> None:

        for input_name, input_data in inputs_data.items():

            response = self._input_api.delete_input_file(self._scenario_id, input_data)

            print(input_name, response.status_code)

    def get_input_logs(self, inputs_data: dict) -> dict:

        input_logs = {}

        for input_name, input_data in inputs_data.items():

            response = self._input_api.get_input_log(self._scenario_id, input_data)

            if response.status_code < 300:

                input_logs[input_name] = response.text

            print(input_name, response.status_code)

        return input_logs

    def get_preview_data(self, inputs_data: dict) -> dict:

        preview_data = {}

        for input_name, input_data in inputs_data.items():

            response = self._input_api.get_preview_data(self._scenario_id, input_data)

            print(input_name, response.status_code)
            if 200 <= response.status_code < 300:
                print(response.json())


# if __name__ == "__main__":
#     optimizer_type = 'tetris'
#     environment = 'LOCAL_STAGE'
#     scenario_id = 470
#     inputs_data = InputData(optimizer_type).get_from_json()
#     creds = Creds.auth(env=environment).values()
#     files_directory = FileDirectory(optimizer_type)
#
#     operation = ApiOperations(environment, scenario_id, creds)
#
#     operation.upload_input_files(inputs_data, files_directory.valid_input_files, files_type='csv')
#     # operation.delete_input_files(inputs_data)
#     operation.get_preview_data(inputs_data)



