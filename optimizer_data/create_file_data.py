import os
from datetime import date, time
from copy import deepcopy

from optimizer_data.data.default_data import DefaultDataFill, ErrorLogText, FileDirectory
from optimizer_data.data.excluded_data import ExcludeValidateColumns

import pandas as pd


class CreateFileData:
    def __init__(self, optimizer_type: str, inputs_data: dict) -> None:
        self._optimizer_type = optimizer_type
        self._inputs_data = inputs_data

    @staticmethod
    def _save_file(file_name: str,
                   file_data: dict,
                   save_directory: str,
                   file_type: str = 'xlsx',
                   as_error_log=False) -> None:

        file_path = f'{save_directory}/{file_name}'

        if not os.path.exists(save_directory):
            os.makedirs(save_directory)

        if as_error_log:
            error_log_data = [f'{_type} {repr(_data)}' for _type, _data in file_data.items()]

            with open(f'{file_path}.txt', 'w', encoding='utf8') as file:
                print(*error_log_data, sep='\n\n', file=file)

            return None

        df = pd.DataFrame(file_data)

        if file_type == 'xlsx':
            df.to_excel(f'{file_path}.{file_type}', index=False)
        elif file_type == 'csv':
            df.to_csv(f'{file_path}.{file_type}', index=False)
        else:
            raise TypeError(f'Wrong file type: "{file_type}"')

    def invalid_files(self,
                      valid_rules_data: dict,
                      invalid_files_directory: str | FileDirectory,
                      error_logs_directory: str | FileDirectory,
                      error_log_text_lang: str = 'eng',
                      file_type: str = 'xlsx') -> None:

        for file_name, file_data in valid_rules_data.items():

            input_data = self._inputs_data.get(file_name)

            if input_data and input_data['active']:

                created_invalid_data, error_log_data = self._creating_invalid_data(file_name,
                                                                                   file_data,
                                                                                   error_log_text_lang)

                self._save_file(file_name, created_invalid_data, invalid_files_directory, file_type)
                self._save_file(file_name, error_log_data, error_logs_directory, as_error_log=True)

    def _creating_invalid_data(self, file_name: str, file_data: dict, error_log_text_lang: str = 'eng') -> (dict, dict):

        invalid_data = {}
        error_log_data = {}
        error_log_text = ErrorLogText().get(error_log_text_lang)
        exclude_valid_cols = ExcludeValidateColumns.get(self._optimizer_type)

        def __error_log_data(column_name: str, type_error: str, row: int) -> None:

            error_log_data.setdefault(error_log_text[type_error], []).append(
                f'{error_log_text["row"]} {row} - {error_log_text["col"]} {column_name.lower()}'
            )

        def __get_validity_data(column_name: str, data: dict, row: int, validity: bool) -> str:

            if not validity:

                if column_name not in exclude_valid_cols.get(file_name, []):

                    __error_log_data(column_name, 'type', row)

            return DefaultDataFill.get(data['data_type'], validity)

        def __get_obligatory_data(column_name: str, data: dict, row: tuple, switch: bool) -> tuple:

            if data['obligatory']:
                __error_log_data(column_name, 'obligation', row[not switch])

            if switch:
                return '', __get_validity_data(column_name, data, row[switch], True)

            return __get_validity_data(column_name, data, row[not switch], True), ''

        def __get_negativity_data(column_name: str, data: dict, row: int) -> str:

            data_type = data['data_type']
            if data_type in (int, float):

                if data['negativity'] is False:
                    __error_log_data(column_name, 'negative', row)

                return '-' + DefaultDataFill.get(data_type, True)

            return __get_validity_data(column_name, data, row, True)

        def __get_integrity_data(column_name: str, data: dict, row: int, negativity: bool = False) -> str:

            types = [int, float]
            data = deepcopy(data)
            data_type = data['data_type']

            if data_type in types:
                types.remove(data_type)

                if data_type is int:
                    __error_log_data(column_name, 'type', row)
                    data['negativity'] = None

                if negativity:
                    data['data_type'] = types[0]
                    return __get_negativity_data(column_name, data, row)
                else:
                    return DefaultDataFill.get(types[0], True)

            return __get_validity_data(column_name, data, row, True)

        def __get_validation_date_data(column_name: str, data: dict, row: tuple) -> tuple:

            if data['data_type'] == date:
                date_1 = '01.07.2024'
                date_2 = '01/07/2024'
                date_3 = '2024-07-01'
                date_4 = '1.7.24'

                validity_datas = (date_1, date_2, date_3, date_4)

                __error_log_data(column_name, 'type', 4)

                return validity_datas

            validity_datas = tuple(__get_validity_data(column_name, data, r, True) for r in row)

            return validity_datas

        def __get_validation_time_data(column_name: str, data: dict, row: tuple) -> tuple:

            if data['data_type'] == time:
                time_1 = '09:45:00 AM'
                time_2 = '09:45:00 PM'
                time_3 = '09:45:00'
                time_4 = '09:45'

                validity_datas = (time_1, time_2, time_3, time_4)

                __error_log_data(column_name, 'type', 3)
                __error_log_data(column_name, 'type', 4)

                return validity_datas

            validity_datas = tuple(__get_validity_data(column_name, data, r, True) for r in row)

            return validity_datas

        obligatory_switch = True

        for col_name, col_valid_data in file_data.items():

            only_preview = self._inputs_data[file_name]['columns'][col_name]['only_for_download_and_preview']  # костыль
            active = self._inputs_data[file_name]['columns'][col_name]['active']  # костыль

            if not only_preview and active:  # костыль

                new_col_data = [
                    __get_validity_data(col_name, col_valid_data, row=2, validity=False),
                    *__get_obligatory_data(col_name, col_valid_data, row=(3, 4), switch=obligatory_switch),
                    __get_negativity_data(col_name, col_valid_data, row=5),
                    __get_integrity_data(col_name, col_valid_data, row=6, negativity=False),
                    __get_integrity_data(col_name, col_valid_data, row=7, negativity=True),
                    __get_validity_data(col_name, col_valid_data, row=8, validity=True),
                    *__get_validation_date_data(col_name, col_valid_data, row=(9, 10, 11, 12)),
                    *__get_validation_time_data(col_name, col_valid_data, row=(13, 14, 15, 16)),
                ]

                invalid_data.update({col_name: new_col_data})

                obligatory_switch = not obligatory_switch

        return invalid_data, error_log_data


# if __name__ == "__main__":
#
#     file_name = "validation_rules_tetris.xlsx"
#     validation_rules_path = FileDirectory().validation_rules
#     # invalid_input_files_path = FileDirectory('tetris').validation_rules
#
#     tetris_valid_rules = ValidateRules.get('tetris')
#     columns = tetris_valid_rules['col_names'].values()
#
#     xlsx_data = OperationsFileData(validation_rules_path).read_xlsx(file_name, 'Validation rules', get_columns=columns, skip_footer_rows=291)
#     valid_rules_data = OperationsFileData.convert_validation_rules_data_to_dict(xlsx_data, tetris_valid_rules)
#     print(valid_rules_data)
#     # CreateFileData.invalid_files(valid_rules_data, save_directory=invalid_input_files_path, error_log_text_lang='rus')
#
#     # res = CreateFileData._creating_invalid_data(valid_rules_data['Buyers contracts'], error_log_text_lang='rus')
#
#     # print(res)
