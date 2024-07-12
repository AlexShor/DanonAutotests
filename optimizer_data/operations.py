import os
import time
from datetime import date, timedelta, datetime

from api.api_operations import ApiOperations
from optimizer_data.create_file_data import CreateFileData
from optimizer_data.data.input_data import InputData
from optimizer_data.data.input_speadsheets_data import Spreadsheets
from optimizer_data.data.default_data import FileDirectory
from optimizer_data.operations_file_data import OperationsFileData
from pages.site_data.credentials import Credentials
from project_data.main_data import ProjectLanguage, ProjectType, ProjectOutputTables
from project_data.default_params import CreateScenarioDefaultParams, DefaultProject, DefaultPFRdata


class Operations:
    def __init__(self,
                 optimizer_type: str,
                 environment: str = None,
                 scenario_id: int = None,
                 use_inputs_data: bool = True):

        self._environment = environment
        self._optimizer_type = optimizer_type

        if use_inputs_data:

            self._inputs_data = InputData(optimizer_type).get_from_json()

        creds = Credentials.auth(env=environment).values()

        if environment and scenario_id:

            self._api_operation = ApiOperations(environment, optimizer_type, scenario_id, creds)

        elif environment:

            self._api_operation = ApiOperations(environment, optimizer_type, auth_creds=creds)

    def __get_upload_queue_for_tetris(self, inputs_data: dict) -> dict:

        uploading_queue = {}

        for input_name, input_data in inputs_data.items():

            queue = input_data['upload_queue']

            uploading_queue.setdefault(queue, {}).update({input_name: input_data})

        return uploading_queue

    def __upload_input_files(self,
                             files_directory: str = None,
                             files_type: str = None,
                             delay_between_queue: int = None,
                             wait_file_validation: bool = True,
                             not_download_list: list = None,
                             use_download_file_name: bool = False) -> dict:

        inputs_data = self._inputs_data

        if not_download_list is not None:
            for input_name in not_download_list:
                if input_name in inputs_data.keys():
                    inputs_data[input_name].update({'not_download': True})

        result = {}

        if self._optimizer_type == ProjectType.TETRIS:

            inputs_data_upload_queue = self.__get_upload_queue_for_tetris(inputs_data)

            queue = sorted(inputs_data_upload_queue.keys())

            for i in queue:

                responses = self._api_operation.upload_input_files(inputs_data_upload_queue[i],
                                                                   files_directory,
                                                                   files_type,
                                                                   wait_file_validation,
                                                                   use_download_file_name)
                result.update(responses)

                if delay_between_queue and i != queue[-1]:
                    time.sleep(delay_between_queue)

        else:

            result = self._api_operation.upload_input_files(inputs_data,
                                                            files_directory,
                                                            files_type,
                                                            wait_file_validation,
                                                            use_download_file_name)

        return result

    def _checking_uploaded_data_status(self, result_uploading_inputs: dict):

        if all(map(lambda resp: resp.status_code < 300, result_uploading_inputs.values())):

            while True:
                if self._api_operation.get_scenario().get('uploaded_data_status'):
                    break

                time.sleep(5)

    def upload_valid_input_files(self,
                                 files_type: str = None,
                                 delay_between_queue: int = None,
                                 not_download_list: list = None,
                                 folder: str = None,
                                 from_zip: str = None,
                                 use_download_file_name: bool = False) -> None:

        files_directory = FileDirectory(self._optimizer_type).valid_input_files

        if from_zip is None:

            if folder is not None:
                files_directory = f'{files_directory}/{folder}'

            result = self.__upload_input_files(files_directory,
                                               files_type,
                                               delay_between_queue,
                                               not_download_list=not_download_list,
                                               use_download_file_name=use_download_file_name)

            self._checking_uploaded_data_status(result)

        else:

            zip_dir = f'{files_directory}/{from_zip}'
            self.upload_downloaded_input_files(zip_dir, not_download_list)

    def upload_invalid_input_files(self,
                                   files_type: str = None,
                                   delay_between_queue: int = None,
                                   not_download_list: list = None,
                                   use_download_file_name: bool = False) -> None:

        files_directory = FileDirectory(self._optimizer_type).invalid_input_files
        result = self.__upload_input_files(files_directory,
                                           files_type,
                                           delay_between_queue,
                                           not_download_list=not_download_list,
                                           use_download_file_name=use_download_file_name)

        self._checking_uploaded_data_status(result)

    def upload_downloaded_input_files(self, zip_directory: str, not_download_list: list = None):

        operation_file_data = OperationsFileData(zip_directory, self._inputs_data)
        self._inputs_data = operation_file_data.extract_downloaded_file_from_zip_and_update_input_data()

        result = self.__upload_input_files(not_download_list=not_download_list)

        self._checking_uploaded_data_status(result)

        #operation_file_data.remove_data()

    def get_validation_rules_from_google_drive(self) -> dict:

        save_time = datetime.now().strftime('%y%m%d_%H%M%S_%f')

        file_name = f'validation_rules_{self._optimizer_type}_{save_time}.xlsx'

        spreadsheet_link = Spreadsheets().get(self._optimizer_type, 'validation_rules')

        file_directory = FileDirectory(self._optimizer_type)
        validation_rules_directory = f'{file_directory.validation_rules}/{self._optimizer_type}'

        operations_file_data = OperationsFileData(validation_rules_directory)

        status_code = operations_file_data.get_from_google_drive(spreadsheet_link, file_name)

        if 200 <= status_code < 300:
            return {'directory': validation_rules_directory, 'file_name': file_name}

    def validation_rules_comparison(self, use_last_created_file: bool = True) -> dict | None:

        if use_last_created_file:

            file_directory = FileDirectory(optimizer_type)
            validation_rules_directory = f'{file_directory.validation_rules}/{self._optimizer_type}'

            operations_file_data = OperationsFileData(validation_rules_directory)
            file_dir = operations_file_data.get_durectory_to_last_validation_ruls(self._optimizer_type)

        else:

            file_dir = self.get_validation_rules_from_google_drive()

        if file_dir:

            input_data = InputData(self._optimizer_type)
            result = input_data.validation_rules_comparison(file_dir)

            return result

    def create_invalid_files(self) -> None:

        error_log_lang = ProjectLanguage.get(self._optimizer_type)

        file_directory = FileDirectory(self._optimizer_type)
        invalid_files_directory = file_directory.invalid_input_files
        error_logs_directory = file_directory.input_files_error_logs

        create_file_data = CreateFileData(self._optimizer_type, self._inputs_data)
        create_file_data.invalid_files(invalid_files_directory, error_logs_directory, error_log_lang)

    def delete_input_files(self) -> None:

        self._api_operation.delete_input_files(self._inputs_data)

    def errors_logs_comparison(self) -> None:

        error_log_lang = ProjectLanguage.get(self._optimizer_type)

        preview_rules_path = FileDirectory(self._optimizer_type).input_files_error_logs
        operations_file_data = OperationsFileData(preview_rules_path, self._inputs_data)

        received_error_logs_txt = self._api_operation.get_input_logs(self._inputs_data)

        created_error_logs = operations_file_data.read_error_logs(error_log_lang)
        received_error_logs = operations_file_data.convert_txt_err_log_to_dict(received_error_logs_txt, error_log_lang)

        comparison_result = operations_file_data.errors_logs_comparison(created_error_logs, received_error_logs)

        import pytest
        pytest.main(['-c', 'optimizer_data_tests/opti_data_pytest.ini',
                     'optimizer_data_tests/test_optimizer_data.py::test_errors_logs_comparison',
                     '--comparison_result', repr(comparison_result)])

    def get_input_files_data(self):

        downloaded_input_files_directory = FileDirectory(self._optimizer_type).downloaded_input_files

        self._api_operation.get_input_files_data(self._inputs_data, downloaded_input_files_directory)

    @staticmethod
    def show_inactive_inputs_data() -> None:

        inputs_data = InputData(optimizer_type).get_from_json(only_active_inputs=False)

        for input_name, input_data in inputs_data.items():
            if not input_data['active']:
                print(f'Not active input: {input_name}')

            for col_name, col_data in input_data['columns'].items():
                if not col_data['active']:
                    print(f'Not active col: {col_name} in {input_name}')

    def upload_multiple_files(self, input_name: str = None, timeout_input_info: int = 5) -> None:

        start_time = time.time()

        files_count = len(next(os.walk(input_name))[-1])

        _inputs_data = self._inputs_data[input_name]

        for i in range(1, files_count + 1):

            current_input_name = f'{input_name}_{i}'

            input_data = {current_input_name: _inputs_data}

            upload_input_response = self._api_operation.upload_input_files(input_data, input_name)

            if upload_input_response:

                while True:
                    get_input_info_response = self._api_operation.get_input_info(input_data)

                    data_uploading_status = get_input_info_response[current_input_name].get('data_uploading_status')

                    print('Elapsed time: ', timedelta(seconds=time.time()-start_time))

                    if data_uploading_status == 'Data successfully uploaded':
                        break

                    time.sleep(timeout_input_info)

    def create_custom_csv_file(self, file_name: str, creating_data: dict, row_count: int) -> None:

        create_file_data = CreateFileData()

        created_input_files_directory = FileDirectory(self._optimizer_type).created_input_files
        file_path = f'{created_input_files_directory}/{file_name}'

        create_file_data.create_custom_csv_file(file_path, creating_data, row_count)

    def create_scenario(self, json_body: dict = None) -> dict:

        if json_body is None:
            json_body = CreateScenarioDefaultParams().get(self._environment, self._optimizer_type)

        scenario_data = self._api_operation.create_scenario(json_body)

        return scenario_data

    def get_scenarios(self, params: dict = None) -> dict:

        if params is None:
            params = {'page': 1, 'per_page': 500}

        scenarios = self._api_operation.get_list_of_scenarios(params)

        return scenarios

    def get_scenario(self) -> dict:

        scenario_data = self._api_operation.get_scenario()

        return scenario_data

    def delete_scenario(self) -> None:

        self._api_operation.delete_scenario()

    def get_data_from_scenarios(self, list_of_data: list, params: dict = None) -> list:

        list_of_scenarios = self.get_scenarios(params).get('results')

        result = []

        for scenario in list_of_scenarios:

            result.append({data: scenario[data] for data in list_of_data if data in scenario})

        return result

    def get_personal_info(self) -> dict:

        personal_info = self._api_operation.get_personal_info()

        return personal_info

    def change_personal_info(self, json_body: dict) -> dict:

        personal_info = self._api_operation.change_personal_info(json_body)

        return personal_info

    def change_active_project(self, project_id: int = None) -> dict:

        if project_id is None:
            project_id = DefaultProject.get(self._environment, self._optimizer_type)['id']

        personal_info = self.change_personal_info({'active_project_id': project_id})

        return personal_info

    def save_defoult_scenario_pfr(self, use_additional_params: bool = False) -> dict:

        pfr_data = DefaultPFRdata().get(self._optimizer_type)

        scenario_data = self._api_operation.get_scenario()

        if self._optimizer_type == ProjectType.CFR:

            cfr_type = scenario_data['cfr_type']['code']

            results = self._api_operation.save_scenario_pfr(pfr_data[cfr_type], use_additional_params)

        else:

            results = self._api_operation.save_scenario_pfr(pfr_data, use_additional_params)

        return results

    def calculate_scenario(self):

        scenario_data = self._api_operation.get_scenario()

        if scenario_data.get('params_for_run_status') is True:

            results = self._api_operation.calculation()

            return results

    def get_calculation_status(self):
        return self._api_operation.scenario_data.get('calculation_status')

    def get_kpi_data(self):

        result = self._api_operation.get_kpi_data()

        return result


    def get_preview_output_table(self, output_table_type: str, query_params: dict = None):

        result = self._api_operation.get_preview_output_table(output_table_type, query_params)

        return result

    def get_preview_defoult_output_tables(self, query_params: dict = None):

        resultes = {}

        output_table_types = ProjectOutputTables.get(self._optimizer_type)

        if output_table_types is None:
            return None

        for output_table in output_table_types:
            resultes[output_table] = self.get_preview_output_table(output_table, query_params)


        return resultes


