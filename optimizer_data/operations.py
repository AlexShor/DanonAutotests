from api.api_operations import ApiOperations
from optimizer_data.create_file_data import CreateFileData
from optimizer_data.data.input_data import InputData
from optimizer_data.data.input_speadsheets_data import Spreadsheets, ValidateRules
from optimizer_data.data.default_data import FileDirectory
from pages.site_data.credentials import Credentials


from optimizer_data.operations_file_data import OperationsFileData


class Operations:
    def __init__(self, optimizer_type: str, environment: str, scenario_id: int = None):

        self._optimizer_type = optimizer_type
        self._inputs_data = InputData(optimizer_type).get_from_json()

        creds = Credentials.auth(env=environment).values()
        if scenario_id:
            self._api_operation = ApiOperations(environment, scenario_id, creds)

    def upload_valid_input_files(self, files_type: str = 'xlsx') -> None:

        files_directory = FileDirectory(self._optimizer_type).valid_input_files
        self._api_operation.upload_input_files(self._inputs_data, files_directory, files_type=files_type)

    def upload_invalid_input_files(self, files_type: str = 'xlsx') -> None:

        files_directory = FileDirectory(self._optimizer_type).invalid_input_files
        self._api_operation.upload_input_files(self._inputs_data, files_directory, files_type=files_type)

    def create_invalid_files(self) -> None:

        file_name = f'validation_rules_{self._optimizer_type}.xlsx'
        valid_rules = ValidateRules.get(self._optimizer_type)
        columns = valid_rules['col_names'].values()

        file_directory = FileDirectory(self._optimizer_type)
        validation_rules_directory = file_directory.validation_rules
        invalid_files_directory = file_directory.invalid_input_files
        error_logs_directory = file_directory.input_files_error_logs

        operation = OperationsFileData(self._inputs_data, validation_rules_directory)

        spreadsheet_params = Spreadsheets.get(self._optimizer_type, 'validation_rules')[1]['params']

        rules_data = operation.read_xlsx(file_name, get_columns=columns, **spreadsheet_params)
        converted_valid_rules = operation.convert_validation_rules_data_to_dict(rules_data, valid_rules)

        create_file_data = CreateFileData(self._optimizer_type, self._inputs_data)
        create_file_data.invalid_files(converted_valid_rules, invalid_files_directory, error_logs_directory, 'rus')

    def delete_input_files(self) -> None:

        self._api_operation.delete_input_files(self._inputs_data)

    def errors_logs_comparison(self) -> None:

        error_log_lang = 'rus'

        preview_rules_path = FileDirectory(self._optimizer_type).input_files_error_logs
        operations_file_data = OperationsFileData(self._inputs_data, preview_rules_path)

        received_error_logs_txt = self._api_operation.get_input_logs(self._inputs_data)

        created_error_logs = operations_file_data.read_error_logs(error_log_lang)
        received_error_logs = operations_file_data.convert_txt_err_log_to_dict(received_error_logs_txt, error_log_lang)

        operations_file_data.errors_logs_comparison(created_error_logs, received_error_logs)

    def show_inactive_inputs_data(self) -> None:

        for input_name, input_data in self._inputs_data.items():
            if not input_data['active']:
                print(f'Not active input: {input_name}')

            for col_name, col_data in input_data['columns'].items():
                if not col_data['active']:
                    print(f'Not active col: {col_name} in {input_name}')


if __name__ == "__main__":
    optimizer_type = 'tetris'
    environment = 'LOCAL_STAGE'
    scenario_id = 471

    operation = Operations(optimizer_type, environment, scenario_id)

    # operation.create_invalid_files()
    # operation.upload_invalid_input_files()
    # operation.errors_logs_comparison()
    # operation.delete_input_files()

    # operation.show_inactive_inputs_data()
