from pages.site_data.urls import BaseUrls
from dotenv import load_dotenv
from base_api_requests import BaseApiRequests

import requests
import urllib3

load_dotenv()
urllib3.disable_warnings()


class ApiInputScenarioPage(BaseApiRequests):

    @staticmethod
    def tetris_input_log(tetris_scenario_id, url_input_type, token, params_input_type, env='DEV'):
        base_url = f'{BaseUrls.BASE_URLS_BACK.get(env)}/api'
        url = f'{base_url}/tetris-scenarios/{tetris_scenario_id}/{url_input_type}/inputs/log'

        response = requests.get(url,
                                headers={'Authorization': f'Bearer {token}'},
                                params={'input_type': params_input_type},
                                verify=False)
        response.encoding = 'UTF-8'

        return response

    @staticmethod
    def tetris_upload_input_file(tetris_scenario_id, url_input_type, token, params_input_type, file_path, env='DEV'):
        base_url = f'{BaseUrls.BASE_URLS_BACK.get(env)}/api'
        url = f'{base_url}/tetris-scenarios/{tetris_scenario_id}/{url_input_type}/inputs'

        files = {'file': open(file_path, 'rb')}

        response = requests.post(url,
                                 headers={'Authorization': f'Bearer {token}'},
                                 params={'input_type': params_input_type},
                                 verify=False,
                                 files=files)

        return response

    @staticmethod
    def tetris_delete_input_file(tetris_scenario_id, url_input_type, token, params_input_type, env='DEV'):

        base_url = f'{BaseUrls.BASE_URLS_BACK.get(env)}/api'
        url = f'{base_url}/tetris-scenarios/{tetris_scenario_id}/{url_input_type}/inputs'

        response = requests.delete(url,
                                   headers={'Authorization': f'Bearer {token}'},
                                   params={'input_type': params_input_type},
                                   verify=False, )

        return response