if __name__ == "__main__":
    environment = 'LOCAL_STAGE'  # DEV LOCAL_STAGE DEMO_STAGE PROD
    optimizer_type = ProjectType.PROMO
    scenario_id = 1758

    # -------
    # operation = Operations(optimizer_type, environment, scenario_id)
    # operation.upload_valid_input_files(not_download_list=['up_down_size'])

    # -------
    # operation = Operations(optimizer_type, environment, scenario_id)
    # operation.get_kpi_data()
    # operation.get_preview_output_table('rtm_cts_wh')

    # -------
    # dir = 'C:/Users/LexSh/Downloads/test/25_Detailed_20240617_mb_Copy_1_20240626-10_39'
    # operation = Operations(optimizer_type, environment, scenario_id)
    # operation.upload_downloaded_input_files(dir)

    # -------
    # operation = Operations(optimizer_type, environment, scenario_id)
    # operation.save_defoult_scenario_pfr()

    # -------
    # operation = Operations(optimizer_type, environment)
    # operation.change_personal_info({'active_project_id': 11})

    # -------
    # operation = Operations(optimizer_type, environment)
    # operation.get_personal_info()

    # -------
    # operation = Operations(optimizer_type, environment)
    # operation.get_data_from_scenarios(['id', 'is_in_progress'])

    # -------
    # operation = Operations(optimizer_type, environment)
    # operation.create_scenario()

    # -------
    # operation = Operations(optimizer_type, environment)
    # operation.get_scenarios()

    # -------
    # operation = Operations(optimizer_type, environment, scenario_id)
    # operation.get_scenario()

    # -------
    # operation = Operations(optimizer_type, environment, scenario_id)
    # operation.delete_scenario()

    # -------
    # operation = Operations(optimizer_type, environment, scenario_id)
    # operation.upload_multiple_files('fc')

    # -------
    # operation = Operations(optimizer_type)
    # operation.validation_rules_comparison()
    # operation.get_validation_rules_from_google_drive()

    # -------
    # operation = Operations(optimizer_type)
    # operation.create_invalid_files()

    # -------
    # operation = Operations(optimizer_type, environment, scenario_id)

    # operation.upload_invalid_input_files()
    # operation.errors_logs_comparison()
    # operation.delete_input_files()

    # operation.show_inactive_inputs_data()

    # operation.get_input_files_data()

    # operation.upload_valid_input_files(files_type='csv', delay_between_queue=10)

    # -------
    # operation = Operations(optimizer_type, use_inputs_data=False)
    # creating_data = {
    #     'mad_date': {'value': date(2024, 1, 1), 'options': {'operation': 'increase', 'value': timedelta(1), 'step': 1}},
    #     'sku': {'value': 1, 'options': {'operation': 'increase', 'value': 1, 'step': 10}},
    #     'wh': {'value': 5000, 'options': {'operation': 'increase', 'value': 10, 'step': 1}},
    #     'chain': {'value': 'chain_1', 'options': {'operation': 'increase_str', 'value': 1, 'step': 1}},
    #     'rfa_id': {'value': 100, 'options': {'operation': 'increase', 'value': 1, 'step': 1}},
    #     'ordered': {'value': 10.01, 'options': {'operation': 'increase', 'value': 0.01, 'step': 1, 'rounding': 2}},
    #     'delivered': {'value': 10.01, 'options': {'operation': 'increase', 'value': 0.01, 'step': 1, 'rounding': 2}},
    #     'test_1': {'value': 'text_value', 'options': None},
    #     'test_2': {'value': 999, 'options': None},
    #     'test_3': {'value': None, 'options': {'operation': 'random', 'rand_range': (0, 100), 'step': 5}},
    #     'test_4': {'value': None, 'options': {'operation': 'copy', 'value': 'test_1', 'step': 1}},
    #     'test_5': {'value': None, 'options': {'operation': 'copy', 'value': 'sku', 'step': 1}}
    # }
    # operation.create_custom_csv_file('fact.csv', creating_data, 1_000_000)

