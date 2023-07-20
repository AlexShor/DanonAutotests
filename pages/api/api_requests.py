from pages.site_data.urls import BaseUrls
from dotenv import load_dotenv

import requests
import urllib3

load_dotenv()
urllib3.disable_warnings()


class PublicRequests:
    @staticmethod
    def authorization(login, password, env='DEV', get=None):
        base_url = f'{BaseUrls.BASE_URLS_BACK.get(env)}/api'
        url = f'{base_url}/auth/login'
        form_data = {"email": login, "password": password}

        response = requests.post(url, verify=False, data=form_data)
        response.encoding = 'UTF-8'

        if get == 'access':
            return response.json().get('access')
        elif get == 'refresh':
            return response.json().get('refresh')
        else:
            return response.json()

    @staticmethod
    def tetris_input_log(tetris_scenario_id, current_type, token, params_input_type, env='DEV'):
        base_url = f'{BaseUrls.BASE_URLS_BACK.get(env)}/api'
        url = f'{base_url}/tetris-scenarios/{tetris_scenario_id}/{current_type}/inputs/log'
        response = requests.get(url,
                                headers={'Authorization': f'Bearer {token}'},
                                params={'input_type': params_input_type},
                                verify=False)
        response.encoding = 'UTF-8'

        return response

    @staticmethod
    def tetris_upload_input_file(tetris_scenario_id, current_type, token, params_input_type, file_path, env='DEV'):
        files = {'file': open(file_path, 'rb')}

        base_url = f'{BaseUrls.BASE_URLS_BACK.get(env)}/api'
        url = f'{base_url}/tetris-scenarios/{tetris_scenario_id}/{current_type}/inputs'

        response = requests.post(url,
                                 headers={'Authorization': f'Bearer {token}'},
                                 params={'input_type': params_input_type},
                                 verify=False,
                                 files=files)

        return response

    @staticmethod
    def tetris_delete_input_file(tetris_scenario_id, current_type, token, env='DEV'):

        base_url = f'{BaseUrls.BASE_URLS_BACK.get(env)}/api'
        url = f'{base_url}/tetris-scenarios/{tetris_scenario_id}/{current_type}/inputs'

        response = requests.delete(url, headers={'Authorization': f'Bearer {token}'}, verify=False,)

        return response
