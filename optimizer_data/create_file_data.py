import os
from datetime import date, time, timedelta
from copy import deepcopy
from random import random, randint, randrange

from optimizer_data.data.default_data import DefaultDataFill, ErrorLogText, FileDirectory
from optimizer_data.data.excluded_data import ExcludeValidateColumns
from custom_moduls.console_design.console_decorator import log_file_operation

import pandas as pd


class CreateFileData:
    def __init__(self, optimizer_type: str = None, inputs_data: dict = None) -> None:
        self._optimizer_type = optimizer_type
        self._inputs_data = inputs_data

    @staticmethod
    def _save_file(file_name: str,
                   file_data: dict,
                   save_directory: str,
                   file_type: str = 'xlsx',
                   as_error_log=False) -> None | Exception:

        file_path = f'{save_directory}/{file_name}'

        if not os.path.exists(save_directory):
            os.makedirs(save_directory)

        if as_error_log:
            error_log_data = [f'{_type} {repr(_data)}' for _type, _data in file_data.items()]

            with open(f'{file_path}.txt', 'w', encoding='utf8') as file:
                print(*error_log_data, sep='\n\n', file=file)

            return None

        df = pd.DataFrame(file_data)

        try:

            if file_type == 'xlsx':
                df.to_excel(f'{file_path}.{file_type}', index=False)
            elif file_type == 'csv':
                df.to_csv(f'{file_path}.{file_type}', index=False)
            else:
                raise TypeError(f'Wrong file type: "{file_type}"')

        except PermissionError as ex:
            return ex

    @log_file_operation(1, True)
    def invalid_files(self,
                      invalid_files_directory: str | FileDirectory,
                      error_logs_directory: str | FileDirectory,
                      error_log_text_lang: str = 'eng',
                      file_type: str = 'xlsx') -> None:

        for file_name, file_data in self._inputs_data.items():

            if file_data['active']:

                self._create_invalid_data_and_save_file(file_name,
                                                        file_type,
                                                        file_data['columns'],
                                                        invalid_files_directory,
                                                        error_logs_directory,
                                                        error_log_text_lang)

    @log_file_operation(2)
    def _create_invalid_data_and_save_file(self,
                                           file_name: str,
                                           file_type: str,
                                           columns: dict,
                                           invalid_files_directory: str | FileDirectory,
                                           error_logs_directory: str | FileDirectory,
                                           error_log_text_lang: str) -> None | Exception:

        created_invalid_data, error_log_data = self._creating_invalid_data(file_name, columns, error_log_text_lang)

        saving_input_file_result = self._save_file(file_name, created_invalid_data, invalid_files_directory, file_type)

        if saving_input_file_result is None:
            saving_error_log_file_status = self._save_file(file_name, error_log_data,
                                                           error_logs_directory, as_error_log=True)
            return saving_error_log_file_status

        return saving_input_file_result

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
            if data_type in ('int', 'float'):

                if data['negativity'] is False:
                    __error_log_data(column_name, 'negative', row)

                return '-' + DefaultDataFill.get(data_type, True)

            return __get_validity_data(column_name, data, row, True)

        def __get_integrity_data(column_name: str, data: dict, row: int, negativity: bool = False) -> str:

            types = ['int', 'float']
            data = deepcopy(data)
            data_type = data['data_type']

            if data_type in types:
                types.remove(data_type)

                if data_type == 'int':
                    __error_log_data(column_name, 'type', row)
                    data['negativity'] = None

                if negativity:
                    data['data_type'] = types[0]
                    return __get_negativity_data(column_name, data, row)
                else:
                    return DefaultDataFill.get(types[0], True)

            return __get_validity_data(column_name, data, row, True)

        def __get_validation_date_data(column_name: str, data: dict, row: tuple) -> tuple:

            if data['data_type'] == 'date':
                date_1 = '01.07.2024'
                date_2 = '01/07/2024'
                date_3 = '2024-07-01'
                date_4 = '1.7.24'
                date_5 = '00.07.2024'
                date_6 = '01.00.2024'
                date_7 = '13.15.2024'
                date_8 = '01.32.2024'

                validity_datas = (date_1, date_2, date_3, date_4, date_5, date_6, date_7, date_8)

                # __error_log_data(column_name, 'type', 13)
                # __error_log_data(column_name, 'type', 14)
                __error_log_data(column_name, 'type', 15)
                __error_log_data(column_name, 'type', 16)

                return validity_datas

            validity_datas = tuple(__get_validity_data(column_name, data, r, True) for r in row)

            return validity_datas

        def __get_validation_time_data(column_name: str, data: dict, row: tuple) -> tuple:

            if data['data_type'] == 'time':
                time_1 = '09:45:00 AM'
                time_2 = '09:45:00 PM'
                time_3 = '09:45:00'
                time_4 = '09:45'

                validity_datas = (time_1, time_2, time_3, time_4)

                __error_log_data(column_name, 'type', 19)
                __error_log_data(column_name, 'type', 20)

                return validity_datas

            validity_datas = tuple(__get_validity_data(column_name, data, r, True) for r in row)

            return validity_datas

        obligatory_switch = True

        for col_name, col_valid_data in file_data.items():

            only_preview = col_valid_data['only_for_download_and_preview']  # костыль

            active = col_valid_data['active']  # костыль

            if not only_preview and active:  # костыль

                new_col_data = [
                    __get_validity_data(col_name, col_valid_data, row=2, validity=False),
                    *__get_obligatory_data(col_name, col_valid_data, row=(3, 4), switch=obligatory_switch),
                    __get_negativity_data(col_name, col_valid_data, row=5),
                    __get_integrity_data(col_name, col_valid_data, row=6, negativity=False),
                    __get_integrity_data(col_name, col_valid_data, row=7, negativity=True),
                    __get_validity_data(col_name, col_valid_data, row=8, validity=True),
                    *__get_validation_date_data(col_name, col_valid_data, row=(9, 10, 11, 12, 13, 14, 15, 16)),
                    *__get_validation_time_data(col_name, col_valid_data, row=(17, 18, 19, 20)),
                ]

                invalid_data.update({col_name: new_col_data})

                obligatory_switch = not obligatory_switch

        return invalid_data, error_log_data

    @staticmethod
    def __processing(i, params_length, text='Processing:'):
        step = params_length / 20
        if i % step == 0:
            percent = str(100 * i / params_length)
            print(f'\r{text} {percent}%', sep='', end='')
        if i == params_length - 1:
            print(f'\r{text} 100.0%', sep='', end='\n')

    @staticmethod
    def __increase_data_values(i: int, data_values: dict, data_options: dict, use_first_values: bool = True):

        new_data_values = data_values.copy()

        for column_name, options in data_options.items():

            if options is not None:

                if i % options['step'] == 0:

                    value = data_values[column_name]

                    if options['operation'] == 'increase' and not use_first_values:
                        if isinstance(value, tuple):
                            new_data_values[column_name] = (value[0], value[1] + options['value'])

                        elif isinstance(value, float):
                            new_value = round(new_data_values[column_name] + options['value'], options['rounding'])
                            new_data_values[column_name] = new_value

                        else:
                            new_data_values[column_name] += options['value']

                    elif options['operation'] == 'increase_str' and not use_first_values:
                        str_value, int_value = data_values[column_name].split('_')
                        new_data_values[column_name] = f"{str_value}_{int(int_value) + options['value']}"

                    elif options['operation'] == 'random':
                        new_data_values[column_name] = randint(*options['rand_range'])

                    elif options['operation'] == 'copy':
                        new_data_values[column_name] = new_data_values[options['value']]

        return new_data_values

    @classmethod
    def create_custom_csv_file(cls,
                               file_path: str,
                               creating_data: dict,
                               row_count: int,
                               write_step: int = 250_000) -> None:

        if row_count <= write_step:
            write_step = row_count - 1

        data_values = {col_name: inc_value['value'] for col_name, inc_value in creating_data.items()}
        data_options = {col_name: inc_value['options'] for col_name, inc_value in creating_data.items()}

        rows = row_count
        prec_i = 0
        mode = 'w'
        header = True
        use_first_values = True

        while rows != 0 and rows >= write_step:
            complete_data = []

            for i in range(write_step):
                data_values = cls.__increase_data_values(i, data_values, data_options, use_first_values)
                use_first_values = False

                complete_data.append(data_values)

                cls.__processing(i + prec_i, row_count)

            df = pd.DataFrame(complete_data)

            df.to_csv(file_path, mode=mode, index=False, header=header, encoding="utf_8_sig")
            mode = 'a'
            header = False

            prec_i += write_step

            rows -= write_step
            if rows < write_step:
                write_step = rows

# if __name__ == "__main__":
# d = CreateFileData('cfr')
#
# data = {
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
#
# d.create_custom_csv_file('test_fact.csv', data, 10000)


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
