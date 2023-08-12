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

        response = requests.post(url=url, verify=False, data=form_data)

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
    def get_input_log(tetris_scenario_id,
                      token,
                      params_input_type,
                      scenario_type,
                      url_input_type=None,
                      env='DEV'):

        url_input_type = (f'/{url_input_type}', '')[url_input_type is None]
        params = ({'input_type': params_input_type}, None)[params_input_type is None]
        inputs_in_url = ('/inputs', '')['promo' in scenario_type]
        headers = {'Authorization': f'Bearer {token}'}

        base_url = f'{BaseUrls.BASE_URLS_BACK.get(env)}/api'
        url = f'{base_url}/{scenario_type}/{tetris_scenario_id}{url_input_type}{inputs_in_url}/log'

        response = requests.get(url=url,
                                headers=headers,
                                params=params,
                                verify=False)
        response.encoding = 'UTF-8'

        return response

    @staticmethod
    def upload_input_file(tetris_scenario_id,
                          token,
                          params_input_type,
                          file_path,
                          scenario_type,
                          url_input_type=None,
                          env='DEV'):

        url_input_type = (f'/{url_input_type}', '')[url_input_type is None]
        params = ({'input_type': params_input_type}, None)[params_input_type is None]
        inputs_in_url = ('/inputs', '')['promo' in scenario_type]
        headers = {'Authorization': f'Bearer {token}'}

        base_url = f'{BaseUrls.BASE_URLS_BACK.get(env)}/api'
        url = f'{base_url}/{scenario_type}/{tetris_scenario_id}{url_input_type}{inputs_in_url}'

        files = {'file': open(file_path, 'rb')}

        response = requests.post(url=url,
                                 headers=headers,
                                 params=params,
                                 verify=False,
                                 files=files)

        return response

    @staticmethod
    def delete_input_file(tetris_scenario_id,
                          url_input_type,
                          token,
                          scenario_type,
                          params_input_type=None,
                          env='DEV'):

        url_input_type = (f'/{url_input_type}', '')[url_input_type is None]
        params = ({'input_type': params_input_type}, None)[params_input_type is None]
        inputs_in_url = ('/inputs', '')['promo' in scenario_type]
        headers = {'Authorization': f'Bearer {token}'}

        base_url = f'{BaseUrls.BASE_URLS_BACK.get(env)}/api'
        url = f'{base_url}/{scenario_type}/{tetris_scenario_id}{url_input_type}{inputs_in_url}'

        response = requests.delete(url=url,
                                   headers=headers,
                                   params=params,
                                   verify=False)

        return response
