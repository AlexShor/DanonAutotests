# from dotenv import load_dotenv

from pages.site_data.credentials import Credentials as Creds
from api.base_api_requests import BaseApiRequests
from optimizer_data.data.input_type_name_matches import InputTypeNameMatch

import requests
# import urllib3

# load_dotenv()
# urllib3.disable_warnings()


class InputApiRequests(BaseApiRequests):

    def __extract_input_params(self, scenario_id: int, input_data: dict, request_url_param: str = '') -> dict:

        url_input_path = input_data.get('url_path')
        params_input_type = input_data.get('parameter')
        scenario_type = input_data.get('scenario_type')

        url_input_path = (f'/{url_input_path}', '')[url_input_path is None]
        inputs_in_url = ('/inputs', '')['promo' in scenario_type]

        params = ({'input_type': params_input_type}, None)[params_input_type is None]
        headers = {'Authorization': f'Bearer {self._access_token}'}

        url = f'{self._base_url}/{scenario_type}/{scenario_id}{url_input_path}{inputs_in_url}{request_url_param}'

        request_parameters = {'url': url, 'headers': headers, 'params': params, 'verify': False}

        return request_parameters

    def get_preview_data(self, scenario_id: int, input_data: dict) -> requests.Response:

        request_url_param = '/data'

        request_parameters = self.__extract_input_params(scenario_id, input_data, request_url_param)
        response = requests.get(**request_parameters)
        response.encoding = 'UTF-8'

        return response

    def get_input_log(self, scenario_id: int, input_data: dict) -> requests.Response:

        request_url_param = '/log'

        request_parameters = self.__extract_input_params(scenario_id, input_data, request_url_param)
        response = requests.get(**request_parameters)
        response.encoding = 'UTF-8'

        return response

    def upload_input_file(self,
                          scenario_id: int,
                          input_data: dict,
                          file_path: str) -> requests.Response | str:

        try:
            files = {'file': open(f'{file_path}', 'rb')}
            request_parameters = self.__extract_input_params(scenario_id, input_data)
            response = requests.post(files=files, **request_parameters)
            response.encoding = 'UTF-8'

            return response
        except FileNotFoundError:
            print('No such file or directory:', file_path)  # Доработать
            return 'Error'

    def delete_input_file(self, scenario_id: int, input_data: dict) -> requests.Response:

        request_parameters = self.__extract_input_params(scenario_id, input_data)
        response = requests.delete(**request_parameters)
        response.encoding = 'UTF-8'

        return response


# if __name__ == "__main__":
#     environment = 'LOCAL_STAGE'
#     scenario_id = 466
#     inputs_data = InputTypeNameMatch.Tetris.TYPES
#
#     session = InputApiRequests(environment).authorization(*Creds.auth(env=environment).values())
#
#
#     data = session.get_preview_data(scenario_id, inputs_data['parameters'])
#
#     print(data.text)
