from pages.site_data.urls import BaseUrls
from dotenv import load_dotenv

import requests
import urllib3

load_dotenv()
urllib3.disable_warnings()


class BaseApiRequests:
    @staticmethod
    def authorization(login, password, env='DEV', get=None):
        base_url = f'{BaseUrls.BASE_URLS_BACK.get(env)}/api'
        url = f'{base_url}/auth/login'
        form_data = {"email": login, "password": password}

        response = requests.post(url, verify=False, data=form_data)
        if response.status_code == 502:
            return response.status_code
        response.encoding = 'UTF-8'

        if get == 'access':
            return response.json().get('access')
        elif get == 'refresh':
            return response.json().get('refresh')
        else:
            return response.json()

    @staticmethod
    def tetris_input_log(tetris_scenario_id,
                         token,
                         params_input_type,
                         type_scenarios,
                         url_input_type=None,
                         env='DEV'):

        url_input_type = (f'{url_input_type}/', '/')[url_input_type is None]

        base_url = f'{BaseUrls.BASE_URLS_BACK.get(env)}/api'
        url = f'{base_url}/{type_scenarios}/{tetris_scenario_id}/{url_input_type}inputs/log'

        response = requests.get(url,
                                headers={'Authorization': f'Bearer {token}'},
                                params={'input_type': params_input_type},
                                verify=False)
        response.encoding = 'UTF-8'

        return response

    @staticmethod
    def tetris_upload_input_file(tetris_scenario_id,
                                 token,
                                 params_input_type,
                                 file_path,
                                 type_scenarios,
                                 url_input_type=None,
                                 env='DEV'):

        url_input_type = (f'/{url_input_type}', '')[url_input_type is None]
        params = ({'input_type': params_input_type}, None)[params_input_type is None]
        inputs_in_url = ('/inputs', '')['promo' in type_scenarios]

        base_url = f'{BaseUrls.BASE_URLS_BACK.get(env)}/api'
        url = f'{base_url}/{type_scenarios}/{tetris_scenario_id}{url_input_type}{inputs_in_url}'

        files = {'file': open(file_path, 'rb')}

        response = requests.post(url,
                                 headers={'Authorization': f'Bearer {token}'},
                                 params=params,
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
